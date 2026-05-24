# Week 4, Class 2: Agentic RAG - From Retrieval to Reasoning

## 📚 Overview
RAG taught your system to retrieve knowledge. Today, we go deeper: build systems that **plan what knowledge they need**, **retrieve it intelligently**, and **reason over structured outputs**. Welcome to **Agentic RAG**—where your AI doesn't just answer, it *investigates, retrieves, reasons, and decides*.

---

## 🎯 What You'll Learn Today

### 1. **From Simple RAG to Agentic RAG**

**Simple RAG System:**
```
User Query → Retrieve Context → LLM Answers
Problem: "Does this even need knowledge retrieval?"
Answer: LLM has no idea. It retrieves anyway.
```

**Agentic RAG System:**
```
User Query → Planner LLM (Classify) → Decide Route
            ├─ Route A: Direct answer (no retrieval)
            └─ Route B: Retrieve → Reason → Answer
Benefits: Saves tokens, reduces latency, more intelligent routing
```

**Key Difference:**
- **Simple RAG:** Always retrieves (wasteful)
- **Agentic RAG:** Decides whether to retrieve (smart)

---

### 2. **What is Agentic RAG?**

An **Agentic RAG System** is a multi-step workflow where:

```
Step 1: User Input
"What's your refund policy?"

Step 2: Planner LLM Routes the Request
├─ Classification: "This is a policy question"
├─ Decision: "Needs knowledge retrieval"
└─ Action: Route to retrieval

Step 3: Intelligent Routing
├─ If: Simple FAQ → Direct answer
├─ Else If: Policy question → Retrieve context
├─ Else If: Reasoning needed → Multi-step retrieval

Step 4: Retrieval Layer
├─ Query semantic search
├─ Get top-k relevant chunks
└─ Pass to reasoning layer

Step 5: Reasoning LLM
├─ Process: "Given this context, what's the best answer?"
├─ Structure: "Format as JSON with key fields"
└─ Validate: "Does this meet our quality standards?"

Step 6: Final Output
{
  "answer": "Refunds allowed within 30 days",
  "confidence": 0.92,
  "policy_sources": ["Section 2.1", "Section 3.4"],
  "reasoning": "Customer has receipt and is within timeframe"
}
```

---

### 3. **The Planner: AI as Router**

The **Planner LLM** is the intelligence center:

```
Role: Decide what action to take
Input: User question
Output: Structured JSON decision
```

**Example Planner Output:**
```json
{
  "classification": "company_policy_question",
  "retrieval_needed": true,
  "search_queries": [
    "refund policy timeline",
    "return requirements"
  ],
  "confidence_in_classification": 0.95,
  "reasoning": "Customer asking about refund details, clearly needs policy context"
}
```

**Why this matters:**
- Saves tokens by avoiding unnecessary retrieval
- Reduces latency (direct answers are instant)
- Improves accuracy (knows what it needs)
- Makes system auditable (explains its routing decision)

---

### 4. **Agentic RAG Pipeline: End-to-End**

```
┌─────────────────────────────────────────────┐
│ 1. USER INPUT                               │
│ "Can I return items bought 60 days ago?"   │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 2. PLANNER LLM (Routing Decision)           │
│ Returns JSON:                               │
│ {                                           │
│   "needs_retrieval": true,                 │
│   "search_queries": [                      │
│     "return policy timeframe",             │
│     "timeline for returns"                 │
│   ]                                        │
│ }                                          │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 3. SEMANTIC SEARCH (Week 3 skill)           │
│ For each search query:                      │
│ - Embed query                               │
│ - Find top-k similar chunks                 │
│ - Aggregate results                         │
│ Result: Top 3 most relevant policy chunks  │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 4. BUILD AUGMENTED PROMPT                  │
│ Context = Top chunks + metadata             │
│ Reasoning task = "Given context, answer"   │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 5. REASONING LLM (Structured Output)        │
│ Input: Context + Question                   │
│ Output JSON:                                │
│ {                                           │
│   "answer": "No, 60 days exceeds...",      │
│   "reasoning": "Policy states...",         │
│   "exceptions": "None apply here",         │
│   "recommendation": "Deny"                 │
│ }                                          │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 6. VALIDATION (Pydantic)                    │
│ Check: All fields present?                  │
│ Check: Types correct?                       │
│ Check: Confidence scores valid?             │
│ Fail safely if validation fails             │
└────────────┬────────────────────────────────┘
             │
┌────────────▼────────────────────────────────┐
│ 7. FINAL OUTPUT TO USER                     │
│ Structured, validated response              │
└─────────────────────────────────────────────┘
```

---

### 5. **Structured Outputs with Pydantic**

Why structured outputs matter:

