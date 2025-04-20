# 🚀 Memgraph MCP Server

Memgraph MCP Server is a lightweight server implementation of the Model Context Protocol (MCP) designed to connect Memgraph with LLMs.

![mcp-server](./mcp-server.png)

## ⚡ Quick start

> 📹 [Memgraph MCP Server Quick Start video](https://www.youtube.com/watch?v=0Tjw5QWj_qY)

### 1. Run Memgraph Database

The easiest way to run Memgraph is using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- Memgraph MAGE with schema info enabled
- Memgraph Lab (web UI) at http://localhost:3000

You can also run Memgraph manually:
```bash
docker run -p 7687:7687 -p 7444:7444 memgraph/memgraph-mage:latest --schema-info-enabled=true
```

### 2. Configure Environment Variables

The server supports configuration through environment variables:

```bash
export MEMGRAPH_URI="bolt://localhost:7687"  # Default
export MEMGRAPH_USER="user"                  # Optional
export MEMGRAPH_PASSWORD="password"          # Optional
```

### 3. Run Memgraph MCP Server

1. Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and create `venv` with `uv venv`. Activate virtual environment with `.venv\Scripts\activate`. 
2. Install dependencies: `uv add "mcp[cli]" httpx`
3. Run Memgraph MCP server: `uv run server.py`.

### 4. Run MCP Client
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

Example config:
```json
{
    "mcpServers": {
      "memgraph": {
        "command": "/path/to/uv",
        "args": [
            "--directory",
            "/path/to/mcp-memgraph",
            "run",
            "server.py"
        ],
        "env": {
            "MEMGRAPH_URI": "bolt://localhost:7687",
            "MEMGRAPH_USER": "",
            "MEMGRAPH_PASSWORD": ""
        }
     }
   }
}
```
> [!NOTE]  
> You may need to put the full path to the uv executable in the command field. You can get this by running `which uv` on MacOS/Linux or `where uv` on Windows. Make sure you pass in the absolute path to your server.

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
