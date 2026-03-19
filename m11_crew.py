from crewai import Agent, Task, Crew
from dotenv import load_dotenv
load_dotenv()

# No ChatGroq import needed
# CrewAI uses model string format directly

researcher = Agent(
    role="Research Analyst",
    goal="Find key information about a given topic",
    backstory="Expert at researching and summarising information",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write clear blog posts from research",
    backstory="Skilled at making complex topics simple",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

task1 = Task(
    description="Research AI trends in Singapore 2025",
    expected_output="Key bullet points on AI trends",
    agent=researcher
)

task2 = Task(
    description="Write a 200-word blog post from the research",
    expected_output="A short blog post",
    agent=writer
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    verbose=True
)

result = crew.kickoff()
print("\nFinal Output:", result)