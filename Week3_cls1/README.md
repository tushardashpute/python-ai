# Week 3, Class 1: RAG Foundations - From Prompt Engineering to Context Engineering

## 📚 Overview
The most transformative week begins now. You'll learn the **single most important technique** for production AI: how to give models access to knowledge they never learned. This is where hallucination dies and accuracy thrives.

---

## 🎯 What You'll Learn Today

### 1. **The Core Problem: Models Have Knowledge Limits**

What your model knows:
- ✅ General knowledge from training data (2021 or whenever it was trained)
- ✅ Patterns and reasoning
- ❌ Your company's policies
- ❌ Today's news
- ❌ Private documents
- ❌ Proprietary research

**The Result:**
```
Question: "What is our company's refund policy?"
Model Response: "I don't have access to your company policies."
Reality: But it will guess anyway (hallucinate)!
```

**The Solution:** Give it the knowledge it needs!

---

### 2. **From Prompt Engineering to Context Engineering**

This is the paradigm shift:

**Week 1-2: Prompt Engineering**
```
Focus: How do I ask the question?
Result: Better prompts → Better outputs
```

**Week 3: Context Engineering**
```
Focus: WHAT information do I provide WITH the question?
Result: Relevant context → Better, grounded outputs
```

**Both matter!**
```
Good Prompt + Bad Context = Hallucination
Bad Prompt + Good Context = Still works better!
^^ This is the key insight
```

---

### 3. **RAG: Retrieval Augmented Generation**

The three-step process:

#### **Step 1: Retrieval**
```
Question: "What's the refund policy?"
         ↓
    [Search through documents]
         ↓
Find relevant docs: "Refunds are allowed within 30 days..."
```

#### **Step 2: Augmentation**
```
Take the retrieved documents and ADD them to the prompt:

New Prompt:
"
You are a helpful assistant.
Company refund policy: {retrieved_document}
User question: What's the refund policy?
"
```

#### **Step 3: Generation**
```
Model reads BOTH the question AND the policy
         ↓
    [Predicts next tokens]
         ↓
Output: "Based on company policy, refunds..."
(Grounded! Not hallucinating!)
```

---

### 4. **RAG Is NOT a Model Feature**

Critical distinction:

**What OpenAI provides:**
- GPT model
- That's it

**What YOU build:**
- Document ingestion
- Retrieval system
- Prompt composition
- Output validation
- Error handling

**Reality:**
```
RAG = SYSTEM ARCHITECTURE
Not something that "comes in" GPT
Not a library you import
Something you ENGINEER
```

This is why building AI systems is valuable—it's not just using a model!

---

### 5. **The Complete RAG Pipeline**

```
User Question
    ↓
[Step 1: Parse & Prepare]
    Query: "refund details"
    ↓
[Step 2: Retrieve]
    Find similar documents
    Get top 3-5 results
    ↓
[Step 3: Augment]
    Format documents into context
    ↓
[Step 4: Create Prompt]
    Combine: context + question + system message
    ↓
[Step 5: Call Model]
    LLM processes new prompt
    ↓
[Step 6: Validate]
    Check structure, cite sources
    ↓
Final Answer
```

---

### 6. **Example: Bad vs Good**

**Without RAG (Bad):**
```python
question = "What's our refund policy?"

prompt = f"""
Answer this question: {question}
"""

response = call_llm(prompt)
# Response might be completely made up!
```

**With RAG (Good):**
```python
question = "What's our refund policy?"

# Step 1: Get actual policy docs
docs = retrieve_from_database(question)
# Returns: "Refunds allowed within 30 days, receipt required"

# Step 2: Create context-rich prompt
prompt = f"""
You are a company support AI.

Our Policy (from official docs):
{docs}

Customer question: {question}

Answer based ONLY on the above policy.
If not in policy, say you don't know.
"""

response = call_llm(prompt)
# Now it's grounded in truth!
```

---

### 7. **Document Retrieval: The Foundation**

The first critical problem: **Which documents are relevant?**

**Naive approach (Keyword matching):**
```
Question: "Can I return items?"
Search for: "Can", "I", "return", "items"
Results: Documents mentioning ANY of these words
Problem: Way too many false positives
```

**Better: Semantic retrieval**
```
Question: "Can I return items?"
Understand: User is asking about refunds/returns
Search for MEANING not keywords
Results: Only refund/return policy documents
(We'll dive deep into this in Class 2!)
```

---

### 8. **Chunking: Breaking Documents into Pieces**

You can't feed entire books into prompts. You need chunks:

```
Original Document:
[==== 100-page PDF ====]

Chunked:
├─ Chunk 1: Intro [100 tokens]
├─ Chunk 2: Section 1 [150 tokens]
├─ Chunk 3: Section 2 [120 tokens]
├─ Chunk 4: Policy Details [200 tokens]
└─ ... more chunks

When searching:
├─ Find most relevant chunks
├─ Return top 3-5 chunks  
└─ Combine into context
```

**Chunking strategies:**
- By section/page
- By token count
- With overlap
- Semantic-aware

---

### 9. **Vector Databases: The Infrastructure**

