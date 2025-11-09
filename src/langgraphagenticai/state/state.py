from typing_extensions import TypedDict,list
from langgraph.graph.message import add_messages
class State(TypeDict):
    """
      Represent the structure of the state used in graph
    """
    message:Annotated[list,add_messages]