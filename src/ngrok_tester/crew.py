"""Simple crew using MCP stdio to fetch from ngrok."""
from crewai import Agent, Crew, Task, LLM
from crewai.mcp import MCPServerStdio
from pathlib import Path

def main():
    # MCP stdio server config
    mcp_server = MCPServerStdio(
        command="python",
        args=[str(Path(__file__).parent / "ngrok_mcp_server.py")],
        env={}
    )
    
    # Agent with MCP server (LLM will use configured connection from dashboard)
    agent = Agent(
        role="Fetcher",
        goal="Fetch data from ngrok using the fetch_ngrok tool",
        backstory="You are an expert at using MCP tools to fetch data",
        mcps=[mcp_server],
        verbose=True
    )
    
    # Task to fetch
    task = Task(
        description="Use the fetch_ngrok MCP tool to fetch data from https://85e00b2844ad.ngrok.app and return the response",
        expected_output="The actual HTTP response from the ngrok endpoint",
        agent=agent
    )
    
    # Run crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )
    result = crew.kickoff()
    print(f"\n\n=== FINAL RESULT ===\n{result}\n")
    return result

if __name__ == "__main__":
    print(main())
