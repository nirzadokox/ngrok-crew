"""Simple crew using HTTP tool to fetch from ngrok."""
from crewai import Agent, Crew, Task
from crewai.tools import BaseTool
import httpx

class FetchNgrokTool(BaseTool):
    name: str = "fetch_ngrok"
    description: str = "Fetches data from the ngrok endpoint at https://85e00b2844ad.ngrok.app"
    
    def _run(self) -> str:
        """Fetch from ngrok endpoint."""
        try:
            with httpx.Client(timeout=30) as client:
                resp = client.get("https://85e00b2844ad.ngrok.app")
                return f"Status: {resp.status_code}\nBody: {resp.text[:500]}"
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    # Simple HTTP tool
    fetch_tool = FetchNgrokTool()
    
    # Agent with HTTP tool
    agent = Agent(
        role="Fetcher",
        goal="Fetch data from ngrok using the fetch_ngrok tool",
        backstory="You are an expert at fetching data from URLs",
        tools=[fetch_tool],
        verbose=True
    )
    
    # Task to fetch
    task = Task(
        description="Use the fetch_ngrok tool to fetch data from the ngrok endpoint and return the response",
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
