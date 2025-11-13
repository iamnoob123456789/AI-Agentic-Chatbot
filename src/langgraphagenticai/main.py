import streamlit as st
from langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graphbuilder.graphbuilder import GraphBuilder
def load_langgraph_agentic_app():
    """Load LangGraph Agentic App"""
    UI=LoadStreamlitUI()
    user_input=ui.load_ui()

    if not user_input:
       st.error("Error: Failed to load user input")
       return
    user_message=st.chat_input("Enter your message:")

    if user_message:
        try:
            #Configure the LLM
            obj_llm_config=GroqLLM(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()

            if not model:
                st.error("Error:LLM Model could not be initialised")
                return
            usecase=user_input.get("selected_usecase")

            if not usecase:
                st.error("Error: No use case selected")
                return 

            ##Graph Builder
              graph_builder=GraphBuilder(model)
              try:
                 graph=graph_builder.setup_grpah(usecase)
               except Exception as e:
                 st.error(f"Error: {str(e)}")
                 return

        except Exception as e:

        