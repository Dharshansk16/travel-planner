import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient

_tools  = None
_client = None

async def _load():
    global _tools, _client
    _client = MultiServerMCPClient({
        "travel_planner": {
            "command":   sys.executable,
            "args":      ["packages/travel_mcp/src/travel_mcp/server.py"],
            "transport": "stdio",
        }
    })
    _tools = await _client.get_tools()
    return _tools, _client

def load_tools():
    global _tools, _client
    if _tools is None:
        _tools_list, _client = asyncio.run(_load())
        _tools = _tools_list
    return {t.name: t for t in _tools}, _client

def get_tool_list():
    """Returns raw tool list for LLM binding."""
    load_tools()
    return _tools