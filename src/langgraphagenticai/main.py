import streamlit as st
from langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI

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
            obj_llm_config=GroqLLMConfig(user_controls_input=user_input)
            model=obj_llm_config.get_llm_model()
            
        