from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langserve import add_routes
import uvicorn
import os
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
load_dotenv()

apiKey = os.getenv('GROQ_API_KEY')

apps = FastAPI(
    title='langchain Server',
    version = '1.0',
    descripion = 'A simple API server'
)

model = ChatGroq(
    model = 'openai/gpt-oss-20b'
)


add_routes(
    apps,
    model,
    path='/chatgroqAI'
)

llm = OllamaLLM(
      model = 'llama2'
)

prompt1 = ChatPromptTemplate.from_messages(['write me an essay about {topic} with 100 words'])
prompt2 = ChatPromptTemplate.from_messages(['write me a poen about {topic} with 100 words'])

add_routes(
    apps,
    prompt1|model,
    path = '/essay'
)
add_routes(
    apps,
    prompt2|llm,
    path = '/poem'
)

if __name__=='__main__':
    uvicorn.run(apps,host='localhost',port = 3030)