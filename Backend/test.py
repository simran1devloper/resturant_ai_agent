from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

# Create the model instance
model = ChatOpenAI(
    model="openai/gpt-4o-mini",         # OpenRouter requires provider prefix
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",   # MUST override
    default_headers={
        "HTTP-Referer": "http://localhost",     # required by OpenRouter
        "X-Title": "My LangChain App",
    }
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello, how are you?"),
]

# Correct invoke method --> use model.invoke()
response = model.invoke(messages)

print("response:", response.content)
