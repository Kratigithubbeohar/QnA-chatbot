from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid mathematical expression"

llm = ChatOllama(
    model = "qwen2.5:3b",
)

agent = create_agent(
    model = llm,
    tools = [calculator]
)

while True:
    query = input("user: ")

    if query.lower() in ["quit", "bye", "exit"]: 
        print("GoodBye😊")
        break
      
    res = agent.invoke({
        "messages":[
           {
            'role':'user',
            'content':query
           }
        ]
    })
    print("AI: ",res['messages'][-1].content , "\n")