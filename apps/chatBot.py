from langchain_ollama import ChatOllama
import streamlit as st

llm = ChatOllama(
    model = "qwen2.5:3b",
)

st.title("AskBuddy🤖")
st.markdown("Q&A Bot with LangChain and Ollama")

#messages is a type of key will store at the storage of session 

if "messages" not in st.session_state:
  st.session_state.messages=[]

for message in st.session_state.messages:
   role = message['role']
   content = message['content']
   st.chat_message(role).markdown(content)

query  = st.chat_input("Ask anything?")

if query:
    st.session_state.messages.append({'role':'user','content':query})
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content)
    ## store the history of message in a session
    st.session_state.messages.append({'role':'ai','content':res.content})