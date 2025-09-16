import json

from openai import AsyncOpenAI as AsyncOpenAIClient

from src.config import settings
from src.interfaces import LLMProviderInterface, ToolInterface
from src.schemas import AccumulatedOutput, Output
from src.utils import format_tool_list

client = AsyncOpenAIClient(api_key=settings.openai_api_key)


class OpenAIProvider(LLMProviderInterface):
    def __init__(
        self, model_name: str, client: AsyncOpenAIClient = client
    ) -> AccumulatedOutput:
        self.model_name = model_name
        self.client = client

    async def completion(self):
        pass

    async def thinking_completion(
        self,
        input_list: list[dict],
        tools: list[ToolInterface] | None = None,
        max_iterations: int = 5,
    ) -> AccumulatedOutput:
        if tools:
            input_tools = format_tool_list(tools)
        else:
            input_tools = None 

        thinking = True
        iteration = 1
        accumulated_output = []
        while thinking and iteration <= max_iterations:
            assistant_messages = []
            function_calls = []
            function_call_output = None

            response = await self.client.responses.create(
                model=self.model_name, input=input_list, tools=input_tools
            )

            input_list += response.output
            for item in response.output:
                if getattr(item, "type", None) == "message":
                    contents = getattr(item, "content", []) or []

                    for content in contents:
                        ctype = getattr(content, "type", None)
                        if ctype in ("output_text", "text"):
                            assistant_message = getattr(content, "text", "")
                            if assistant_message != "completed":
                                assistant_messages.append(assistant_message)
                            else:
                                thinking = False

                if getattr(item, "type", None) == "function_call":
                    function_calls.append(item)
                    for tool in tools:
                        if tool.name == item.name:
                            function_call_output = tool.execute(
                                json.loads(item.arguments)
                            )
                            input_list.append(
                                {
                                    "type": "function_call_output",
                                    "call_id": item.call_id,
                                    "output": json.dumps(
                                        {f"{tool.name}_output": function_call_output}
                                    ),
                                }
                            )

            output = Output(
                iteration=iteration,
                assistant_messages=assistant_messages,
                function_calls=function_calls,
                function_call_output=function_call_output,
            )
            iteration += 1
            accumulated_output.append(output)

        return AccumulatedOutput(output=accumulated_output)
