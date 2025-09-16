from src.interfaces import LLMProviderInterface
from src.schemas import AccumulatedOutput


class SpeakingAgent:
    def __init__(self, system_prompt: str, llm_model: LLMProviderInterface):
        self.system_prompt = system_prompt
        self.llm_model = llm_model

    async def run(self, query: str, function_call_outputs: list[dict]) -> AccumulatedOutput:
        input_list = [
            {"role": "system", "content": self.system_prompt},
            {
            "role": "user",
            "content": """**Query**

            {query}

            **Tool Outputs**

            {tool_outputs}""".format(query=query, tool_outputs=function_call_outputs),
            },
        ]

        response = await self.llm_model.thinking_completion(input_list, max_iterations=1)

        return response
