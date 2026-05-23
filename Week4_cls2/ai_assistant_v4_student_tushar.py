
# Week 3 Class 2 - Structured + Guardrails AI Assistant + RAG

import os, json,sys
from openai import OpenAI
from pypdf import PdfReader
import numpy as np 
from pathlib import Path 

import ai_assistant_v3_student_tushar as sm 

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "ThinkPythonAI_Demo_Company_Policies.pdf"

# Step 1 : Setup Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 2: JSON Cleanup

def clean_json_output(output):
    output = output.strip()

    if output.startswith("```json"):
        output = output[len("```json"):].strip()
    elif output.startswith("```"):
        output = output[len("```"):].strip()

    if output.endswith(("```")):
        output = output[:3].strip()

    return output 

def get_input():
    topic = input("Enter the quetion/query : ")
    try:
        temp = float(input("Temperature (0.2 - 0.8, default 0.5):  "))
        if not (0.2 <= temp <= 0.8):
            print("Temperature shoud between 0.2 and 1.0, setting it to 0.5")
            temp = 0.5
    except ValueError:
        print("Invalid Input, setting it to 0.5")
        temp=0.5
    return topic,temp

def run_prompt(prompt,temp):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a senior devops engineer, Return the output strictly in JSON format"},
            {"role":"user","content":prompt}
        ],
        temperature=temp,
        max_tokens=500,
    )
    return response

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


def agentic_rag_support(user_request, vector_store,k=3):
    plan = create_plan(user_request) # creates the plan using LLM 

    query = " ".join(plan["knowledge_needed"]) 
    retrieved = sm.semantic_search(query,vector_store,k=k)  # what knowledge we need based on that we RAG

    decison = make_descision(user_request, plan, retrieved) # decision LLM reasons over that context

    return { 
        "plan": plan,
        "retrieved": retrieved,
        "decision": decison
    }
    
def main():
    if not PDF_PATH.exists():
        print(f"PDF file not found at: {PDF_PATH}")
        
    # 1. Load PDF Text
    print("Ingesting policy documents...")
    raw_test = sm.load_pdf_text(PDF_PATH)
    
    # 2. Chunk Text
    chunk = sm.chunk_text(raw_test, chunk_size=500)
    
    # 3. Create embedding/cosine similarty/build vector store
    vector_store = sm.build_vector_store(chunk)
    print(f"Vector store ready with {len(vector_store)} chunks. \n")
    
    query,temp = get_input()
    
    result = agentic_rag_support(query,vector_store,k=3)
    
    print("\n====================PLAN==================")
    print(json.dumps(result["plan"],indent=2))

    print("\n====================RETRIEVED==================")
    print(json.dumps(result["retrieved"],indent=2))

    print("\n====================DECISION==================")
    print(json.dumps(result["decision"],indent=2))

    print("\n====================CUSTOMER RESPONSE==================")
    print(json.dumps(result["decision"]["customer_reply"]))

if __name__ == "__main__":
    main()
