from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv(dotenv_path="..")  # Adjust the path to your .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")

# Define AI agents
researcher = Agent(
    role='AI Market Researcher',
    goal='Discover the top 3 AI startups launched in 2024',
    backstory='You are a veteran AI analyst with deep knowledge of market trends, emerging companies, and funding rounds.',
    verbose=True,
)

analyst = Agent(
    role="Startup Analyst",
    goal="Evaluate the companies based on innovation and market potential.",
    backstory="You specialize in evulating early-stage tech companies and giving clear, structured summaries of their value.",
    verbose=True,
)

task1 = Task(
    description='Search for the top 3 most promising AI startups launched in 2024. Include their name, what they do, and any key investors or innovations.',
    expected_output='A list of 3 AI startup names with a 2-3 sentence description of each and any notable investors.',
    agent=researcher,
    
)

task2 = Task(
    description='Summarize the 3 companies found by the researcher and rank them by innovation and market potential. Use structured bullet points for clarity.',
    expected_output='A bullet-pointed summary of each startup with a short analysis and a final ranking from 1st to 3rd place.',
    agent=analyst
)

crew = Crew(
    agents=[researcher, analyst],
    tasks=[task1, task2],
    verbose=True,
)

print("Starting anget workflow...\n")
result = crew.kickoff()
print("Workflow completed.\n")
print(result)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("agent_outputs", exist_ok=True)
output_file = f"agent_outputs/ai_startup_research_{timestamp}.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(str(result))

print(f"Results saved to {output_file}")

      