```python
# ❌ String output (unreliable)
answer = "Yes or no..."
if "yes" in answer.lower():
    process_approval()
# Problem: Fragile parsing, prone to errors

# ✅ Pydantic (reliable)
from pydantic import BaseModel

class PolicyDecision(BaseModel):
    answer: str
    reasoning: str
    confidence: float
    recommendation: str  # "approve" | "deny" | "escalate"

decision = PolicyDecision.parse_obj(llm_output)
if decision.recommendation == "approve":
    process_approval()  # Safe, type-checked
```

**Benefits:**
- Type safety (Python catches errors before runtime)
- Validation (fields must be correct format)
- Documentation (clear what system expects)
- Serialization (easy to store/send)

---

### 6. **Decision LLM: Reasoning Over Context**

The second LLM makes the actual decision:

```
Input to Decision LLM:
─────────────────────
Policies (from retrieval):
"Refunds allowed within 30 days with receipt"
"Items must be in original condition"
"Shipping costs are non-refundable"

Question:
"Can I return my jacket bought 40 days ago?"

Task:
Reason over the policies and answer.
Format your response as JSON with:
- decision: (approve/deny)
- reasoning: (explain why)
- policy_applied: (which policy matches)

Output:
─────────────────────
{
  "decision": "deny",
  "reasoning": "Purchase was 40 days ago, exceeds 30-day window",
  "policy_applied": "Return Policy Section 1.1",
  "exception_possible": false
}
```

---

### 7. **Multi-Step Retrieval: When One Search Isn't Enough**

Complex questions may need multiple retrievals:

```
Question: "Can I return my international order that was shipped but damaged?"

Planner decides:
[
  "Search 1: return policy international orders",
  "Search 2: damaged goods policy",
  "Search 3: shipping damage coverage"
]

Retrieval step:
├─ Search 1 → Chunk A (international returns)
├─ Search 2 → Chunk B (damage assessment)
└─ Search 3 → Chunk C (shipping insurance)

Aggregate context from all three searches
Feed combined context to Reasoning LLM

Reasoning LLM now has complete picture:
- International status ✓
- Damage policy ✓
- Shipping coverage ✓
→ Can make informed decision
```

---

### 8. **Implementation Example**

```python
def agentic_rag_workflow(user_query):
    # Step 1: Planner decides what's needed
    planner_output = planner_llm(user_query)
    # Returns: {"needs_retrieval": true, "search_queries": [...]}
    
    if not planner_output["needs_retrieval"]:
        # Direct answer, no retrieval needed
        return reasoning_llm(user_query)
    
    # Step 2: Multi-query retrieval
    all_context = []
    for query in planner_output["search_queries"]:
        chunks = semantic_search(query, vector_store, k=3)
        all_context.extend(chunks)
    
    # Step 3: Reasoning with context
    augmented_prompt = build_prompt(user_query, all_context)
    decision_output = reasoning_llm(augmented_prompt)
    
    # Step 4: Validate structure
    validated = PolicyDecision.parse_obj(decision_output)
    
    # Step 5: Return result
    return validated
```

---

### 9. **Why Agentic RAG Matters**

**Problems it solves:**

| Problem | Simple RAG | Agentic RAG |
|---------|-----------|-----------|
| Wastes tokens on simple Q&A | ❌ Yes | ✅ Routes direct |
| Can't handle multi-step questions | ❌ Fails | ✅ Multi-retrieval |
| Unpredictable outputs | ❌ String parsing | ✅ Validated JSON |
| No reasoning explanation | ❌ Just answers | ✅ Explains decision |
| Can't decide confidence | ❌ Always confident | ✅ Structured confidence |

---

### 10. **Practical Applications**

**Customer Service:**
- Route simple FAQ → direct answer
- Route complex policy Q → retrieval + reasoning
- Output: Structured decision with confidence

**Loan Processing:**
- Planner: Classifies application type
- Retriever: Gets relevant policies, rates, precedents
- Reasoner: Evaluates risk, makes decision, explains it

**Resume Screening:**
- Planner: Identifies must-haves vs nice-to-haves
- Retriever: Finds matching resume sections
- Reasoner: Ranks candidates, explains reasoning

---

### 11. **Error Handling & Fallbacks**

```python
def safe_agentic_rag(query):
    try:
        # Try planner
        plan = planner_llm(query)
    except:
        # Fallback: assume retrieval needed
        plan = {"needs_retrieval": True, "search_queries": [query]}
    
    try:
        # Try retrieval
        context = semantic_search(plan["search_queries"], vector_store)
    except:
        # Fallback: use general knowledge only
        context = []
    
    try:
        # Try reasoning
        decision = reasoning_llm(query, context)
    except:
        # Fallback: return safe default
        decision = {
            "answer": "I need human review",
            "confidence": 0.0,
            "recommendation": "escalate"
        }
    
    return decision
```

