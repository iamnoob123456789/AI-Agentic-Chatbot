import streamlit as st
from typing import Dict, Any
from langgraphagenticai.ui.streamlitui.uiconfigfile import Config

class LoadStreamlitUI:
    def __init__(self) -> None:
        self.config = Config()
        self.user_controls: Dict[str, Any] = {}

    def load_ui(self) -> Dict[str, Any]:
        """
        Load and render the Streamlit UI components.
        
        Returns:
            Dict[str, Any]: Dictionary containing user selections and inputs
        """
        st.set_page_config(
            page_title=self.config.get_page_title(),
            layout="wide"
        )
        st.header(self.config.get_page_title())

        with st.sidebar:
            llm_options = self.config.get_llm_options()
            use_case_options = self.config.get_usecase_options()
            
            # LLM Selection 
            self.user_controls["selected_llm"] = st.selectbox("Select LLM", llm_options)

            if self.user_controls["selected_llm"] == 'Groq':
                # Model Selection for Groq
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select Model", 
                    model_options
                )
                
                # API Key Input
                self.user_controls["GROQ_API_KEY"] = st.text_input(
                    "API Key", 
                    type="password",
                    help="Enter your Groq API key"
                )
                
                # Store in session state
                st.session_state["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"]
                
                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.error("Please enter a valid Groq API key")
            
            # Use Case Selection
            self.user_controls["selected_usecase"] = st.selectbox(
                "Select Use Case", 
                use_case_options
            )
            if self.user_controls["selected_usecase"]=="Chatbot with Web":
                self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY API KEY",type="password")
            if not self.user_controls["TAVILY_API_KEY"]:
                st.error("Please enter a valid Tavily API key")

        return self.user_controls
