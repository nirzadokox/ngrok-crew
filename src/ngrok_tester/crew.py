"""Simple crew using MCP stdio to fetch from ngrok."""
from crewai import Agent, Crew, Task
from crewai.mcp.transports.stdio import StdioTransport
from crewai.mcp import MCPClient
from pathlib import Path

def main():
    # MCP stdio transport - spawns Python process with ngrok_mcp_server.py
    transport = StdioTransport(
        command="python",
        args=[str(Path(__file__).parent / "ngrok_mcp_server.py")],
        env={}
    )
    
    # Agent with MCP client
    agent = Agent(
        role="Fetcher",
        goal="Fetch data from ngrok",
        backstory="Fetches data via MCP",
        mcp_client=MCPClient(transport=transport)
    )
    
    # Task to fetch
    task = Task(
        description="Use fetch_ngrok tool to get data from ngrok endpoint",
        expected_output="Response from ngrok",
        agent=agent
    )
    
    # Run crew
    crew = Crew(agents=[agent], tasks=[task])
    return crew.kickoff()

if __name__ == "__main__":
    print(main())
