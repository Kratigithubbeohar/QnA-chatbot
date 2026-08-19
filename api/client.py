import requests
import streamlit as st

def get_chatGroq_response(input_text):
    response = requests.post('http://localhost:3030/essay/invoke',
                json ={'input':input_text})
    return response.json()['output']

# def get_ollama_response(input_text):
    response = requests.post('http://localhost:3030/poem/invoke',
                json ={'input':input_text})
    return response.json()['output']

st.title("langchain demo chatbot🌻")
input_text = st.text_input("write an essay on")
# input_text1 = st.text_input("write a poem on")

if input_text:
    st.write(get_chatGroq_response({'topic':input_text}))

# if input_text:
#     st.write(get_ollama_response({'topic':input_text}))    
