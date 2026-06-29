from fastapi import APIRouter

from src.agents.property_agent import property_agent

query_router = APIRouter()


@query_router.get("/v1/query/response")
async def get_query_response(query: str):
    result = await property_agent.run(query)
    return result.output
