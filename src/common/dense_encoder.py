from openai import OpenAI

from src.config import settings

openai_client = OpenAI(api_key=settings.openai_api_key)


def encode(text: str) -> list[float]:
    """Encode a text input into a dense embedding using OpenAI's latest embedding model."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
        encoding_format="float",
    )
    return response.data[0].embedding
