"""FastAPI application for PropertyAI."""
from typing import Union 
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    """Root endpoint."""
    return {"Hello": "World"}

@app.post("/v1/documents/{id}/upload")
async def upload_document(id: str):
    """uploads the document to the postgres database""" 

    #placeholder code
    return {"document_name": id}

@app.post("/v1/documents/{id}/transcriptions")
async def transcribe_document(id: str):
    """Reads the document, transcribes the pdf and stores it in the postgres database"""
    
    #placeholder code
    return {"document_id": id}

@app.post("/v1/documents/{id}/index")
async def index_document(id: str):
    """The api chunks the documents and indexes them to the vector database Qdrant"""

    #placeholder code
    return {"document_id": id}

@app.get("/v1/search")
async def search_document(query: str):
    """Searches the relevant documents from the vector database Qdrant"""

    #placeholder code
    return {"query": query}

