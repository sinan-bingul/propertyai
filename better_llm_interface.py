from abc import ABC, abstractmethod
from typing import Any, Optional, TypeAlias, Union

import anthropic
from openai import AsyncOpenAI, OpenAI

# Type alias for cleaner code
LLMClientType: TypeAlias = Union[
    OpenAI, AsyncOpenAI, anthropic.Anthropic, anthropic.AsyncAnthropic
]


class ToolInterface(ABC):
    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        raise NotImplementedError("Tool execution not implemented")


class LLMInterface(ABC):
    """Abstract interface for LLM implementations"""

    # Type hint for client that supports multiple LLM providers
    client: LLMClientType
    model_name: str

    def __init__(self, client: LLMClientType, model_name: str):
        self.client = client
        self.model_name = model_name

    @abstractmethod
    def completion(
        self, query: str, tools: Optional[list[ToolInterface]] = None
    ) -> str:
        """Generate a completion for the given query"""
        raise NotImplementedError("LLM completion method not implemented")

    @abstractmethod
    async def async_completion(
        self, query: str, tools: Optional[list[ToolInterface]] = None
    ) -> str:
        """Generate an async completion for the given query"""
        raise NotImplementedError("LLM async completion method not implemented")

    @abstractmethod
    def stream(self, query: str, tools: Optional[list[ToolInterface]] = None):
        """Stream completion tokens"""
        raise NotImplementedError("LLM streaming not implemented")


class OpenAILLM(LLMInterface):
    """OpenAI implementation of LLM interface"""

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        client = OpenAI(api_key=api_key)
        super().__init__(client, model_name)

    def completion(
        self, query: str, tools: Optional[list[ToolInterface]] = None
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name, messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

    async def async_completion(
        self, query: str, tools: Optional[list[ToolInterface]] = None
    ) -> str:
        # Would need AsyncOpenAI client for this
        pass

    def stream(self, query: str, tools: Optional[list[ToolInterface]] = None):
        stream = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": query}],
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content


class AnthropicLLM(LLMInterface):
    """Anthropic implementation of LLM interface"""

    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        client = anthropic.Anthropic(api_key=api_key)
        super().__init__(client, model_name)

    def completion(
        self, query: str, tools: Optional[list[ToolInterface]] = None
    ) -> str:
        response = self.client.completions.create(
            model=self.model_name,
            prompt=f"Human: {query}\n\nAssistant:",
            max_tokens_to_sample=1000,
        )
        return response.completion

    async def async_completion(
        self, query: str, tools: Optional[list[ToolInterface]] = None
    ) -> str:
        # Would need AsyncAnthropic client for this
        pass

    def stream(self, query: str, tools: Optional[list[ToolInterface]] = None):
        stream = self.client.completions.create(
            model=self.model_name,
            prompt=f"Human: {query}\n\nAssistant:",
            max_tokens_to_sample=1000,
            stream=True,
        )
        for completion in stream:
            yield completion.completion


# Factory function for creating LLM instances
def create_llm(
    provider: str, api_key: str, model_name: Optional[str] = None
) -> LLMInterface:
    """Factory function to create LLM instances"""
    if provider.lower() == "openai":
        return OpenAILLM(api_key, model_name or "gpt-3.5-turbo")
    elif provider.lower() == "anthropic":
        return AnthropicLLM(api_key, model_name or "claude-3-sonnet-20240229")
    else:
        raise ValueError(f"Unsupported provider: {provider}")


# Usage example
if __name__ == "__main__":
    # Create different LLM instances
    openai_llm = create_llm("openai", "your-openai-key")
    anthropic_llm = create_llm("anthropic", "your-anthropic-key")

    # Both satisfy the LLMInterface type
    def process_with_llm(llm: LLMInterface, query: str):
        return llm.completion(query)

    # Type checker knows both are valid LLMInterface implementations
    result1 = process_with_llm(openai_llm, "Hello, world!")
    result2 = process_with_llm(anthropic_llm, "Hello, world!")
