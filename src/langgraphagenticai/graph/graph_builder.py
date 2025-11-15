from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatBotNode
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
        self.basic_chatbot_node=BasicChatbotNode(self.llm)
        
        self.graph_builder.add_node("chatbot","")
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)
    
    def setup_graph(self,usecase:str):
       """
       Sets up the graph for the selected use case.
       """
       if usecase=="Basic Chatbot":
           self.basic_chatbot_build_graph(usecase)
        
        return self.graph_builder.compile()