from pydantic import BaseModel

class BlogState(BaseModel):
    #uper input
    topic:str = ""
    audience:str=''
   ##reasearcher output
    research:str =''
    research_feedback:str=""
   ##writer o/p
    draf:str=''
    draft_feedback:str=''
   # editor o/p
    final_blog : str =""

   # metadata
    revision_count=int = 0