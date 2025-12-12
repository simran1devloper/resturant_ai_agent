# backend/agents/food_agent.py
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import os
from .prompts import SYSTEM_PROMPT

from .tools import (
    create_order,
    view_order,
    confirm_order,
)

# Load latest RAG Knowledge Base
from Backend.Rag.knowledge_base import load_rag_kb

# ----- Load Knowledge Base (Chroma Vector DB) -----
kb = load_rag_kb()   # persistent RAG store

# ----- Register Tools (Order operations only) -----
TOOLS = [
    create_order,
    view_order,
    confirm_order,
]

# ----- Agent Definition -----
food_agent = Agent(
    name="food_ordering_rag_agent",
    model=OpenAIChat(
        id="gpt-4o-mini",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    ),
    knowledge=kb,                  # RAG Knowledge Base
    tools=TOOLS,                   # Menu & Order tools
    instructions=SYSTEM_PROMPT,    # System behavior
    markdown=True,

)
