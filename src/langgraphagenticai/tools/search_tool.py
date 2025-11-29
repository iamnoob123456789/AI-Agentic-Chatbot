from langchain.community.tools.tavily import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns the list of tools that are present
    """
    tools=[TavilySearchResults(max_result=2)]

    return tools

def create_tool_node(tools):
    """
    Created and returns tool node for the graph
    """

    return ToolNode(tools=tools)
