"""Document search tool exposed to the planning agent.

Pydantic AI derives the tool name, description and JSON schema directly from the
function name, docstring and signature, so no separate interface class is needed.
"""


def document_search_tool(query: str) -> dict:
    """Search a document for content matching a query.

    Args:
        query: The query to search the document for.
    """
    return {
        "address": "71/38 Shoreline Dr, Rhodes",
        "building_type": "Townhouse",
        "purchase_price ($)": "1500000",
        "purchase_date": "2025-09-23",
    }
