import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# get LLM
def get_llm(model_name:str="openai/gpt-oss-20b", temperature :float=0.5):
    api_key = os.getenv('GROQ_API_KEY')
    llm = ChatGroq(model=model_name, temperature= temperature, api_key=api_key)
    return llm


# research agent
RESEARCHER_PROMPT = ChatPromptTemplate.from_messages({
    {'role': 'system', 'content': """   
         "you are  a Research Agent. Given a blog topic and target audience, produce a clear,"
         "1. 5-7 key points the blog should cover\n"
         "2. Important facts, starts, or examples for each point\n"
         "3. Suggested angle or hook\n"
         "Be concise. Use bullet points. Do not write the full blog yet."
    """},
    {'role':'user', "content":'Topic:{topic}, Audience:{audience},{revision_hints},wite the research outline now.'}
})

# researcher agent

def researcher_agent(llm:ChatGroq, topic:str, audienece:str, feedback:str = ""):
    revision_hints = f"the human provided this feedback on your previous research - please address it:{feedback}"
    if not feedback:
        revision_hints='this is your first attempt'

    chain = RESEARCHER_PROMPT | llm
    result = chain.invoke({
        'topic':topic,
        'audience':audienece,
        "revision_hints":revision_hints
    })  
    return result.content  

WRITER_PROMPT = ChatPromptTemplate.from_messages([
    {'role': 'system', 'content': """   
             "you are  a blog writer Agent.Using the research notes, write a complete,"
             "engaging blog post.\n"
             "-length 500-
        """},
        {'role':'user', "content":'Topic:{topic}, Audience:{audience},{revision_hints},wite the research outline now.'}
])