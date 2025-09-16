from src.interfaces import LLMProviderInterface, ToolInterface
from src.schemas import AccumulatedOutput


class PlanningAgent:
    def __init__(self, system_prompt: str, llm_model: LLMProviderInterface, tool_list: list[ToolInterface]):
        self.system_prompt = system_prompt
        self.llm_model = llm_model
        self.tool_list = tool_list

    async def run(self, query: str) -> AccumulatedOutput:
        input_list = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query},
        ]
        
        response = await self.llm_model.thinking_completion(input_list, self.tool_list)
        
        return response