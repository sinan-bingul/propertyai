from src.interfaces import ToolInterface

def format_tool_list(tool_list: list[ToolInterface]):
    tool_json_list = []
    for tool in tool_list:
        tool_name = tool.name
        tool_description = tool.description
        parameters = tool.input_schema.model_json_schema()
        parameters["additionalProperties"] = False
        tool_json = {
            "type": "function",
            "name": tool_name,
            "description": tool_description,
            "strict": True,
            "parameters": parameters,
        }
        tool_json_list.append(tool_json)
    return tool_json_list