**Key principle:** Always have fallbacks for production systems!

---

## 🚀 What You Can Now Do

✅ Understand agent-based decision routing  
✅ Implement multi-step planning with LLMs  
✅ Build structured outputs with Pydantic  
✅ Handle complex questions requiring multiple retrievals  
✅ Validate and error-handle agent outputs  
✅ Deploy production-ready agentic systems  

---

## 📊 Agentic RAG vs Other Approaches

| Feature | Simple Chat | Simple RAG | Agentic RAG |
|---------|-----------|-----------|-----------|
| Knowledge | ❌ Limited | ✅ Retrieves | ✅ Selective |
| Planning | ❌ None | ❌ Always retrieves | ✅ Decides |
| Routing | ❌ One path | ❌ One path | ✅ Multiple paths |
| Structured outputs | ❌ String | ❌ String | ✅ JSON/Pydantic |
| Cost efficiency | ✅ Cheap | ⚠️ Medium | ✅ Optimized |
| Reasoning | ❌ None | ⚠️ Basic | ✅ Multi-step |
| Production ready | ❌ No | ⚠️ Maybe | ✅ Yes |

---

## 📖 Files in This Class
- `wk4_class2.py` - Full agentic RAG example
- `ai_assistant_v3_student_tushar.py` - Practical workflow
- `ai_assistant_v4_student_tushar.py` - Enhanced version
- `ThinkPythonAI_Demo_Company_Policies.pdf` - Sample knowledge base

---

## 🎯 Interview Questions & Answers

### **Beginner Level Questions**

**Q1: What's the difference between simple RAG and agentic RAG?**  
**A:** Simple RAG always retrieves context and then answers. Agentic RAG first decides *whether* to retrieve, making it smarter and more cost-efficient. It uses a planner LLM to classify the request and route it appropriately.

**Q2: Why does the planner matter?**  
**A:** The planner routes requests intelligently. Simple questions get direct answers (fast, cheap). Complex questions get full retrieval + reasoning (accurate, grounded). This saves money and reduces latency without sacrificing quality.

**Q3: What is Pydantic and why use it?**  
**A:** Pydantic validates that LLM outputs match an expected structure (schema). Instead of parsing messy strings, you get type-safe Python objects. If the LLM output doesn't match the schema, it fails loudly rather than silently failing downstream.

### **Intermediate Level Questions**

**Q4: How do you handle multi-step reasoning in agentic RAG?**  
**A:** The planner can return multiple search queries. Each retrieves relevant context, then all contexts combine into one augmented prompt. The reasoning LLM sees the complete picture and can reason across multiple domains (e.g., international policy + damage policy + shipping).

**Q5: What's a fallback strategy when the planner fails?**  
**A:** Assume retrieval is needed and proceed to semantic search. If that fails, use general knowledge. If reasoning fails, escalate to human or return a safe default. Always have three levels of fallback for production systems.

**Q6: How do you measure confidence in an agentic RAG system?**  
**A:** Include a confidence score in the structured output. This can come from the planner's confidence in classification, the similarity scores from retrieval, or the reasoning LLM's own confidence token probabilities. Use this to decide: execute automatically, flag for review, or escalate.

### **Advanced Level Questions**

**Q7: Can agentic RAG handle contradictory information in retrieved contexts?**  
**A:** Yes. The reasoning LLM sees all retrieved chunks and can note contradictions. You can add validation rules: if chunks conflict and confidence drops below threshold, escalate to human rather than making a confident wrong decision.

**Q8: How do you optimize token usage in agentic RAG?**  
**A:** Route simple queries directly (skips retrieval entirely). For complex queries, pre-filter chunks by relevance before feeding to LLM. Use smaller models for routing decisions, larger ones for reasoning. Batch similar requests. Monitor token costs per query type.

**Q9: What's the production deployment checklist for agentic RAG?**  
**A:** (1) Structured logging of planner decisions and reasoning chains, (2) Human review dashboards for escalated cases, (3) Metrics tracking: classification accuracy, retrieval relevance, decision correctness, (4) Cost monitoring by query type, (5) A/B testing different planner prompts, (6) Fallback system health checks.

---

## 📚 Key Takeaways

1. **Planning changes everything**: A system that decides what to do is smarter than one that always does the same thing.
2. **Structure your outputs**: JSON + Pydantic prevents silent failures and makes production systems reliable.
3. **Think in workflows**: Agentic RAG is a orchestrated sequence, not just RAG + LLM glued together.
4. **Always have fallbacks**: Production systems fail. Plan for it.

