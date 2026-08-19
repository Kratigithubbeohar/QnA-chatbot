import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
## ChatPromptTemplate helps to create chatbot
from langchain_core.prompts import ChatPromptTemplate
# help to customize output
from langchain_core.output_parsers import StrOutputParser
import streamlit as st

# apiKey = os.getenv['GROQ_API_KEY']

prompts = ChatPromptTemplate(
    {
        ("system","you are a helpful assistant. Please response to the user queries"),
        ('user','Question:{question}')
    }
)

st.title("langchain demo chatbot🌻")
input_text = st.text_input("search the topic you want")

llm = ChatGroq(
    model = 'openai/gpt-oss-20b'
)
output_parser = StrOutputParser()
chain = prompts | llm | output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))