import asyncio
import sys
from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_mcp_tools():
    client = MultiServerMCPClient({
        "travel_planner": {
            "command":   sys.executable,
            "args":      ["packages/travel_mcp/src/travel_mcp/server.py"],
            "transport": "stdio",
        }
    })
    tools = await client.get_tools()
    return tools, client

def load_tools():
    tools_list, client = asyncio.run(get_mcp_tools())
    return {t.name: t for t in tools_list}, client