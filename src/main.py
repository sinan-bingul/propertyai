"""FastAPI application for PropertyAI."""

from fastapi import FastAPI
from src.routers.etl_router import etl_router
from src.routers.query_router import query_router

app = FastAPI()
app.include_router(etl_router)
app.include_router(query_router)

@app.get("/")
async def read_root():
    """Root endpoint."""
    return {"Hello": "World"}