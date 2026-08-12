from dotenv import load_dotenv
load_dotenv()
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
import streamlit as st

db = SQLDatabase.from_uri("sqlite:///tasks.db")

db.run("""
     CREATE TABLE IF NOT EXISTS tasks (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         title TEXT NOT NULL,
         description TEXT,
         status TEXT CHECK(status IN ('pending','completed')) DEFAULT 'pending',
         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
     );
""")

# i need llm, tools, memory, systemPrompt

# llm model we are using groq model
model = ChatGroq(
    model = 'openai/gpt-oss-20b'
)

#tools- using SQLDatabaseToolkit sql_db_query, sql_db_schema,sql_db_list_tables,sql_db_query_checker


toolkit = SQLDatabaseToolkit(db = db, llm = model)
tools = toolkit.get_tools()

#system prompt so agent coud know how to behave

system_prompt = """
You are an AI task management assistant that manages tasks stored in a SQL database.

The database contains a table called `tasks` with:
- id: integer primary key
- title: task title
- description: optional task description
- status: either 'pending' or 'completed'
- created_at: timestamp

TASK RULES:

1. CREATE
When the user asks to create or add a task:
- Extract the task title and description.
- Insert the task into the database using the sql_db_query tool.
- New tasks must have status='pending'.
- After INSERT, run a SELECT query to verify that the task was created.
- Only tell the user that the task was created after the INSERT succeeds.

Example:
User: Create a task called "Attend class on Monday" with description "Learning Gen-AI"

Execute:
INSERT INTO tasks (title, description, status)
VALUES ('Attend class on Monday', 'Learning Gen-AI', 'pending');

Then run SELECT to verify it.

2. READ
When the user asks to show/list tasks:
- Use SELECT.
- Return a maximum of 10 tasks.
- Order by created_at DESC.

3. UPDATE
When the user asks to complete a task:
- Find the task by id or title.
- Update its status to 'completed'.
- Run SELECT afterward to verify the update.

4. DELETE
When the user asks to delete a task:
- Find the task by id or title.
- Delete it using the SQL tool.
- Run SELECT afterward to verify deletion.

IMPORTANT:
- You MUST use the SQL tools to actually modify the database.
- Do not just describe the SQL query.
- Do not claim that an operation succeeded unless the SQL tool successfully executed it.
- If the user's request is missing the task title, ask for the title.

When showing multiple tasks, display them in a structured table.
"""

#agent
#this function can't be run again and again that's why we use this decorator
@st.cache_resource
def get_agent():
    agent = create_agent(
       model = model,
       tools = tools,
       checkpointer = InMemorySaver(),
       system_prompt = system_prompt
    )
    return agent

agent = get_agent()

#building the web application

st.subheader("TaskManager🪶")

if 'messages' not in st.session_state:
    st.session_state.messages=[]


for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])


prompt = st.chat_input("Ask me about your existing task or new task")

if prompt:
    st.chat_message("User: ").markdown(prompt)
    st.session_state.messages.append({'role':'user','content':prompt})
    #shows loading until content generates
    with st.chat_message("ai"):
        with st.spinner("your tasks will be load in a while..."):
            response = agent.invoke(
               {
                   "messages":[{
                      'role':'user','content':prompt
                    }]
               },
               {
                   'configurable':{'thread_id':'1'}
               }
            )
            result = response['messages'][-1].content
            st.markdown(result)
            st.session_state.messages.append({'role':'ai','content':result})