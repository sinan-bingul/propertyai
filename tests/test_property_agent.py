import asyncio

from pydantic_ai.messages import ModelRequest, ToolReturnPart
from pydantic_ai.models.test import TestModel

from src.agents.property_agent import property_agent
from src.tools.document_tool import document_search_tool


def test_document_search_tool_returns_property_details():
    result = document_search_tool(query="purchase price")
    assert result["address"] == "71/38 Shoreline Dr, Rhodes"
    assert result["purchase_price ($)"] == "1500000"


def test_property_agent_returns_text_output():
    """The agent should return the model's text output as a string."""
    with property_agent.override(model=TestModel(custom_output_text="final answer")):
        result = asyncio.run(
            property_agent.run("What is the purchase price of my property?")
        )

    assert result.output == "final answer"


def test_property_agent_calls_document_tool():
    """TestModel calls every available tool once, so the document tool's output
    should appear in the run's message history."""
    with property_agent.override(model=TestModel()):
        result = asyncio.run(property_agent.run("anything"))

    tool_returns = [
        part
        for message in result.all_messages()
        if isinstance(message, ModelRequest)
        for part in message.parts
        if isinstance(part, ToolReturnPart)
    ]

    assert any(part.tool_name == "document_search_tool" for part in tool_returns)
