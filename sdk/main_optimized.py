import os
from crewai import Agent, Task, Crew
from cached_llm import GeminiCachedLLM # Import our custom class
from openhands_tool import OpenHandsWorkerTool
from auditor import TokenAuditor

# --- CONFIGURATION ---
# Paste the ID you got from Step 1
# Use CACHE_NAME env var to load your real cache identifier
CACHE_NAME = os.getenv("CACHE_NAME")
assert CACHE_NAME, "Missing CACHE_NAME environment variable (set to your cache ID)" 
API_KEY = os.getenv("API_KEY")  
assert API_KEY, "Missing GOOGLE_API_KEY or API_KEY environment variable"
import google.generativeai as genai
# Configure the GenAI SDK with the provided API key
genai.configure(api_key=API_KEY)

# Allow external prompts via environment variables
DEFAULT_PLAN_PROMPT = (
    "Develop 'task app' for me to communicate with my team on daily basis, assign tasks, team to update status, flag - open, close, ongoing, choose appropriate development tools, python is preferable, to be deployed in my vps"
)  # Updated as per user instruction

     
DEFAULT_CODE_PROMPT = (
    "Take the technical specification from the Architect and implement it exactly. "
    "Use the OpenHands tool to write the code, install dependencies (requests, pandas), "
   
)
plan_prompt = os.getenv("PLAN_PROMPT", DEFAULT_PLAN_PROMPT)
code_prompt = os.getenv("CODE_PROMPT", DEFAULT_CODE_PROMPT)

# 1. SETUP THE OPTIMIZED BRAIN
# Instead of a standard LLM, we use our Cached wrapper
architect_brain = GeminiCachedLLM(
    model="gemini-2.0-flash-exp",
    api_key=API_KEY,
    cache_name=CACHE_NAME
)
# 2. SETUP THE TOOLS
# Mirror the cached brain for QA (to avoid undefined name)
gemini_llm = architect_brain

engineer_tool = OpenHandsWorkerTool()

# 3. DEFINE AGENTS
architect = Agent(
    role='Chief Software Architect',
    goal='Design software using the cached standards.',
    backstory="You are the guardian of the codebase.",
    verbose=True,
    llm=architect_brain # <--- Injecting the Cached Brain
)

# # The "Project Manager" ensures the engineer actually did the job.
qa_manager = Agent(
    role='QA Lead',
    goal='Verify the software implementation meets the requirements.',
    backstory="You are strict. You check if the engineer actually created the files requested.",
    verbose=True,
    llm=gemini_llm
)

# 4. DEFINE THE TASKS

# Task 1: The Plan (Gemini thinks about it)
design_task = Task(
    timeout=60,  # abort if no LLM response after 60s
    description=plan_prompt,
    expected_output='A technical spec string to be passed to the engineer.',
    agent=architect
)

# Task 2: The Execution (OpenHands does the work)
# This is where we hand off to the local OpenHands instance
coding_task = Task(
    timeout=120,      # abort if no LLM response after 120s
    max_retries=2,    # retry at most twice on failure
    description=code_prompt,
    expected_output='Confirmation that the file exists and the script ran successfully.',
    agent=architect, # The Architect supervises the tool use
    tools=[engineer_tool],
    context=[design_task] # Uses the output from Task 1
)


# 5. EXECUTION
crew = Crew(
    agents=[architect, qa_manager],
    tasks=[design_task, coding_task],  # restored coding_task
    verbose=True
)

result = crew.kickoff()
print(result)

# PRINT THE BILL
TokenAuditor().generate_report()


