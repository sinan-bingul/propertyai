import os

from openai import AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()

_client: AsyncOpenAI | None = None


def get_openai_client() -> AsyncOpenAI:
    """Return the async OpenAI client, creating it once and reusing it."""
    global _client
    if _client is not None:
        return _client
    _client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _client


async def get_openai_response(prompt: str) -> str:
    """Make a GPT-5.5 Responses API call with reasoning disabled."""
    client = get_openai_client()
    response = await client.responses.create(
        model="gpt-5.5",
        input=prompt,
        reasoning={"effort": "none"},
    )
    return response.output_text
