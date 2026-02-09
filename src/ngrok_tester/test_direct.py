"""Direct test of MCP stdio."""
import asyncio
from pathlib import Path
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    server_path = str(Path(__file__).parent / "ngrok_mcp_server.py")
    print(f"Starting MCP server: {server_path}")
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
        env=None
    )
    
    print("Connecting to MCP server...")
    async with stdio_client(server_params) as (read_stream, write_stream):
        from mcp.client.session import ClientSession
        
        async with ClientSession(read_stream, write_stream) as session:
            print("Initializing session...")
            await session.initialize()
            
            print("Listing tools...")
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            print("Calling fetch_ngrok tool...")
            result = await session.call_tool("fetch_ngrok", arguments={})
            print(f"Result: {result}")
            
            for content in result.content:
                print(f"Content: {content.text}")

if __name__ == "__main__":
    asyncio.run(main())
