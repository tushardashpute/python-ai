
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

# Input
def get_user_inputs():
    """Handles terminal input for the error topic and temperature."""
    topic = input("Enter Error Topic (e.g., 'Connection Timeout'): ")
    try:
        temp_input = input("Temperature (0.2 to 0.8, default 0.5): ")
        temp = float(temp_input) if temp_input.strip() else 0.5
        if not (0.2 <= temp <= 1.0):
            print("Temperature should be between 0.2 and 1.0. Defaulting to 0.5")
            temp = 0.5
    except ValueError:
        print("Invalid Input. Defaulting to 0.5")
        temp = 0.5
    return topic, temp

# -- Utility function ---

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
    """Reads PDF and extracts text with page markers."""
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found at: {file_path}")
    
    reader = PdfReader(str(file_path))
    full_text = ""

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text :
            full_text+= f"\n ---- Page {page_num} ---\n{text}\n"

    return full_text

# Step 3: Chunking

def chunk_text(text, chunk_size=500):
    """Splits long text into smaller overlapping segments."""
    chunks = []
    for i in range(0,len(text),chunk_size):
        chunk = text [i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)     
    return chunks 

# Step 4: Create embeddings
# converting the chunks into embedding - critical step 

def get_embedding(text):
    """Generates vector embeddings using OpenAI's latest model."""
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = text
    )
    return response.data[0].embedding

# Step 5: cosine similarity  -1 -> 1
def cosine_similarity(a,b):
    """Calculates the similarity between two vectors (1.0 is identical)."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    return float(np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# Step 6 - Build Vector Store

def build_vector_store(chunks):
    """Creates an in-memory database of text and their embeddings."""
    vector_store =[]
    print(f"Generating embeddings for {len(chunks)} chunks...")
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
    """Finds the top K most relevant chunks for a given query."""
    query_embedding = get_embedding(query)
    score_results = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        score_results.append({
            "chunk_id": item["chunk_id"],
            "text": item["text"],
            "score":score 
        })

    # Sort by highest score first
    score_results.sort(key=lambda x: x["score"], reverse=True)
    return score_results[:k] # return the top-k results

# Step 8: RAG Answer
def rag_answer(question,vector_store,k=3):
    """The Retrieval-Augmented Generation step."""
    top_chunks = semantic_search(question,vector_store,k=k)
    context = "\n\n".join([item['text'] for item in top_chunks])

    prompt = f"""Use ONLY the context below to answer the question.
    If answer is not in context, say "I dont know"

    Context:
    {context}

    Question:
    {question}
    """
    response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.0
    )
    return response.choices[0].message.content , top_chunks

def refine_to_structured_json(raw_answer, topic, temp):
    """Refines a raw answer into a structured, beginner-friendly JSON."""
    prompt = f"""
    Explain the following technical solution for the topic: '{topic}'.
    
    Constraints:
    - Under 150 words
    - Beginner-friendly (no jargon)
    - Return output as a JSON object with keys: 'ERROR', 'Description', 'Debugging Commands' and 'Resolution'.
    
    Raw Answer to Process:
    {raw_answer}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # Use response_format to ensure valid JSON
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a senior technical writer. You only output structured JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=temp
    )
    return response.choices[0].message.content

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

def main():
    # Step 1: User Input
    topic, temp = get_user_inputs()
        
    # Step 2: Ingest Data     
    print("Loading PDF.....")
    pdf_text = load_pdf_text(PDF_PATH)

    print("\n Chunking Text....")
    chunks = chunk_text(pdf_text, chunk_size=500)
    print(f"Total chunks created: {len(chunks)}")

    print("\n Building the vector store .........")
    vector_store = build_vector_store(chunks)

    # Step 3: Retrieval & Generation
    print(f"\nPerforming RAG for: {topic}...")
    raw_answer, sources = rag_answer(topic, vector_store)

    if "I dont know" in raw_answer:
        print("\nResult: The knowledge base does not contain information on this topic.")
    else:
        # Step 4: Refinement
        try:
            print("Refining answer into structured JSON...")
            refined_json_str = refine_to_structured_json(raw_answer, topic, temp)
            cleaned_data = clean_output(refined_json_str)
            json_data = json.loads(cleaned_data)
            print(json.dumps(json_data, indent=4))
            print("\nSource Attribution:")
            for s in sources:
                print(f"- Chunk {s['chunk_id']} | Similarity: {s['score']:.4f}")
        except json.JSONDecodeError:
            print("Invalid Json")

    # print("\nSource chunks used ")
    # for s in sources:
    #     print(f"ChunkID:{s['chunk_id']} | Score : {s['score']} ")
    #     print(s['text'][:300])

if __name__ == "__main__":
    main()

