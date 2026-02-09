"""Crew that uses MCP stdio to interact with ngrok endpoint."""

from crewai import Agent, Crew, Task
from crewai.mcp.transports.stdio import StdioTransport
from crewai.mcp import MCPClient
from pathlib import Path


def create_ngrok_crew():
    """Create a crew that interacts with ngrok through MCP."""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent.absolute()
    server_path = script_dir / "ngrok_mcp_server.py"
    
    # Configure MCP stdio transport - uses StdioServerParameters pattern
    # This matches: server_params = StdioServerParameters(command, args, env)
    mcp_transport = StdioTransport(
        command="python",
        args=[str(server_path)],
        env={}
    )
    
    # Create MCP client
    mcp_client = MCPClient(transport=mcp_transport)
    
    # Define agent
    ngrok_agent = Agent(
        role="Ngrok API Tester",
        goal="Send requests to the ngrok endpoint and analyze responses",
        backstory="Expert at testing APIs using MCP tools",
        verbose=True,
        mcp_client=mcp_client,
    )
    
    # Define task
    test_task = Task(
        description=(
            "Use MCP tools to:\n"
            "1. Get ngrok URL with get_ngrok_url\n"
            "2. Send GET request with send_ngrok_request\n"
            "3. Send POST request with sample data\n"
            "4. Analyze and report results"
        ),
        expected_output="Detailed report with URL, status codes, and analysis",
        agent=ngrok_agent,
    )
    
    # Create crew
    crew = Crew(
        agents=[ngrok_agent],
        tasks=[test_task],
        verbose=True,
    )
    
    return crew


def main():
    """Run the crew."""
    print("Starting Ngrok Crew...")
    crew = create_ngrok_crew()
    result = crew.kickoff()
    print(f"\nResults:\n{result}")
    return result


if __name__ == "__main__":
    main()
