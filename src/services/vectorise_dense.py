from openai import AsyncOpenAI

from src.config import settings
from typing import Union
from logger import logging 
import asyncio 

openai_client = AsyncOpenAI(api_key=settings.openai_api_key)

class DenseVector:
    def __init__(self, client: Union[AsyncOpenAI]):
        self.client = client

    async def run(self, input_text: str):
        response = await self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=input_text,
            encoding_format="float"
        )

        return response.data[0].embedding

if __name__=="__main__":
    dense_vector_pipeline = DenseVector(client=openai_client)
    embedding = asyncio.run(dense_vector_pipeline.run(input_text="This is a sample text"))
    logging.info(embedding)