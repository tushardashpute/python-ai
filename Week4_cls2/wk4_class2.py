'''
Lets build an agent that can plan what knowledge it needs,retrieve it, and reason over it.

AGENTIC RAG System: Planner + Retrieval + Tools + json output(pydantic)
so lets combine RAG today 

LLM is doing multiple intellignent jobs - 
1. classifies the request
2. decides what knowledge is needed
3. user retrieval
4. reasons over context
5. returns structure decision
6. final answer 

step 1 - knowledge base 
step 2 - Planner LLM returns JSON - the planner here isnt just a thinker, its a router.
LLM planner is the one to decide "Does this need knowledge? " or simply it can just answer.
benefit - saves tokens(money) and reduces latency. 
Step 3: RAG retrieval tool. this is where we use week 3 semantic search.
Step 4: Decision LLM with retrieved context 
Final output


A chatbot just answers the questions, if it doesnt find - it says the else case.
An Agentic RAG system investigates, retrieves then, reasons, and then finally responds.

'''

import json
from pathlib import Path 
import numpy as np # for vector math 
from pypdf import PdfReader
from openai import OpenAI
import time 

client = OpenAI()

# Step 1 - file path
BASE_DIR = Path(__file__).resolve().parent 
PDF_PATH = BASE_DIR / "ThinkPythonAI_Demo_Company_Policies.pdf"

# Step 2 : JSON Cleanup 

def clean_json_output(output):
    output = output.strip()

    if output.startswith("```json"):
        output = output[len("```json"):].strip()
    elif output.startswith("```"):
        output = output[len("```"):].strip()

    if output.endswith(("```")):
        output = output[:3].strip()

    return output 


# Step 3 : Load PDF Text 

def load_pdf_text(file_path):
    reader = PdfReader(str(file_path))

    full_text = ""
    for page_num, page in enumerate(reader.pages,start=1):
        text = page.extract_text()
        if text: 
            full_text+= f"\n ---PAGE {page_num} ---\n{text}\n"

    return full_text

# Step 4 : chunk text 

def chunk_text(text,chunk_size=500):
    chunks = []

    for i in range(0,len(text),chunk_size):
        chunk = text [i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)

    return chunks 

# Step 5 : Create embedding

def get_embedding(text):
    response = client.embeddings.create(

        model = "text-embedding-3-small",
        input = text
    )
    return response.data[0].embedding


# Step 6: Cosine similarity 

def cosine_similarity(a,b):
    a=np.array(a,dtype=float)
    b=np.array(b,dtype=float)

    return float(np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))) 

# higher score means more similar meaning. 
# Search is no longer matching the words/text but it is not measuring the closeness in meaning space.

# Step 7: Build vector store

def build_pdf_vector_store(pdf_path, chunk_size=500):
    pdf_text = load_pdf_text(pdf_path)
    chunks = chunk_text(pdf_text,chunk_size=chunk_size)

    vector_store = []

    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        vector_store.append({
            "chunk_id": i,
            "source":pdf_path.name,
            "text": chunk,
            "embedding": emb
        })

    return vector_store


# Step 8: Semantic retrieval

def retrieval_policies(query,vector_store,k=3):
    query_embedding = get_embedding(query)
    scored_results = []

    for item in vector_store:
        score=cosine_similarity(query_embedding, item["embedding"])
        scored_results.append({
            "chunk_id": item["chunk_id"],
            "source":item['source'],
            "text": item["text"],
            "score":round(score,4) 
        })

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return scored_results[:k]

# Step 9: Planner LLM

def create_plan(user_request):
    prompt = f"""

You are an AI support operations planner.

Analyze the customer request and return ONLY valid JSON.
Do not use markdown fences.
Do not add explanations before or after the JSON.

Customer Request:
{user_request}

Return JSON with exactly this schema:
{{
"issue_type": "refund_case | damage_case | refund_damage_case | general_case",
"knowledge_needed" : ["string","string"],
"reason": "string"
}}

"""
    
    response = client.chat.completions.create(

        model="gpt-4o-mini",
        messages= [ { "role":"user","content": prompt}],
        temperature=0.0
    )
    
    raw_output = response.choices[0].message.content
    print("Plan RAW output: ")
    print(raw_output)

    cleaned = clean_json_output(raw_output)
    return json.loads(cleaned)



# we are acting the LLM to act as a "router".  if -else part, if it decides its needs knowledge, we trigger the RAG. This is the router mode, and is helpful in saving costs as we dont want to search the whole PDF for simple questions/user like "Hello".


# Step 10 : Decision LLM
def make_descision(user_request, plan, retrieved_context):

    prompt = f"""

You are an AI support descision agent.

Use ONLY the retrieved policy context below.

Customer request:
{user_request}

Plan:
{json.dumps(plan, indent =2)}

Retrieved policies:
{json.dumps(retrieved_context, indent =2)}

Return ONLY valid JSON.
Do not use markdown fences.
Do not add explanations before or after the JSON.

Return JSON with exactly this schema:
{{
"eligible": true or false,
"recommended_action" : "short action",
"reasoning" : "brief reasoning",
"sources_used" : ["source names"],
"customer_reply" : "polite customer-facing message"
}}
"""

    response =client.chat.completions.create(
        model = "gpt-4o-mini", # Later change it to a faster model and see if latency improves
        messages = [{"role": "user", "content":prompt}],
        temperature=0.0
    )

    raw_output = response.choices[0].message.content 
    print("\nDecision RAW Output: ")
    print(raw_output)

    cleaned = clean_json_output(raw_output)
    return json.loads(cleaned)



# Model Tiering. - using diff models for both planning and decision phase of LLM to achive, balance on latency, accuracy, and budget.


# Step 11: Full Agentic RAG Flow
# Two - Stage Orchestration: The seperation between the planning and decision phase is the industry standard for Agentic Workflows.
# It prevents the "Single-call Hallucination" where a model tries to do "too much" at once and fails. 

def agentic_rag_support(user_request, vector_store,k=3):
    plan = create_plan(user_request) # creates the plan using LLM 

    query = " ".join(plan["knowledge_needed"]) 
    retrieved = retrieval_policies(query,vector_store,k=k)  # what knowledge we need based on that we RAG

    decison = make_descision(user_request, plan, retrieved) # decision LLM reasons over that context

    return { 
        "plan": plan,
        "retrieved": retrieved,
        "decision": decison
    }


# step 12: Run it
if __name__ == "__main__":

    print("Loading and embedding policy PDF.....")
    vector_store = build_pdf_vector_store(PDF_PATH,chunk_size=500)

    print(f"Vector store ready with {len(vector_store)} chunks. \n")

    #user_request = "A Customer wants a refund after 2 weeks and says the item was damaged."
    #user_request = "A Customer accessed a digital product and now wants a refund"
    #user_request = "A Customer is asking where their package is and says shipping is too slow"
    #user_request = "The situation is unusual and unclear. What should the support do?"
    user_request = "What is the salary of your CEO?"
    
    start_time=time.time()
    result = agentic_rag_support(user_request,vector_store,k=3)
    end_time=time.time()

    print("Latency : ", end_time-start_time,"seconds") 

    '''
    you can add the latency check - planner latency, retierval latency, dec latency, total latency
    '''

    print("\n====================PLAN==================")
    print(json.dumps(result["plan"],indent=2))

    print("\n====================RETRIEVED==================")
    print(json.dumps(result["retrieved"],indent=2))

    print("\n====================DECISION==================")
    print(json.dumps(result["decision"],indent=2))

    print("\n====================CUSTOMER RESPONSE==================")
    print(json.dumps(result["decision"]["customer_reply"]))
