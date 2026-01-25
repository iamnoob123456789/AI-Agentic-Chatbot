import streamlit as st
from pathlib import Path
import sqlite3
from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.callbacks import StreamlitCallbackHandler   # Correct for 0.2.x

from langchain_groq import ChatGroq

st.set_page_config(page_title="LangChain: Chat with SQL DB", page_icon="🦜")
st.title("🦜 LangChain: Chat with SQL DB")

# Constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_opt = [
    "Use SQLite 3 Database - student.db",
    "Connect to your MySQL Database"
]

selected_opt = st.sidebar.radio(
    label="Choose the Database you want to chat with",
    options=radio_opt
)

db_uri = LOCALDB
mysql_host = mysql_user = mysql_password = mysql_db = None

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host")
    mysql_user = st.sidebar.text_input("MySQL User")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database Name")

api_key = st.sidebar.text_input("Grok API Key", type="password")

if not api_key:
    st.warning("Please provide your Groq API key to continue.")
    st.stop()

if db_uri == MYSQL and not all([mysql_host, mysql_user, mysql_password, mysql_db]):
    st.warning("Please fill in all MySQL connection details.")
    st.stop()

# LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant",
    streaming=True,
    temperature=0.7
)

@st.cache_resource(ttl="2h")
def get_db_connection(_db_uri, _host=None, _user=None, _pass=None, _db_name=None):
    if _db_uri == LOCALDB:
        db_path = (Path(__file__).parent / "student.db").absolute()
        st.write(f"Using local database: {db_path}")
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        engine = create_engine("sqlite:///", creator=creator)
        return SQLDatabase(engine)
    
    else:  # MySQL
        connection_string = f"mysql+mysqlconnector://{_user}:{_pass}@{_host}/{_db_name}"
        engine = create_engine(connection_string)
        return SQLDatabase(engine)

db = get_db_connection(
    db_uri,
    mysql_host,
    mysql_user,
    mysql_password,
    mysql_db
)

# Create toolkit and agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="zero-shot-react-description",   # string is correct in 0.2.x
    handle_parsing_errors=True                  # recommended in 0.2.x
)

# Chat history
if "messages" not in st.session_state or st.sidebar.button("Clear Chat History"):
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me anything about the database 😊"}]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about the database..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                streamlit_callback = StreamlitCallbackHandler(st.container())
                response = agent_executor.run(
                    input=prompt,
                    callbacks=[streamlit_callback]
                )
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})