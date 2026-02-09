"""Test MCP server directly."""
import asyncio
import subprocess
import json
from mcp.client.stdio import stdio_client, StdioServerParameters

async def test_mcp():
    server_path = r"c:\Users\Nir Zadok\research\ngrok_crew_minimal\src\ngrok_tester\ngrok_mcp_server.py"
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_path],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        # Initialize
        init = await read()
        print(f"Server init: {init}")
        
        # Request tool list
        await write.send({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        })
        
        tools_response = await read()
        print(f"\nTools available: {tools_response}")
        
        # Call the tool
        await write.send({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "fetch_ngrok",
                "arguments": {}
            }
        })
        
        result = await read()
        print(f"\nTool result: {result}")

if __name__ == "__main__":
    asyncio.run(test_mcp())
