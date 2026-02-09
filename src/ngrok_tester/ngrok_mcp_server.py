"""Simple MCP Server to fetch from ngrok."""
import asyncio
import json
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("ngrok-fetch")

@app.list_tools()
async def list_tools():
    return [Tool(
        name="fetch_ngrok",
        description="Fetch data from ngrok endpoint",
        inputSchema={"type": "object", "properties": {}}
    )]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "fetch_ngrok":
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://85e00b2844ad.ngrok.app")
                return [TextContent(type="text", text=f"Status: {resp.status_code}\nBody: {resp.text[:500]}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

if __name__ == "__main__":
    async def main():
        async with stdio_server() as (read, write):
            await app.run(read, write, app.create_initialization_options())
    asyncio.run(main())
