import os
import subprocess
import time
import logging
import sys
import atexit
import socket
from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-memgraph")

# Initialize FastMCP server
mcp = FastMCP("mcp-memgraph")

# Configuration from environment variables with defaults
MEMGRAPH_URI = os.getenv("MEMGRAPH_URI", "bolt://localhost:7687")
MEMGRAPH_USER = os.getenv("MEMGRAPH_USER", "")
MEMGRAPH_PASSWORD = os.getenv("MEMGRAPH_PASSWORD", "")
MEMGRAPH_CONTAINER_NAME = os.getenv("MEMGRAPH_CONTAINER_NAME", "memgraph-mcp")

# Only create the driver if we're not in the main module yet
driver = None

def is_port_open(host, port, timeout=1):
    """Check if a port is open on a host"""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def is_container_running(container_name):
    """Check if a Docker container is running"""
    try:
        output = subprocess.check_output(
            ["docker", "inspect", "-f", "{{.State.Running}}", container_name],
            stderr=subprocess.DEVNULL
        )
        return output.strip().decode() == "true"
    except subprocess.CalledProcessError:
        return False

def start_memgraph():
    """Start the Memgraph Docker container if it's not already running"""
    if is_container_running(MEMGRAPH_CONTAINER_NAME):
        logger.info(f"Memgraph container '{MEMGRAPH_CONTAINER_NAME}' is already running")
        return
    
    logger.info(f"Starting Memgraph container '{MEMGRAPH_CONTAINER_NAME}'...")
    
    try:
        # Remove the container if it exists but is not running
        subprocess.run(
            ["docker", "rm", "-f", MEMGRAPH_CONTAINER_NAME],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Start the container
        subprocess.run([
            "docker", "run", "-d",
            "--name", MEMGRAPH_CONTAINER_NAME,
            "-p", "7687:7687",
            "-p", "7444:7444",
            "memgraph/memgraph-mage:latest",
            "--log-level=TRACE",
            "--schema-info-enabled=true"
        ], check=True)
        
        # Wait for the container to be ready
        max_retries = 30
        retry_count = 0
        while retry_count < max_retries:
            if is_port_open("localhost", 7687):
                logger.info("Memgraph is ready!")
                return
            logger.info(f"Waiting for Memgraph to be ready... ({retry_count+1}/{max_retries})")
            time.sleep(1)
            retry_count += 1
        
        raise Exception("Memgraph failed to start in time")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start Memgraph: {e}")
        sys.exit(1)

def stop_memgraph():
    """Stop the Memgraph Docker container"""
    logger.info(f"Stopping Memgraph container '{MEMGRAPH_CONTAINER_NAME}'...")
    try:
        subprocess.run(["docker", "stop", MEMGRAPH_CONTAINER_NAME], check=True)
        subprocess.run(["docker", "rm", MEMGRAPH_CONTAINER_NAME], check=True)
    except subprocess.CalledProcessError as e:
        logger.warning(f"Error stopping Memgraph: {e}")

def get_driver():
    """Get or create the Neo4j driver with lazy initialization"""
    global driver
    if driver is None:
        driver = GraphDatabase.driver(MEMGRAPH_URI, auth=(MEMGRAPH_USER, MEMGRAPH_PASSWORD))
    return driver

def execute_query(query):
    """Helper function to execute a query on Memgraph"""
    with get_driver().session() as session:
        return session.run(query).data()

@mcp.tool()
def run_query(query: str) -> list:
    """Run a query against Memgraph"""
    logger.info(f"Running query: {query}")
    try:
        result = execute_query(query)
        return result
    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        return [f"Error: {str(e)}"]

@mcp.resource("schema://main")
def get_schema() -> str:
    """Get Memgraph schema information as a resource"""
    logger.info("Fetching Memgraph schema...")
    try:
        with get_driver().session() as session:
            return session.run("SHOW SCHEMA INFO").data()
    except Exception as e:
        logger.error(f"Schema fetch failed: {str(e)}")
        return f"Error fetching schema: {str(e)}"

if __name__ == "__main__":
    # Register cleanup function
    atexit.register(stop_memgraph)
    
    # Start Memgraph container
    start_memgraph()
    
    # Log configuration for debugging
    logger.info(f"Memgraph MCP Server Configuration:")
    logger.info(f"  URI: {MEMGRAPH_URI}")
    logger.info(f"  User: {MEMGRAPH_USER}")
    logger.info(f"  Password: {'*' * len(MEMGRAPH_PASSWORD) if MEMGRAPH_PASSWORD else '(not set)'}")
    logger.info(f"  Container: {MEMGRAPH_CONTAINER_NAME}")
    
    # Initialize and run the server
    logger.info("Starting FastMCP server...")
    mcp.run(transport="stdio")
