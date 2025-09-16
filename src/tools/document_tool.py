from pydantic import BaseModel, Field
from src.interfaces import ToolInterface 

class DocumentToolInputSchema(BaseModel):  
    query: str = Field(title="User Search Query", description="The query to search the document for")

class DocumentTool(ToolInterface): 
    name = "document_search_tool"
    description = "Search a document for content matching a query."
    input_schema = DocumentToolInputSchema 

    @staticmethod
    def execute(query: DocumentToolInputSchema):
        return {
            "tool_name": DocumentTool.name,
            "tool_description": DocumentTool.description, 
            "tool_output": {
                "address": "71/38 Shoreline Dr, Rhodes",
                "building_type": "Townhouse",
                "purchase_price ($)": "1500000",
                "purchase_date": "2025-09-23"
            }
        }

if __name__ == "__main__":
    document_tool = DocumentTool() 
    print(DocumentTool.input_schema.model_json_schema())