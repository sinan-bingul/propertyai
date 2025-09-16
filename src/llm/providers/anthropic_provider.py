from src.interfaces import LLMProviderInterface


class AnthropicProvider(LLMProviderInterface):
    def __init__(self, model_name: str, client):
        pass

    def completion(self, input_list: list[dict]):
        pass
