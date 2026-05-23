
# Week 3 Class 2 - Structured + Guardrails AI Assistant + RAG

import os, json
from openai import OpenAI
from pypdf import PdfReader
import numpy as np 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "KB_Errors_Simple.pdf"

# Step 1 : Setup Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# TODO: input
topic = input("Enter Error : ")
try:
    temp = float(input("Temperature: "))
    if not (0.2 <= temp <= 0.8):
        print("Temperature shoud be etween 0.2 and 1.0, setting it to 0.5")
except ValueError:
    print("Invalid Input, setting it to 0.5")
    temp=0.5


def run_prompt(prompt):
    # TODO: structured prompt
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

# Step 2: Load PDF

def load_pdf_text(file_path):
    reader = PdfReader(str(file_path))
    full_text = ""

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text :
            full_text+= f"\n ---- Page {page_num} ---\n{text}\n"

    return full_text

# Step 3: Chunking

def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0,len(text),chunk_size):
        chunk = text [i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)
        
    return chunks 

# Step 4: Create embeddings
# converting the chunks into embedding - critical step 

def get_embedding(text):
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = text
    )

    return response.data[0].embedding

# Step 5: cosine similarity  -1 -> 1
def cosine_similarity(a,b):
    a=np.array(a, dtype=float)
    b=np.array(b, dtype=float) 

    return float(np.dot(a,b) / np.linalg.norm(a) * np.linalg.norm(b))

# Step 6 - Build Vector Store

def build_vector_store(chunks):
    vector_store =[]

    for i,chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        vector_store.append({
            "chunk_id": i,
            "text": chunk,
            "embedding": emb
        })

    return vector_store 

# Step 7 - Semantic Search

def semantic_search(query,vector_store,k=3):
    query_embedding = get_embedding(query)

    score_results = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        score_results.append({
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "score":score 
     
        })

    score_results.sort(key=lambda x: x["score"], reverse=True)

    return score_results[:k] # return the top-k results



# Step 8: RAG Answer
def rag_answer(question,vector_store,k=3):
    top_chunks = semantic_search(question,vector_store,k=k)

    context = "\n\n".join([item['text'] for item in top_chunks])

    prompt = f"""
Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

Constraints:
- keep it under 150 words

Rules:
- Return the output strictly in JSON format with sections and bullet points
- Must be beginner-friendly
- No jargon, keep it simple
- Write a concise summary in bullet points

If answer is not in context, say "I dont know"
"""
    response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.0
)
    
    return response.choices[0].message.content , top_chunks

def better_improve_answer(answer):
    # This function takes an answer and prompts the model to rewrite it in a more structured, professional, and beginner-friendly way, while keeping it concise. 
    # The output is expected to be in JSON format with sections and bullet points for easy scanning.
    return run_prompt(f"""
Explain {topic}.

Constraints:
- keep it under 150 words

Rules:
- Return the output strictly in JSON format with sections and bullet points
- Must be beginner-friendly
- No jargon, keep it simple
- Write a concise summary in bullet points

Answer:
{answer}
"""
)


def clean_output(output):
    # Remove code block markers if present
    output=output.strip()

    if output.startswith("```json"):
        print("inside if block")
        output=output[len("```json"):].strip()
    
    if output.endswith("```"):
        print("Inside else part")
        code_marker="```"
        end_index = len(output) - len(code_marker)
        output=output[:end_index].strip()

    return output

def refine_until_good(answer, iterations=3):
    # this function takes an initia answer and refins it iteratively for a given number if times.
    for i in range(iterations):
        print(f"Refinement iteration {i+1}")
        answer = better_improve_answer(answer)
    return answer

    
print("Loading PDF.....")
pdf_text = load_pdf_text(PDF_PATH)

print("\n Chunking Text....")
chunks =chunk_text(pdf_text, chunk_size=500)
print(f"Total chunks created: {len(chunks)}")

print("\n Building the vector store .........")
vector_store = build_vector_store(chunks)


print(f"\nSemantic Search query: {topic}")

results =  semantic_search(topic,vector_store,k=2)

print("\n top Matching chunks: ")
for r in results:
    print(f"ChunkID : {r['chunk_id']}")
    print(f"Similarity score : {r['score']}")
    print(r['text'][:500])


print("\n Final Answer: ")



try:
    answer,sources = rag_answer(topic,vector_store,k=3)
    print(answer)
    refined_output = refine_until_good(answer)
    cleaned_data = clean_output(refined_output.choices[0].message.content)
    json_data = json.loads(cleaned_data)
    print(json.dumps(json_data, indent=4))
except json.JSONDecodeError:
    print("Invalid Json")

print("\nSource chunks used ")
for s in sources:
    print(f"ChunkID:{s['chunk_id']} | Score : {s['score']} ")
    print(s['text'][:300])

# # print(response.choices[0].message.content)
# print(f"Completion_Tokens : {refined_output.usage.completion_tokens}")
# print(f"Prompt_Tokens : {refined_output.usage.prompt_tokens}")
# print(f"Total_Tokens : {refined_output.usage.total_tokens}")
