import sys
from pathlib import Path

import numpy as np
from openai import OpenAI
from pypdf import PdfReader

# Ensure stdout can print Unicode characters on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
PDF_PATH = BASE_DIR / "TPAI_Week3_Class1.pdf"

# ====== RAG End-to-End Pipeline ======
# 1. Load text from a source document
# 2. Split the text into chunks
# 3. Convert chunks into embeddings
# 4. Store embeddings in a vector store
# 5. Run semantic search to retrieve top-k relevant chunks
# 6. Build an augmented prompt with retrieved context
# 7. Ask the LLM to answer from the context only

# Step 1: Setup the OpenAI client
client = OpenAI()


def load_pdf_text(file_path: Path) -> str:
    """Extract all text from a PDF file and return it as one string."""
    reader = PdfReader(str(file_path))
    full_text = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            full_text.append(f"\n---- Page {page_num} ----\n{text.strip()}\n")

    return "\n".join(full_text)


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """Break raw text into smaller chunks that will become retrieval units."""
    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)

    return chunks


def get_embedding(text: str) -> list[float]:
    """Create an embedding vector for a piece of text."""
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    score = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return float(score)


def build_vector_store(chunks: list[str]) -> list[dict]:
    """Create a simple in-memory vector store from chunked text."""
    vector_store = []
    for chunk_id, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        vector_store.append({"chunk_id": chunk_id, "text": chunk, "embedding": embedding})

    return vector_store


def semantic_search(query: str, vector_store: list[dict], k: int = 3) -> list[dict]:
    """Retrieve the top-k most relevant chunks for the query."""
    query_embedding = get_embedding(query)
    scored_chunks = []

    for item in vector_store:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored_chunks.append(
            {
                "chunk_id": item["chunk_id"],
                "text": item["text"],
                "score": score,
            }
        )

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)
    return scored_chunks[:k]


def build_rag_prompt(question: str, top_chunks: list[dict]) -> str:
    """Build the augmented prompt that includes retrieved context."""
    context = "\n\n".join(chunk["text"] for chunk in top_chunks)
    return f"""
Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

If answer is not in context, say "I dont know"
"""


def rag_answer(question: str, vector_store: list[dict], k: int = 3) -> tuple[str, list[dict]]:
    """Run the full RAG answer flow: retrieve + augment + generate."""
    top_chunks = semantic_search(question, vector_store, k=k)

    prompt = build_rag_prompt(question, top_chunks)
    print(prompt)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )

    answer = response.choices[0].message.content
    return answer, top_chunks


if __name__ == "__main__":
    print("Loading PDF...")
    pdf_text = load_pdf_text(PDF_PATH)

    print("Chunking text...")
    chunks = chunk_text(pdf_text, chunk_size=500)
    print(f"Total chunks created: {len(chunks)}")

    print("Building the vector store...")
    vector_store = build_vector_store(chunks)

    search_query = "What is the difference between keyword search and semantic search?"
    print(f"\nSemantic search query: {search_query}")
    results = semantic_search(search_query, vector_store, k=2)

    print("\nTop matching chunks:")
    for result in results:
        print(f"ChunkID: {result['chunk_id']} | Score: {result['score']:.4f}")
        print(result["text"][:500])
        print("---")

    # question = "What is the RAG Pipeline?"
    question = "What is RAG Pipeline?"
    print(f"\nRAG question: {question}")
    answer, sources = rag_answer(question, vector_store, k=5)

    print("\nFinal Answer:")
    print(answer)

    print("\nSource chunks used:")
    for source in sources:
        print(f"ChunkID: {source['chunk_id']} | Score: {source['score']:.4f}")
        print(source["text"][:300])
        print("---")

    print("\nEnd-to-end RAG flow:")
    print("1. Load source text from PDF")
    print("2. Chunk text into smaller pieces")
    print("3. Convert chunks to embeddings")
    print("4. Store chunk embeddings in a vector store")
    print("5. Use semantic search to find top-k relevant chunks")
    print("6. Build a context-rich prompt using retrieved chunks")
    print("7. Call the LLM to answer from the context only")
