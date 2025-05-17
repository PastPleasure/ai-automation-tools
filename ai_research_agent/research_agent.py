from crewai import Agent, Task, Crew
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument('--topic', type=str, help='Topic for the agents')
args = parser.parse_args()
topic = args.topic if args.topic else "AI startups 2024"

load_dotenv(dotenv_path="")  # Adjust the path to your .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")



# Define AI agents
researcher = Agent(
    role='AI Market Researcher',
    goal='Discover the top 3 AI startups launched in 2024',
    backstory='You are a veteran AI analyst with deep knowledge of market trends, emerging companies, and funding rounds.',
    verbose=False
)

analyst = Agent(
    role="Startup Analyst",
    goal="Evaluate the companies based on innovation and market potential.",
    backstory="You specialize in evulating early-stage tech companies and giving clear, structured summaries of their value.",
    verbose=False
)

writer = Agent(
    role="AI Content Writer",
    goal="Write a short blog article summarizing the research and analysis.",
    backstory="You are an expert blog writer for tech and startup audiences. You write clear, engaging summaries with SEO in mind.",
    verbose=False
)

task1 = Task(
    description=f"Search for the top 3 most promising startups in: {topic}",
    expected_output='A list of 3 AI startup names with a 2-3 sentence description of each and any notable investors.',
    agent=researcher
)

task2 = Task(
    description=f"Summarize the 3 companies found by the researcher and rank them by innovation and market potential. Use structured bullet points for clarity.",
    expected_output='A bullet-pointed summary of each startup with a short analysis and a final ranking from 1st to 3rd place.',
    agent=analyst
)

task3 = Task(
    description="Write a 300-500 word article summarizing the research findings and ranking. Include an SEO blog title and 3 relevant hashtags.",
    expected_output="A blog-style article with clear formatting, a compelling title, and 3 relevant hashtags.",
    agent=writer
)

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[task1, task2, task3],
    verbose=False
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

print(f"\nResults saved to {output_file}")

memory_entry = {
    "timestamp": timestamp,
    "topic": topic,
    "result": str(result)
}

with open("memory.jsonl", "a", encoding="utf-8") as memfile:
    memfile.write(json.dumps(memory_entry) + "\n")
    
print("\nMemory updated.")
