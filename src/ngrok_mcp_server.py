"""MCP Server for sending requests to ngrok endpoint."""

import asyncio
import json
import logging
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ngrok endpoint
NGROK_URL = "https://85e00b2844ad.ngrok.app"

# Create MCP server
app = Server("ngrok-requester")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="send_ngrok_request",
            description="Send a request to the ngrok endpoint",
            inputSchema={
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "description": "HTTP method (GET, POST, PUT, DELETE)",
                        "enum": ["GET", "POST", "PUT", "DELETE"],
                        "default": "GET"
                    },
                    "path": {
                        "type": "string",
                        "description": "API path (e.g., /api/endpoint)",
                        "default": "/"
                    },
                    "data": {
                        "type": "object",
                        "description": "JSON data to send (for POST/PUT)",
                        "default": {}
                    },
                    "params": {
                        "type": "object",
                        "description": "Query parameters",
                        "default": {}
                    }
                },
            },
        ),
        Tool(
            name="get_ngrok_url",
            description="Get the configured ngrok URL",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    logger.info(f"Tool called: {name} with arguments: {arguments}")
    
    if name == "get_ngrok_url":
        return [
            TextContent(
                type="text",
                text=f"Ngrok URL: {NGROK_URL}"
            )
        ]
    
    elif name == "send_ngrok_request":
        method = arguments.get("method", "GET")
        path = arguments.get("path", "/")
        data = arguments.get("data", {})
        params = arguments.get("params", {})
        
        url = f"{NGROK_URL}{path}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                logger.info(f"Sending {method} request to {url}")
                
                if method == "GET":
                    response = await client.get(url, params=params)
                elif method == "POST":
                    response = await client.post(url, json=data, params=params)
                elif method == "PUT":
                    response = await client.put(url, json=data, params=params)
                elif method == "DELETE":
                    response = await client.delete(url, params=params)
                else:
                    return [
                        TextContent(
                            type="text",
                            text=f"Unsupported method: {method}"
                        )
                    ]
                
                result = {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text,
                }
                
                try:
                    result["json"] = response.json()
                except Exception:
                    pass
                
                logger.info(f"Response received: {response.status_code}")
                
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )
                ]
        
        except Exception as e:
            logger.error(f"Request failed: {e}", exc_info=True)
            return [
                TextContent(
                    type="text",
                    text=f"Error sending request: {str(e)}"
                )
            ]
    
    else:
        return [
            TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )
        ]


async def main():
    """Run the MCP server."""
    logger.info("Starting ngrok MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
