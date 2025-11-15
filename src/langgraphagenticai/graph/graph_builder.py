from typing import Any, Dict, Optional
from langgraph.graph import StateGraph, START, END
from langchain_core.language_models.base import BaseLanguageModel

from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatBotNode

class GraphBuilder:
    def __init__(self, llm: Optional[BaseLanguageModel] = None):
        """Initialize the GraphBuilder with an optional LLM.
        
        Args:
            llm: The language model to use for the graph nodes.
        """
        self.llm = llm
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_build_graph(self) -> StateGraph:
        """
        Builds a basic chatbot using LangGraph.
        This method initializes a chatbot node using the BasicChatBotNode class.
        
        Returns:
            StateGraph: The configured state graph for the chatbot.
        """
        if not self.llm:
            raise ValueError("LLM is required to build the chatbot graph")
            
        # Initialize the chatbot node
        self.basic_chatbot_node = BasicChatBotNode(self.llm)
        
        # Add node with the actual node function
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        
        # Define the graph edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
        return self.graph_builder.compile()
    
    def setup_graph(self, usecase: str) -> Any:
        """
        Sets up the graph for the selected use case.
        
        Args:
            usecase: The use case to set up the graph for.
            
        Returns:
            The compiled graph for the specified use case.
            
        Raises:
            ValueError: If the specified use case is not supported.
        """
        if usecase == "Basic Chatbot":
            return self.basic_chatbot_build_graph()
        else:
            raise ValueError(f"Unsupported use case: {usecase}")