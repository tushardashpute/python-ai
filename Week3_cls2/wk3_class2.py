#Create embedding

from openai import OpenAI 
import os, json
import numpy as np 

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# response = client.embeddings.create(

#     model = "text-embedding-3-small",
#     input = "refund policy"
# )

# embedding =  response.data[0].embedding

# print(len(embedding)) # vector size 


'''
A verctor is a list of numbers that represent something:
[0.12, -0.45, 0.89, 0.33 ]

when we define it as a set of cooridantes that tells us where they are sititng in the space

for eg [3,5]
x=3
y=5


'''

def cosine_similarity(a,b):
    return np.dot(a,b) / np.linalg.norm(a) * np.linalg.norm(b)  


# refund policy embedding in emb1
emb1 = client.embeddings.create(

    model = "text-embedding-3-small",
    input = "refund policy"
).data[0].embedding

emb2 = client.embeddings.create(

    model = "text-embedding-3-small",
    input = "return rules"
).data[0].embedding

score = cosine_similarity(emb1,emb2)

print("Similarity Score:", score)
# Similarity Score: 0.3786070419135282


documents = [

    "Refunds are allowed within 30 days",
    "Shipping takes 5-7 days",
    "Damaged items can be replaced",
    "Digital products are not refundable"
]

# add some noise

documents.append("Random unrelated text")

def run_prompt(prompt):
    response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
    return response.choices[0].message.content 

# Step 1 - Precompute the embeddings -> this is how it is done in production. 
doc_embeddings = []

for doc in documents:
    emb =  client.embeddings.create(

        model = "text-embedding-3-small",
        input = doc
    ).data[0].embedding

    doc_embeddings.append((doc,emb))

#P.S: We only compute embddings once - not every time. 

# step 2 - we create Query embeddings

def semantic_search(query,k=2):
    query_emb = client.embeddings.create(

                model = "text-embedding-3-small",
                input = query
        ).data[0].embedding
    
    scores = []

    for doc, emb in doc_embeddings:
        score=cosine_similarity(query_emb,emb)
        scores.append((doc,score))
    
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:k] # top-k 

print(semantic_search("return policy"))
#[('Digital products are not refundable', np.float64(0.46964039749569403)), ('Refunds are allowed within 30 days', np.float64(0.450337059690279))]
# (document text(chunk), similarity score) - these are my top 2 (becox of top-k) documents along with theri similarity scores.

# Step 3- Plug this into RAG 

def rag_system_semantic(question):
    results= semantic_search(question)

    context = "\n".join([r[0] for r in results])

    prompt = f"""

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}


"""
    
    return run_prompt(prompt)


print(rag_system_semantic("Can I return an item after 2 weeks?"))
print(rag_system_semantic("return rules"))


