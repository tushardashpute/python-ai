from pypdf import PdfReader
from openai import OpenAI
import numpy as np 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "TPAI_Week3_Class1.pdf"

# Step 1- Setup client
client  = OpenAI()

# Step 2 - Load PDF 
'''
We first extract the text from the pdf.
At this point, it is just raw text.
PDFREader lets us extract text from the PDF

'''

def load_pdf_text(file_path):
    reader = PdfReader(str(file_path))
    full_text = ""

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text :
            full_text+= f"\n ---- Page {page_num} ---\n{text}\n"

    return full_text

# documents [] in our eg 

# Step 3 - Chunking

def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0,len(text),chunk_size):
        chunk = text [i:i + chunk_size].strip()

        if chunk:
            chunks.append(chunk)
        
    return chunks 

# Chunking creates the unit of knowledge.

# Step 4: Create embeddings
# converting the chunks into embedding - critical step 

def get_embedding(text):
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = text
    )

    return response.data[0].embedding


# we are converting meaning into numbers 

# Step 5: cosine similarity  -1 -> 1
def cosine_similarity(a,b):
    a=np.array(a, dtype=float)
    b=np.array(b, dtype=float) 

    return float(np.dot(a,b) / np.linalg.norm(a) * np.linalg.norm(b)) 


'''
a=[1,2,3]
b=[4,5,6]
np.dot(a,b) -> will be 1*4 + 2*5 + 3*6 = 32

1.0 -> v similar meanning
0.0 -> totally unrelated
-1.0 -> 

more higher -> more similar meaning.

'''

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

'''
In prod 
a real vector DB stores embeddings at scale.
We are just doing the simplest possible version in python - this is the only diff than a prod grade RAG system that we are implementing. 

'''

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


# this is semantic retrieval 

# RAG Answer
def rag_answer(question,vector_store,k=3):
    top_chunks = semantic_search(question,vector_store,k=k)

    context = "\n\n".join([item['text'] for item in top_chunks])

    prompt = f"""
Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

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



print("Loading PDF.....")
pdf_text = load_pdf_text(PDF_PATH)

print("\n Chunking Text....")
chunks =chunk_text(pdf_text, chunk_size=500)
print(f"Total chunks created: {len(chunks)}")

print("\n Building the vector store .........")
vector_store = build_vector_store(chunks)

query = "What is the difference keyword search and meaning search?"
print(f"\nSemantic Search query: {query}")

results =  semantic_search(query,vector_store,k=2)

print("\n top Matching chunks: ")
for r in results:
    print(f"ChunkID : {r['chunk_id']}")
    print(f"Similarity score : {r['score']}")
    print(r['text'][:500])


#question =  "What is RAG and why does it reduce hallucination?"
#question = "Why does chunking matter?"
question = "What is RAG Pipeline?"

print(f"\nRAG Question : {question}")
answer,sources = rag_answer(question,vector_store,k=3)

print("\n Final Answer: ")
print(answer)

print("\nSource chunks used ")
for s in sources:
    print(f"ChunkID:{s['chunk_id']} | Score : {s['score']} ")
    print(s['text'][:300])

