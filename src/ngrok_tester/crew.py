"""Simple crew - no tools, just testing deployment."""
from crewai import Agent, Crew, Task

def main():
    # Simple agent without tools
    agent = Agent(
        role="Greeter",
        goal="Say hello from deployed crew",
        backstory="You are a friendly assistant",
        verbose=True
    )
    
    # Simple task
    task = Task(
        description="Say 'Hello from ngrok-tester crew! Deployment works!'",
        expected_output="A greeting message",
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
