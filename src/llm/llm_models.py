"""Shared Pydantic AI model configuration.

The application runs on GPT 5.5 served through OpenAI's Responses API with a
medium reasoning effort. Both the planning and speaking agents reuse the same
model instance and settings defined here.
"""

from pydantic_ai.models.openai import (
    OpenAIResponsesModel,
    OpenAIResponsesModelSettings,
)
from pydantic_ai.providers.openai import OpenAIProvider

from src.config import settings

MODEL_NAME = "gpt-5.5"

openai_provider = OpenAIProvider(api_key=settings.openai_api_key)

gpt_5_5 = OpenAIResponsesModel(MODEL_NAME, provider=openai_provider)

medium_reasoning_settings = OpenAIResponsesModelSettings(
    openai_reasoning_effort="medium",
)