Once you have chunks, how do you search them efficiently?

**Traditional database:**
```
Query: "refund policy"
Searching through every document: SLOW
Exact match only: LIMITED
```

**Vector Database:**
```
- Store chunks as VECTORS (not text)
- Search by SIMILARITY
- Fast, efficient, semantic
- Examples: Pinecone, Weaviate, FAISS, Chroma
```

**Why it matters:**
- ✅ Fast search (even with millions of chunks)
- ✅ Semantic understanding (meaning-based)
- ✅ Scalable to production
- ✅ Real-time updates

---

### 10. **Putting It All Together: A RAG System**

```python
import vector_db

def answer_company_question(user_question):
    """
    Complete RAG system
    """
    
    # Step 1: Retrieve relevant policy documents
    retrieved_chunks = vector_db.search(
        query=user_question,
        top_k=5
    )
    
    # Step 2: Format retrieved context
    context = format_context(retrieved_chunks)
    
    # Step 3: Create augmented prompt
    prompt = f"""
    You are a company support AI.
    
    Official Company Policy:
    {context}
    
    Customer Question: {user_question}
    
    Instructions:
    - Answer based ONLY on above policy
    - Cite which section you used
    - If policy doesn't cover it, say so
    - Format response as JSON
    """
    
    # Step 4: Get response
    response = call_llm(prompt, response_format="json")
    
    # Step 5: Validate
    if validate_response(response):
        return response
    else:
        return {"error": "Invalid response, escalate to human"}
```

**This is a production RAG system!**

---

### 11. **When RAG Fails (And How to Fix It)**

**Problem 1: Bad Retrieval**
```
Question: "refund policy"
Retrieved: [Documents about "return shipping"]
Issue: Wrong documents → Bad answer

Fix: Better search, semantic retrieval
```

**Problem 2: Too Much Context**
```
Retrieved 20 pages of docs
Model gets confused
Token limit exceeded

Fix: Better chunking, top-k limit, relevance scoring
```

**Problem 3: Conflicting Information**
```
Multiple documents say different things
Model has to choose

Fix: Citation requirements, contradiction detection
```

---

### 12. **RAG vs Fine-tuning: Why RAG?**

**Fine-tuning:**
- ❌ Expensive
- ❌ Slow (need to retrain)
- ❌ Can't update daily

**RAG:**
- ✅ Cheap
- ✅ Real-time updates
- ✅ Easy to fix
- ✅ Explainable (shows sources)

**Real scenario:**
```
Your company updates policy: "Now 45-day refunds!"
Fine-tuning: Wait 2 weeks, retrain, deploy
RAG: Update database TODAY, bam, it works
```

---

## 🔬 Key RAG Concepts

| Term | Meaning |
|------|---------|
| **Chunk** | A piece of a document (usually 100-500 tokens) |
| **Retrieval** | Finding relevant chunks for a query |
| **Augmentation** | Adding chunks to the prompt context |
| **Generation** | Model generating answer based on context |
| **Vector DB** | Database optimized for semantic similarity search |
| **Embedding** | Numerical representation of text meaning (next class!) |

---

## 🏗️ Complete RAG Architecture

```
Documents
   ↓
[Chunking]
   ↓
Chunks
   ↓
[Embedding] (Day 2)
   ↓
Vectors
   ↓
[Vector DB Storage]
   ↓
User Query
   ↓
[Retrieve]
   ↓
Context + Query
   ↓
[Prompt Formation]
   ↓
[LLM]
   ↓
Answer
   ↓
[Validation]
   ↓
Final Response
```

---

## 💡 The Huge Insight

> For Week 1-2, the model stayed the SAME.
> For Week 3, the MODEL hasn't changed.
> What changed is everything AROUND it!

**Week 3 is about engineering, not AI research.**

---

## 🚀 What This Enables

After today's class:

✅ You understand why RAG matters  
✅ You know the three-step process  
✅ You can design a RAG system  
✅ You understand the limitations  
✅ You know the alternatives  

Tomorrow: **Embeddings** - the secret sauce that makes retrieval work!

---

## 🎯 Real-world Use Cases Ready to Build

1. **Customer Support Bot**
   - Documents: Company policies, FAQs
   - Queries: Customer questions
   - Output: Accurate, cited answers

2. **Internal Knowledge Base**
   - Documents: Employee handbooks, procedures
   - Queries: Staff questions
   - Output: Company-specific answers

3. **Product Documentation QA**
   - Documents: All product docs
   - Queries: User technical questions
   - Output: Accurate technical answers

4. **Legal Document Review**
   - Documents: Legal contracts
   - Queries: Specific clause questions
   - Output: Referenced answers

---

## 📖 Files in This Class
- `wk3_class1.py` - RAG system examples
- `wk3_class1.txt` - Raw class notes

---

## 🔮 Tomorrow: Embeddings

The ONE thing that makes RAG possible:
- How to convert text to numbers MEANINGFULLY
- Why "refund" and "return" are mathematically close
- How to search by SIMILARITY not keywords

---

**Remember:** RAG is not magic—it's **engineering**. You're building a system that feeds the model knowledge so it stops hallucinating! 🎯

