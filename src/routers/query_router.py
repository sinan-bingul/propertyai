from fastapi import APIRouter
from src.services.agent_orchestrator import AgentOrchestrator
query_router = APIRouter()

@query_router.get("/v1/query/response")
async def get_query_response(query: str):
    return await AgentOrchestrator().response(query)
    
