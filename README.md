# 🚀 Memgraph MCP Server

Memgraph MCP Server is a lightweight server implementation of the Model Context Protocol (MCP) designed to connect Memgraph with LLMs.

![mcp-server](./mcp-server.png)

## ⚡ Quick start

> 📹 [Memgraph MCP Server Quick Start video](https://www.youtube.com/watch?v=0Tjw5QWj_qY)

### 🐳 Automatic Docker Mode (Recommended)

The server can automatically manage a Memgraph Docker container for you:

1. Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and create `venv` with `uv venv`. 
2. Activate virtual environment with `source .venv/bin/activate` (MacOS/Linux) or `.venv\Scripts\activate` (Windows).
3. Install dependencies: `uv add "mcp[cli]" httpx neo4j`
4. Run the auto-Docker server: `python server_with_docker.py`

The server will:
- Start a Memgraph container if none is running
- Wait for Memgraph to be ready
- Connect to the database
- Clean up when shutting down

### Manual Mode

#### 1. Configure Environment Variables

The server supports configuration through environment variables:

```bash
export MEMGRAPH_URI="bolt://localhost:7687"  # Default
export MEMGRAPH_USER="user"                  # Optional
export MEMGRAPH_PASSWORD="password"          # Optional
export MEMGRAPH_CONTAINER_NAME="memgraph-mcp" # For Docker mode
```

#### 2. Run Memgraph MCP Server

For manual mode (when you're managing Memgraph yourself):
```bash
python server.py
```

#### 3. Run MCP Client
1. Install [Claude for Desktop](https://claude.ai/download).
2. Add the Memgraph server to Claude config: 

**MacOS/Linux**
```
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows**

```
code $env:AppData\Claude\claude_desktop_config.json
```

Example config for auto-Docker mode:
```json
{
    "mcpServers": {
      "memgraph": {
        "command": "/path/to/python",
        "args": ["/path/to/mcp-memgraph/server_with_docker.py"],
        "env": {
            "MEMGRAPH_URI": "bolt://localhost:7687",
            "MEMGRAPH_CONTAINER_NAME": "memgraph-mcp"
        }
     }
   }
}
```

Example config for manual mode:
```json
{
    "mcpServers": {
      "memgraph": {
        "command": "/path/to/python",
        "args": ["/path/to/mcp-memgraph/server.py"],
        "env": {
            "MEMGRAPH_URI": "bolt://localhost:7687",
            "MEMGRAPH_USER": "user",
            "MEMGRAPH_PASSWORD": "password"
        }
     }
   }
}
```

> [!NOTE]  
> Replace paths with the appropriate values for your system.

## 🔧Tools

### run_query()
Run a Cypher query against Memgraph.

## 🗃️ Resources

### get_schema()
Get Memgraph schema information (prerequisite: `--schema-info-enabled=True`).

## 🗺️ Roadmap

The Memgraph MCP Server is just at its beginnings. We're actively working on expanding its capabilities and making it even easier to integrate Memgraph into modern AI workflows. In the near future, we'll be releasing a TypeScript version of the server to better support JavaScript-based environments. Additionally, we plan to migrate this project into our central [AI Toolkit](https://github.com/memgraph/ai-toolkit) repository, where it will live alongside other tools and integrations for LangChain, LlamaIndex, and MCP. Our goal is to provide a unified, open-source toolkit that makes it seamless to build graph-powered applications and intelligent agents with Memgraph at the core.

## Contributing

Contributions are welcome! Please feel free to submit pull requests, report bugs, or suggest features through GitHub issues.
