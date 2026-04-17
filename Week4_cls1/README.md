# Week 4, Class 1: AI Workflows - From Predictions to Actions

## 📚 Overview
You've learned how to make AI predict, structure, and know. Now it's time to make AI **do things**. This class introduces **AI Workflows**—the bridge between intelligent predictions and real-world actions. Think of it as embedding your AI into a **controlled decision loop** where AI is a component in your code, not the entire program.

---

## 🎯 What You'll Learn Today

### 1. **The Evolution: From RAG to Workflows**

**What we've built so far:**
```
Week 1-2: AI as prediction engine (answers questions)
Week 3:   AI as knowledge engine (answers questions with context)
Week 4:   AI as ACTION engine (executes multi-step processes)
```

**The key distinction:**
```
RAG Systems:          AI knows things
Workflows:            AI DOES things + knows things
```

**Example - Same Task, Different Approaches:**
```
RAG Approach:
  User Input → Retrieve Context → Generate Answer
  Result: "Here's information about your product"

Workflow Approach:
  User Input → Retrieve Context → Generate Decision 
             → Execute Action 1 → Update State 
             → Execute Action 2 → Final Result
  Result: "I've processed your request and updated the system"
```

---

### 2. **What is an AI Workflow?**

An **AI Workflow** is a **structured sequence of steps** where you pre-define exactly what happens and in what order. The AI is simply a **component** inside your code.

**Structure:**
```
Linear:    Step 1 → Step 2 → Step 3 → Done
Branched:  Step 1 → If condition → Step 2a or Step 2b → Done
```

**Key characteristics:**
```
├─ Control:        HIGH - You define the exact flow
├─ Predictability: HIGH - Same input = Same path (mostly)
├─ Structure:      Pre-defined - Not dynamic
└─ AI's Role:      Decision-making at specific points
```

**Real-world example: Document Processing Workflow**
```
1. User uploads PDF
2. Extract text (LLM: Understanding the document type)
3. Chunk the document (Deterministic code)
4. Generate summaries (LLM: For each chunk)
5. Generate metadata (LLM: Category, tags, urgency)
6. Save to database (Deterministic code)
7. Send notification (Deterministic code)

Result: Predictable, high-volume processing
```

---

### 3. **Why Workflows Matter**

**When you NEED workflows:**
```
✅ E-commerce order processing (can't afford mistakes)
✅ Legal document summarization (compliance required)
✅ Medical record analysis (audit trails needed)
✅ Financial reporting (reproducibility required)
✅ Batch processing at scale (consistency matters)
```

**The guarantee workflows give you:**
```
Same Input + Same Workflow = Same Output (every time)
```

This is crucial for:
- **Compliance:** "Here's exactly what the system did"
- **Debugging:** "I can replay this exact sequence"
- **Scale:** "Process 10,000 items reliably"

---

### 4. **Workflow vs Agent: The Critical Difference**

This is THE most important distinction to understand:

| Aspect | Workflow | Agent |
|--------|----------|-------|
| **Path** | You define it | AI decides it |
| **Structure** | Linear/Branched | Interactive loop |
| **Control** | High | Lower |
| **Predictability** | High | Variable |
| **When to use** | Defined processes | Ambiguous tasks |
| **Example** | Processing payroll | Troubleshooting issues |

**Visual comparison:**

```
WORKFLOW (You control the path):
  ┌─────────────┐
  │  User Input │
  └──────┬──────┘
         │
    ┌────▼────┐
    │ Step 1  │ (LLM decision point)
    └────┬────┘
         │
    ┌────▼──────────────┐
    │ If condition A:   │
    │   Step 2A         │
    │ Else:             │
    │   Step 2B         │
    └────┬──────────────┘
         │
    ┌────▼──────┐
    │  Output   │
    └───────────┘

AGENT (AI controls the path):
  ┌─────────────┐
  │  User Goal  │
  └──────┬──────┘
         │
    ┌────▼──────────────────┐
    │  AI Planner (LLM)     │ ◄── AI DECIDES next step
    │  "What tool to use?"  │
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │  Execute Chosen Tool  │
    │  & Update State       │
    └────┬──────────────────┘
         │
         └──► Loop back? (AI decides)
              Or finish?
```

---

### 5. **Building Your First Workflow**

**Anatomy of a workflow:**

```python
def document_processing_workflow(pdf_file):
    # Step 1: Extract text (Deterministic)
    text = extract_pdf(pdf_file)
    
    # Step 2: Classify document (LLM decision point)
    classification = llm.classify_document(text)
    
    # Step 3: Branch based on classification
    if classification == "INVOICE":
        result = process_invoice(text)
    elif classification == "CONTRACT":
        result = process_contract(text)
    else:
        result = process_generic(text)
    
    # Step 4: Save results (Deterministic)
    save_to_database(result)
    
    return result
```

**Key principles:**
```
1. Define the flow FIRST (before writing code)
2. LLM goes at DECISION POINTS (not everywhere)
3. Use deterministic code for guardrails
4. Validate at each step
5. Log everything for audit trails
```

---

### 6. **The Workflow Pattern: Plan, Execute, Validate**

Every workflow follows this pattern:

```
INPUT
  ↓
PLAN (What should happen?)
  ├─ LLM decides: route, priority, approach
  ↓
EXECUTE (Do exactly what was planned)
  ├─ Run the steps in order
  ├─ Each step validated
  ↓
VALIDATE (Is the result correct?)
  ├─ Schema validation
  ├─ Sanity checks
  ├─ Business rules
  ↓
OUTPUT
```

**Example in practice:**
```
INPUT: "Process this invoice"
  ↓
PLAN: LLM says "This is 2024 invoice, route to AR team, priority HIGH"
  ↓
EXECUTE: 
  - Extract invoice number, amount, date
  - Create database entry
  - Generate AR report
  ↓
VALIDATE:
  - Amount > 0? ✓
  - Date is valid? ✓
  - Invoice number unique? ✓
  ↓
OUTPUT: "Invoice processed and routed to AR"
```

---

### 7. **Why Workflows Are Production-Ready**

```
✅ Testability:    Each step is deterministic and testable
✅ Observability:  Clear logs of what happened when
✅ Recoverability: Can retry failed steps
✅ Scalability:    Process thousands reliably
✅ Compliance:     Audit trail of decisions
✅ Debugging:      Replay exact sequence if needed
```

---

## 🔑 Key Takeaways

1. **Workflows = Controlled sequences where AI makes specific decisions**
2. **You define the path; AI makes decisions within that path**
3. **Use workflows for: high-volume, compliance-heavy, reproducible tasks**
4. **Next class: Agents—where AI decides the path itself**

---

## 📝 Files Included

- `wk4_class1.py` - Complete workflow examples and patterns
- `TPAI_Week4_Class1.pdf` - Visual slides and diagrams
- `wk4_hw.txt` - Practice exercises
- `wk4_class1.txt` - Raw notes and detailed exploration

---

## 💡 Remember

**Workflows are the practical workhorse of production AI.** While agents get the attention, workflows run most real AI systems. Master workflows first—they're simpler, more predictable, and most importantly, they **actually work** at scale.

Next up: **Agents** - where you learn to let AI decide its own path.
