from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
load_dotenv()

llm = ChatGroq(
    model = "openai/gpt-oss-20b",
)

search = GoogleSerperAPIWrapper()

memory = MemorySaver()

agent = create_agent(
    model = llm,
    tools = [search.run],
    checkpointer = memory,
    system_prompt = "you are a helpful agent search for any question on google"
)

while True:
    query = input("user: ")

    if query.lower() in ["quit", "bye", "exit"]: 
        print("GoodBye😊")
        break
      
    res = agent.invoke(
        {
           "messages":[
              {
                 'role':'user',
                 'content':query
              }
            ]
        },
        {
            'configurable':{'thread_id':'1'}    
        }
    )
    print("AI: ",res['messages'][-1].content , "\n")