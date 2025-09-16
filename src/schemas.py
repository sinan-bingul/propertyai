from pydantic import BaseModel
from typing import Any

class Output(BaseModel):
    iteration: int
    assistant_messages: list[str] = []
    function_calls: Any = None
    function_call_output: Any = None


class AccumulatedOutput(BaseModel):
    output: list[Output] = []
