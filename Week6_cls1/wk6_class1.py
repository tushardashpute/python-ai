'''
m imp mapping our wk 5 project to LangChain - then later with LangGraph.
At its core, it helps organize common LLM application patterns.
LangChain usually helps with things like: 

chaining steps together.

create_plan()
LangChain will be mapped to
prompTemplate
model call
strutures parser

build_resume_vector_store maps to

document loader
text splitter
embeddings

summarize_top_candidates()
maps to 
evaluation chain


'''

# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# prompt = ChatPromptTemplate.from_template("""
# Analyze this job description and extract a hiring plan.                                          
                                          
# Job Description:
# {job_description}
                                
                                          
# """)

# chain = prompt | llm 

# result = chain.invoke({
#     "job_description" : "We are hiring a Python Automation Engineer....."
# })

'''
prompt | llm  - creates a pipeline. this is synonmus to our manual retreieval function and orchestrator function.
.invoke - is resp for running the pipeline.

'''

# print("=========")
# print(result.content)

from typing import List
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

class ResumePlan(BaseModel):
    role_title: str 
    must_have_skills: List[str] # list of strings. can use list[str]
    nice_to_have_skills: List[str]
    reason: str 

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(ResumePlan)

prompt = ChatPromptTemplate.from_template("""
Extract a hiring plan from this job description                                         
                                          
Job Description:
{job_description}
                                                                          
""")

chain = prompt | structured_llm

plan = chain.invoke({
    "job_description" : "We are hiring a Python Automation Engineer....."
})

print("=======Pydantic==========")
print(plan)
print(plan.must_have_skills)
#['Proficiency in Python programming', 'Experience with automation frameworks', 'Knowledge of CI/CD tools', 'Familiarity with version control systems (e.g., Git)', 'Understanding of software testing methodologies']

#In langchain this is called "Observability-by-default"


print("============Retrieval============")

from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

'''
break large docs into smaller, manageable chunks.
it optimizes text for LLM context windows (huge adv), preserving semantic meaning through strucutres like RecursiveCharacterTextSplitter.
RecursiveCharacterTextSplitter
splits text based on a character, sentence, paragrpah as seperators.
CharacterTextSplitter splits on a specific character string. eg \n .
TokenTextSplitter: splits text based on tokens, ideal for adhering to specific model limits. OpenAI tiktoken
Lang - specifi splitters also - Python, markdowns or JSFrameworkTextSplitter.

chunk_size : Defines the max size of each chunk
chunk overlap: Maintains context between adjacent chunks.
create_documents: A function used to create Doc obj from split texxts, useful for building the vector DB.

'''

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

text = '''
Candidate resume text goes here......
Python,Selenium, REST API testing, automation frameworks....
'''

chunks = splitter.split_text(text)
print(chunks[:2])

vector = embeddings.embed_query(chunks[0])
print(len(vector))

'''
1536 - is not 1536 words or 1536 tokens or 1536 characters,
1536 is dimensions.

the embedding is reprsented by 1536 floating-point values.

'''

'''
Chunk 1: Python automation engineer with experience in API
Chunk 2: Validation, selenium, and     maintainable framework.....

paragrpah break
line breaks
spaces


paragraph breaks
bullet points
lines
spaces
sentences


this gives us better chunks
And better chunks means
better embeddings
better retrieval
better semantic search 
more meaningful

["\n\n" , "\n", " ", ""]
Try1 - \n\n - paragraph breaks
if good, then done
else
try 2: within paragraph - line breaks \n
else:
try 3:
if its still too large, then try spaces " "
try 4:
if even then, then split at raw character level

This progressive fallback is the main point - and is the reason called as "Recursive"
this is how you preserve the "most" meaning psossible, and do not cut randomly.


This is the main reason its often better and used for real-world RAG pipelines. LangChain.

'''


''' 
LangGraph
stateful.

create,debug, and scale prodcution -ready LLM agents that require looping, multi-agent collab, and human-in-the-loop decision-making.

State Management: LangGraph maintains a "shared state" - this is passed between nodes(funcitons that were calling LLM's)

Core peices of LangGraph:
a. State (m imp)
A shared object that moves through the graph

b. Nodes
Functions or steps inside the workflow

c. Edges
Connections between steps 

d. Conditional Edges
Branching logic based on state.


'''

from typing import TypedDict, List, Dict, Any

class HiringState(TypedDict):

    job_description: str 
    plan: Dict[str,Any]
    retrieved_chunks: List[Dict[str,Any]]
    candidate_rankings: List[Dict[str,Any]]
    shortlist: Dict[str,Any]
    evaluation_report: Dict[str,Any]


from langgraph.graph import StateGraph, END 

'''
create_plan() ---> planner node
retrieve_candidate_chunks() ---> retrieval node 
aggregate_by_candidate()  ----> ranking node
summarize_top_candidates() ----> shortlist node
eval_shortlist_with_judge() --> judge node 

A node in LangGraph is just one meaningful step in the workflow.

'''


def planner_node(state:HiringState):
    # create_plan() - you can map it to the prev class
    state["plan"] = {"role_title": "Python Automation Engineer"}
    return state # m imp in langgraph, we pass the state from one node to another.

def retrieval_node(state:HiringState):
    # retrieve_candidate_chunks()
    state["retrieved_chunks"] = [{"candidate_name": "Ananya Patel","score":0.57}]
    return state

def shortlist_node(state:HiringState):
    # summarize_top_candidates()
    state["shortlist"] = {"top_candidates": ["Ananaya Patel"]} 
    return state

def judge_node(state:HiringState):
    # eval_shortlist_with_judge()
    state["evaluation_report"] = {"overall_verdict": "Looks grounded"} 
    return state

graph = StateGraph(HiringState)
graph.add_node("planner", planner_node)
graph.add_node("retrieval", retrieval_node)
graph.add_node("shortlist", shortlist_node)
graph.add_node("judge", judge_node)

graph.set_entry_point("planner")
graph.add_edge("planner","retrieval")
graph.add_edge("retrieval","shortlist")
graph.add_edge("shortlist","judge")
graph.add_edge("judge",END)

app =graph.compile()

result = app.invoke({

    "job_description": "We are hiring a Python Automation Engineer...."
})


print("=========LangGraph===========")
print(result)