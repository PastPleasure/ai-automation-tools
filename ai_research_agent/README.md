AI Research Agent – CrewAI Project
This project is a fully autonomous AI-powered research pipeline using CrewAI. It simulates how a team of intelligent agents can collaborate to gather, analyze, and deliver insights on a given topic.
What It Does
Launches a research agent to find the top 3 AI startups founded in 2024

Sends results to an analyst agent who ranks and summarizes them

Saves the full structured result to a .txt file with timestamp

Designed for researchers, analysts, and AI system developers

Project Structure
ai_research_agent/
├── research_agent.py → Main script
├── .env → Your API keys (not tracked)
├── requirements.txt → Dependencies
├── agent_outputs/ → Auto-generated results
├── README.md → This file
Setup Instructions
1. Clone the repo
git clone https://github.com/yourusername/ai_research_agent.git
cd ai_research_agent
2. Install dependencies
pip install -r requirements.txt
3. Add your .env file
OPENAI_API_KEY=your_openai_key_here  
SERPAPI_API_KEY=your_serpapi_key_here
4. Run the research agent
python3 research_agent.py
Output
The agent workflow will run live in terminal

The final result will be saved inside agent_outputs/ as a .txt file:

Example:
agent_outputs/ai_startup_research_2025-05-08_21-33-15.txt
