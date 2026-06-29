"""Property agent.

A single Pydantic AI agent that answers property-related queries. It gathers any
information it needs via tools (Pydantic AI manages the tool-calling loop) and
then produces the final answer for the user.
"""

from pydantic_ai import Agent

from src.llm.llm_models import gpt_5_5, medium_reasoning_settings
from src.prompts.prompt_store import read_prompt
from src.tools.document_tool import document_search_tool

property_agent = Agent(
    gpt_5_5,
    model_settings=medium_reasoning_settings,
    system_prompt=read_prompt("property_agent_prompt"),
    tools=[document_search_tool],
)
