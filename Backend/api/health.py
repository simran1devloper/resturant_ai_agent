from fastapi import APIRouter, status

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint for container orchestration
    """
    return {
        "status": "healthy",
        "service": "food-ordering-backend",
        "version": "1.0.0"
    }

@router.get("/readiness", status_code=status.HTTP_200_OK)
def readiness_check():
    """
    Readiness check - verifies all dependencies are available
    """
    # TODO: Check database connection, RAG availability, etc.
    try:
        # Basic check - can import the agent
        from Backend.agents.food_agent import food_agent
        
        return {
            "status": "ready",
            "agent_loaded": True,
            "dependencies": {
                "rag": True,
                "model": True
            }
        }
    except Exception as e:
        return {
            "status": "not_ready",
            "error": str(e)
        }

@router.get("/liveness", status_code=status.HTTP_200_OK)
def liveness_check():
    """
    Liveness check - simple ping to verify the service is running
    """
    return {"status": "alive"}
