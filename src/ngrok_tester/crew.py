"""Simple crew using HTTP tool to fetch from ngrok."""
from crewai import Agent, Crew, Task
from crewai.tools import tool
import urllib.request
import ssl

@tool("fetch_ngrok")
def fetch_ngrok() -> str:
    """Fetches data from the ngrok endpoint at https://85e00b2844ad.ngrok.app"""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request("https://85e00b2844ad.ngrok.app")
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            body = resp.read().decode('utf-8')[:500]
            return f"Status: {resp.status}\nBody: {body}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Agent with HTTP tool
    agent = Agent(
        role="Fetcher",
        goal="Fetch data from ngrok using the fetch_ngrok tool",
        backstory="You are an expert at fetching data from URLs",
        tools=[fetch_ngrok],
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
