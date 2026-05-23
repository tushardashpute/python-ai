# rag_example.py
# Minimal RAG demo: chunk a text, compute simple embeddings (simulated), and retrieve top-k similar chunks.

from math import sqrt

# simple token-based embedding (toy)

def embed(text):
    # map characters to small ints and return normalized vector
    vec = [ord(c) % 32 for c in text[:128]]
    norm = sqrt(sum(x*x for x in vec)) or 1
    return [x / norm for x in vec]


def cosine(a, b):
    return sum(x*y for x,y in zip(a,b))


docs = [
    "Refund policy: you can return within 30 days.",
    "Shipping policy: orders ship within 3-5 business days.",
    "Privacy: We do not share personal data without consent."
]

embs = [embed(d) for d in docs]


def retrieve(query, k=1):
    qv = embed(query)
    sims = [(i, cosine(qv, e)) for i,e in enumerate(embs)]
    sims.sort(key=lambda x: x[1], reverse=True)
    return [docs[i] for i,_ in sims[:k]]


if __name__ == "__main__":
    q = "How long do I have to request a refund?"
    print("Query:", q)
    print("Top doc:", retrieve(q, k=1)[0])
