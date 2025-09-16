from src.agents.planning_agent import PlanningAgent
from src.agents.speaking_agent import SpeakingAgent
from src.llm.llm_models import GPT5, GPT5_NANO
from src.prompts.prompt_store import read_prompt
from src.tools.document_tool import DocumentTool
import asyncio

class AgentOrchestrator:
    async def response(self, query: str):
        planning_agent = PlanningAgent(
            system_prompt=read_prompt("planning_agent_prompt"),
            llm_model=GPT5,
            tool_list=[DocumentTool],
        )

        speaking_agent = SpeakingAgent(
            system_prompt=read_prompt("speaking_agent_prompt"),
            llm_model=GPT5_NANO,
        )

        planning_response = await planning_agent.run(query)

        function_call_outputs = [
            response.function_call_output for response in planning_response.output
        ]
        speaking_output = await speaking_agent.run(query, function_call_outputs)
        
        return speaking_output.output[0].assistant_messages[0]


if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    print(asyncio.run(orchestrator.response("What is the purchase price of my property")))