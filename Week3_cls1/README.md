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

## 🎯 Interview Questions & Answers

### **Beginner Level Questions**

**Q1: What is RAG and why is it important?**  
**A:** RAG (Retrieval-Augmented Generation) is a technique where AI first retrieves relevant information from a knowledge base, then uses that information to generate answers. It's important because it prevents hallucination by grounding AI responses in actual data, making outputs more accurate and trustworthy.

**Q2: What's the difference between traditional AI and RAG?**  
**A:** Traditional AI relies only on training data (which can be outdated). RAG combines retrieval of current information with generation, allowing AI to access up-to-date knowledge and cite sources. RAG is more accurate and explainable.

**Q3: What are the three steps of RAG?**  
**A:** Retrieval (find relevant documents), Augmentation (add retrieved info to prompt), Generation (AI creates response using the augmented prompt). This three-step process ensures responses are grounded in real knowledge.

### **Intermediate Level Questions**

**Q4: How do you decide what information to retrieve for RAG?**  
**A:** Use semantic similarity between the user's query and your documents. Convert both to embeddings (vector representations), then find documents with highest similarity scores. This ensures you retrieve meaningful, not just keyword-matching, content.

**Q5: What are the challenges of implementing RAG?**  
**A:** Chunking documents appropriately, handling large datasets efficiently, ensuring retrieval quality, managing context window limits, and dealing with conflicting information. Also need good vector databases and embedding models.

**Q6: How does RAG compare to fine-tuning for knowledge updates?**  
**A:** Fine-tuning requires retraining the model (expensive, slow, requires expertise). RAG allows real-time knowledge updates by just updating the retrieval database. RAG is faster, cheaper, and more flexible for changing information.

### **Advanced Level Questions**

**Q7: How would you design a production RAG system?**  
**A:** Include document ingestion pipeline, chunking strategy, embedding generation, vector database, retrieval logic, prompt engineering, response validation, monitoring/metrics, and fallback mechanisms. Consider scalability, cost optimization, and error handling.

**Q8: What are the limitations of RAG and how do you address them?**  
**A:** Retrieval might miss relevant info, retrieved context might not fit in context window, and AI can still hallucinate within retrieved content. Address by: improving retrieval quality, using better chunking, implementing validation, and having human oversight for critical cases.

---

## 🔬 Additional Theory & Real-Time Examples

### **Theory: RAG vs Fine-tuning Decision Framework**

**Choose Fine-tuning when:**
- Domain-specific language patterns are needed
- Consistent style across all responses
- Performance is critical (no retrieval latency)
- Knowledge is stable and won't change

**Choose RAG when:**
- Knowledge changes frequently
- Need to cite sources
- Cost and speed of updates matter
- Knowledge base is large and diverse

**Real-time Example:** A legal AI might use fine-tuning for legal language patterns + RAG for current case law.

### **Theory: Chunking Strategies Deep Dive**

**Strategy 1: Fixed-size Chunking**
```
Document: 2000 tokens
Chunk size: 500 tokens
Result: 4 chunks of ~500 tokens each
Pros: Simple, predictable
Cons: May split related information
```

**Strategy 2: Semantic Chunking**
```
Split on natural boundaries:
- Paragraph breaks
- Section headers
- Topic changes
Pros: Preserves meaning
Cons: Variable sizes
```

**Strategy 3: Sliding Window**
```
Chunk 1: tokens 0-500
Chunk 2: tokens 250-750 (overlap)
Chunk 3: tokens 500-1000
Pros: Better context preservation
Cons: More storage, potential redundancy
```

**Real-time Example:** For code documentation, use semantic chunking on function boundaries. For legal documents, use sliding windows to preserve context.

### **Real-Time Example: Multi-source RAG**

**Scenario:** Customer support with multiple knowledge sources

**Sources:**
- Product manuals (technical specs)
- FAQ database (common questions)
- Support tickets (past resolutions)
- Policy documents (rules and procedures)

**Retrieval Strategy:**
```python
def retrieve_context(query):
    # Search all sources
    manual_results = search_manuals(query, top_k=2)
    faq_results = search_faq(query, top_k=3)
    ticket_results = search_tickets(query, top_k=1)
    policy_results = search_policies(query, top_k=1)
    
    # Combine and rank by relevance
    all_results = manual_results + faq_results + ticket_results + policy_results
    return rank_by_similarity(query, all_results)[:5]
```

**Business Impact:** More comprehensive answers from diverse sources.

### **Theory: RAG Evaluation Metrics**

**Retrieval Metrics:**
- **Precision:** % of retrieved documents that are relevant
- **Recall:** % of relevant documents that were retrieved
- **Mean Reciprocal Rank:** How high relevant docs rank

**Generation Metrics:**
- **Faithfulness:** Does answer match retrieved context?
- **Relevance:** Does answer address the query?
- **Groundedness:** Can claims be verified from sources?

**Real-time Example:** A good RAG system should achieve >80% precision and faithfulness scores.

### **Real-Time Example: RAG for Code Generation**

**Use Case:** AI coding assistant

**RAG Pipeline:**
1. **Query:** "How to implement user authentication in React?"
2. **Retrieve:** Similar code examples, best practices, documentation
3. **Augment:** Include retrieved code patterns in prompt
4. **Generate:** AI writes code using proven patterns

**Prompt Example:**
```
Using these code examples as reference:
[Retrieved authentication examples]

Implement user authentication for a React app with:
- Login/logout functionality
- JWT token handling
- Protected routes
```

**Result:** More reliable, pattern-following code generation.

### **Theory: Cost Optimization in RAG**

**Strategies:**
- **Pre-compute embeddings:** Don't embed at query time
- **Index optimization:** Use efficient vector databases
- **Caching:** Cache frequent queries and results
- **Chunk size:** Balance retrieval quality vs context limits
- **Top-k tuning:** Retrieve only what's needed

**Real-time Example:** A RAG system processing 1000 queries/day can reduce costs by 60% through smart caching and optimal chunking.

### **Real-Time Example: Handling Conflicting Information**

**Problem:** Retrieved documents contradict each other

**Solutions:**
1. **Citation requirement:** Force AI to cite specific sources
2. **Confidence scoring:** Include uncertainty indicators
3. **Human escalation:** Flag conflicts for review
4. **Source ranking:** Prefer authoritative sources

**Example Response:**
```
Based on our product manual (source: PM-2024-v2, page 15), returns are accepted within 30 days. However, the FAQ (source: FAQ-2023) mentions 45 days. I'll escalate this discrepancy for clarification.
```

---

## 🔮 Tomorrow: Embeddings

The ONE thing that makes RAG possible:
- How to convert text to numbers MEANINGFULLY
- Why "refund" and "return" are mathematically close
- How to search by SIMILARITY not keywords

---

**Remember:** RAG is not magic—it's **engineering**. You're building a system that feeds the model knowledge so it stops hallucinating! 🎯

