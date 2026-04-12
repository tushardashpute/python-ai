from openai import OpenAI 

import os, json

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def run_prompt(prompt):
    response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
    return response.choices[0].message.content 

# print("========opt1: no context============")
# print(run_prompt("What is my company refund policy? "))

# prompt = """
# You are a helpful AI assitant.

# Explain our company refund policy.
# Constraints:
# - max 50 words
# - JSON format 

# """

# print("=====week2======")
# print(run_prompt(prompt))

# RAG Pipeline Steps:

# Step 1: knowledge base - more like a fake one for this eg, but you can use an actual pdf 
knowledge_base = {

    "refund": "Refunds are allowed within 30 days with receipt!",
    "password": "Password resets require manager approval",
    "timesheet": "timesheets must be submitted every friday before EOD. No EXceptions!!!!"
}

# Step 2 : Retrieval (simple)
def retrieve_context(question):
    q=question.lower()

    if "refund"  in q or "return" in q:
        return knowledge_base["refund"]
    elif "password" in q:
        return knowledge_base["password"]
    elif "timesheet" in q:
        return knowledge_base["timesheet"]
    # else:
    #     return f"It didnt match any policy !"

# Step 3 - RAG Pipline 

def rag_system(question):
    context = retrieve_context(question) # Step 1 of RAG - retrieval 

    prompt = f"""

You are a helpful assistant.

Use the context to answer the question.

Context:
{context}

Question:
{question}

If answer is not in context, say "I dont know"
"""

    return run_prompt(prompt) # step 3 LLM 

print("======with some context======")
print(rag_system("What is the refund policy? ")) # try this agian with rfd instead of refund


documents = [

    "Refunds are allowed within 30 days",
    "Shipping takes 5-7 days",
    "Damaged items can be replaced",
    "CEO salary is $1Million",
]


def simple_search(query, k=2): # default arg of top-k as 2
    results = []
    for doc in documents:
        if any(word in doc.lower() for word in query.lower().split()):
            results.append(doc)
    return results[:2] # top-k 
    

def rag_system(question):

    results = simple_search(question)
    context = "\n".join(results)

    prompt = f""" 
You are a helpful assitant.

Use ONLY the context below to answer.

Context:
{context}

Question:
{question}

If answer is not in context, say "I dont know"
"""

    return run_prompt(prompt) # step 3 LLM 

print("======with updated context======")
print(rag_system("Tell me about refunds and damaged items")) 


# text= """
# Refunds allowed within 30 days.
# Digital products are not refundable.
# Store credit is only avaiable for damaged items.

# """

# chunks = text.split(".")
# print(chunks)

    
# print(simple_search("refund"))
# print(simple_search("refund damaged"))


print(rag_system("What is my CEO salary?")) 

print(simple_search("refund damaged", k=3))