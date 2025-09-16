from fastapi import APIRouter 

etl_router = APIRouter()

@etl_router.post("/v1/documents/:id")
def add_document(id: str, name: str, path: str):
    pass