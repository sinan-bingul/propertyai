import asyncio
from unittest.mock import AsyncMock

import pytest
from pydantic import BaseModel

from src.llm.providers.openai_provider import OpenAIProvider
from src.schemas import AccumulatedOutput, Output


class ResponseOutputText(BaseModel):
    text: str
    type: str = "output_text"


class ResponseOutputMessage(BaseModel):
    id: str
    content: list[ResponseOutputText]
    role: str = "assistant"
    type: str = "message"


class Response(BaseModel):
    id: str
    output: list[ResponseOutputMessage]


@pytest.fixture
def model_name():
    return "gpt-5"


@pytest.fixture
def client():
    openai_client = AsyncMock()
    openai_client.responses.create = AsyncMock(
        return_value=Response(
            id="1",
            output=[
                ResponseOutputMessage(
                    id="1", content=[ResponseOutputText(text="Paris")]
                )
            ],
        )
    )
    return openai_client


@pytest.fixture
def system_prompt():
    return "You are a helpful assistant."


@pytest.fixture
def user_prompt():
    return "What is the capital of France?"


class TestOpenAIProvider:
    def test_thinking_completion_without_tools(
        self, system_prompt, user_prompt, model_name, client
    ):
        provider = OpenAIProvider(model_name=model_name, client=client)
        input_list = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response = asyncio.run(
            provider.thinking_completion(input_list, max_iterations=1)
        )
        print(response)
        assert response == AccumulatedOutput(
            output=[Output(iteration=1, assistant_messages=["Paris"])]
        )
