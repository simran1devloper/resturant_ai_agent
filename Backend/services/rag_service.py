from Backend.agents.food_agent import food_agent


class RAGService:

    @staticmethod
    def query_rag(question):
        response = food_agent.run(question)
        return response
