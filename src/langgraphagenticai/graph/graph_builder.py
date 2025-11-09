from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from src.langgraphagenticai.LLms.groqllm import GroqLLM
from pyexpat import model


class GraphBuilder:
    def __init__(self):
        self.llm=model
        self.graph_builder=StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot using LangGraph
        This method initialises a chatbot node using the BasicChatBotNode class
        """
        self.graph_builder.add_node("chatbot","")
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)