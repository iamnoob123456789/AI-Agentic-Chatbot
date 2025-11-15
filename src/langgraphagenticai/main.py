import streamlit as st
from typing import Dict, Any, Optional

from langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder


def load_langgraph_agentic_app() -> None:
    """
    Main function to load and run the LangGraph Agentic application.
    Handles UI setup, user input, and graph execution.
    """
    # Initialize the Streamlit UI
    ui = LoadStreamlitUI()
    user_input = ui.load_ui()

    if not user_input:
        st.error("Error: Failed to load user input")
        return

    # Get user message from chat input
    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            # Configure the LLM
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM Model could not be initialized")
                return

            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No use case selected")
                return

            # Initialize and build the graph
            graph_builder = GraphBuilder(model=model)
            try:
                # Get the compiled graph
                graph = graph_builder.setup_graph(usecase)
                
                # Execute the graph with the user's message
                if graph:
                    # Assuming the graph expects a state dictionary with a 'messages' key
                    result = graph.invoke({"messages": [{"role": "user", "content": user_message}]})
                    
                    # Display the result (adjust based on your graph's output structure)
                    if result and "messages" in result:
                        for msg in result["messages"]:
                            if msg.role == "assistant":
                                st.chat_message("assistant").write(msg.content)
                    else:
                        st.error("Error: Invalid response from the model")
                
            except Exception as e:
                st.error(f"Error setting up or executing graph: {str(e)}")
                st.exception(e)  # This will show the full traceback in the UI
                return

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            st.exception(e)  # This will show the full traceback in the UI