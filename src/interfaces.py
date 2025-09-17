from abc import ABC, abstractmethod
from typing import Any


from src.schemas import AccumulatedOutput


class ToolInterface(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        raise NotImplementedError("Tool execution not implemented")


class LLMProviderInterface(ABC):
    @abstractmethod
    def __init__(self, model_name: str, client):
        raise NotImplementedError("LLM provider instantiation not implemented")

    @abstractmethod
    def completion(self, input_list: list[dict]) -> str:
        """Generate a completion for the given input list"""
        raise NotImplementedError("LLM completion not implemented")

    @abstractmethod
    def thinking_completion(self, input_list: list[dict]) -> AccumulatedOutput:
        """Generate a thinking completion for the given input list"""
        raise NotImplementedError("LLM thinking completion not implemented")