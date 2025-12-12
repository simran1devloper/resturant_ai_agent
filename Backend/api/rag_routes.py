from fastapi import APIRouter
from Backend.agents.food_agent import food_agent


router = APIRouter()


@router.get("/query")
def query_rag(q: str):
    response = food_agent.run(q)
    print(response.content)
    return {"content": response.content}

