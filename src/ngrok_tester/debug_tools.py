"""Debug: check what tools the agent sees."""
from crewai import Agent, LLM
from crewai.mcp.transports.stdio import StdioTransport
from crewai.mcp import MCPClient
from pathlib import Path
import asyncio

async def check_tools():
    transport = StdioTransport(
        command="python",
        args=[str(Path(__file__).parent / "ngrok_mcp_server.py")],
        env={}
    )
    
    mcp_client = MCPClient(transport=transport)
    
    # Try to initialize and list tools
    print("Initializing MCP client...")
    await mcp_client.initialize()
    
    print(f"Tools available: {mcp_client.list_tools_sync()}")

if __name__ == "__main__":
    asyncio.run(check_tools())
