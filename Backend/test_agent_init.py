
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

try:
    print("Attempting to import food_agent...")
    from Backend.agents.food_agent import food_agent
    print("Successfully imported food_agent.")
    print(f"Agent Model ID: {food_agent.model.id}")
    print(f"Agent Base URL: {food_agent.model.base_url}")
except Exception as e:
    print(f"Error initializing agent: {e}")
    sys.exit(1)
