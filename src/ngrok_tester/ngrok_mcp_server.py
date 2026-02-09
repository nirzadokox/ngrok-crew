"""Simple MCP Server to fetch from ngrok."""
import asyncio
import json
import httpx
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("ngrok-fetch")

def log(msg):
    """Log to stderr so it doesn't interfere with stdio protocol."""
    print(f"[MCP SERVER] {msg}", file=sys.stderr, flush=True)

@app.list_tools()
async def list_tools():
    log("list_tools called")
    return [Tool(
        name="fetch_ngrok",
        description="Fetch data from ngrok endpoint",
        inputSchema={"type": "object", "properties": {}}
    )]

@app.call_tool()
async def call_tool(name, arguments):
    log(f"call_tool: name={name}, arguments={arguments}")
    if name == "fetch_ngrok":
        try:
            url = "https://85e00b2844ad.ngrok.app"
            log(f"Making GET request to {url}")
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url)
                log(f"Got response: status={resp.status_code}")
                result = f"Status: {resp.status_code}\nBody: {resp.text[:500]}"
                log(f"Returning result: {result[:100]}")
                return [TextContent(type="text", text=result)]
        except Exception as e:
            log(f"Error occurred: {e}")
            return [TextContent(type="text", text=f"Error: {e}")]

if __name__ == "__main__":
    async def main():
        async with stdio_server() as (read, write):
            await app.run(read, write, app.create_initialization_options())
    asyncio.run(main())
