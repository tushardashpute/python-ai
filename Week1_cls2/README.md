# Week 1, Class 2: Building Your First AI System - From Prompts to Pipelines

## 📚 Overview
Now that you understand how LLMs work, it's time to learn how to **properly use them**. Today, you'll learn the difference between asking a question and building a system. This is where the real power begins!

---

## 🎯 What You'll Learn Today

### 1. **Prompts Are NOT Questions!**
This is the most important paradigm shift:

**Wrong way of thinking:**
```
Prompt = "Explain AI"
```

**Correct way of thinking:**
```
Prompt = A complete program written in natural language
```

**Real example:**

❌ **Bad Prompt:**
```
Explain AI
```

✅ **Good Prompt:**
```
You are a senior AI engineer.
Explain AI to a software developer entering the field.
Constraints:
- Keep it under 100 words
- Use simple language
Output format:
- Definition
- Example
```

**Why does this matter?**
- More precise prompts = Less guessing by the model
- Less guessing = More predictable, better results
- Better results = Scalable AI systems

---

### 2. **The Four Levels of AI Systems**

AI systems aren't all the same. They range from simple to complex:

#### **Level 1: Prompt Systems (Stateless)**
```
User Input → Prompt → LLM → Response
```
- Simplest form
- No memory, stateless
- Example: "Summarize this report"
- Most people think this IS AI (but it's not the full story!)

**Limitations:**
- ❌ Hallucination issues
- ❌ Forgets context quickly
- ❌ Can't access private data
- ❌ Can't run code or take action

#### **Level 2: RAG Systems (Retrieval Augmented Generation)**
```
User Question → Retrieve Knowledge → Context → LLM → Response
```
When AI needs **knowledge** it doesn't have:
- ✅ Company documents
- ✅ PDFs and research papers
- ✅ Policy databases
- ✅ Private/proprietary information

**The key insight:** "If AI needs knowledge → Use Retrieval"

#### **Level 3: Tool Systems (Agents)**
```
User Request → AI thinks → Uses Tools → Returns Result
```
When AI needs to **do something**, not just answer:
- ✅ Analyze CSV files
- ✅ Call APIs
- ✅ Run Python code
- ✅ Query databases

**The key insight:** "If AI needs action → Use Tools"

#### **Level 4: Workflows**
Multiple steps combined into a coordinated system:
```
Upload Document 
    ↓
Process it
    ↓
Retrieve Context
    ↓
Generate Answer
    ↓
Store Output
    ↓
Send to User
```

**The big picture:** AI is a **STACK** of architectures, not one thing!

---

### 3. **What is a Real Prompt?**
The complete anatomy of a prompt:

```python
prompt = {
    "system_message": "You are a helpful AI assistant",
    "user_message": "Explain AI in one sentence",
    "conversation_history": [previous messages],
    "retrieved_docs": [relevant documents],
    "formatting_instructions": "JSON format, max 50 words"
}
```

**Components:**
- **System message:** Controls behavior of the model
- **User message:** The actual task/question
- **Conversation history:** Simulates chat (optional)
- **Retrieved documents:** Context (RAG)
- **Tool results:** From executed functions
- **Formatting instructions:** How to structure output

**Example with role-based structure:**
```json
[
  {
    "role": "system",
    "content": "You are a precise AI instructor explaining to beginners."
  },
  {
    "role": "user",
    "content": "Explain hallucination in one sentence."
  },
  {
    "role": "assistant",
    "content": "[Previous model response - for chat context]"
  }
]
```

---

### 4. **From Single Prompts to Prompt Pipelines**

The evolution:

**Stage 1: One Prompt**
```
User Input → Prompt → LLM → Output
```
Basic usage.

**Stage 2: Multiple Structured Prompts**
```
User Input
    ↓
[Prompt 1: Definition]
    ↓
[Prompt 2: Simplify/Advance]
    ↓
[Prompt 3: Example]
    ↓
Final Output
```

This is NO LONGER just a prompt—**it's a pipeline!**

**Why pipelines work:**
- ✅ Decomposition: Break tasks into steps
- ✅ Orchestration: Python controls the flow
- ✅ Control: Each step is optimizable
- ✅ Predictability: More consistent results

**Real example:**
```python
def create_learning_guide(topic):
    # Step 1: Get definition
    definition = llm_call(f"Define {topic} for beginners")
    
    # Step 2: Simplify if complex
    simplified = llm_call(f"Simplify this: {definition}")
    
    # Step 3: Add example
    example = llm_call(f"Give a real example for: {simplified}")
    
    return f"{definition}\n{simplified}\n{example}"
```

**This is ARCHITECTURE, not just prompting!**

---

### 5. **Prompt Refinement Loops**
Making AI better through iteration:

```python
def refine_until_good(answer, iterations=3):
    for i in range(iterations):
        answer = llm_call(
            f"Improve this answer: {answer}"
        )
    return answer
```

**Advanced concept:** We're using AI to fix AI!

**When to stop?**
- Set max iterations
- Check quality threshold
- Have humans evaluate (especially for critical tasks)

---

### 6. **Prompt Guardrails**
Enforcing behavior and constraints:

A guardrail is an explicit constraint you add to the prompt:

```python
prompt = """
You are a support AI for our company.
Answer questions about our refund policy.

GUARDRAILS:
1. Only answer using provided documentation
2. If unsure, ask for human help
3. Never make up policies
4. Keep responses under 100 words
5. Be polite but direct
"""
```

**Why guardrails matter:**
- ✅ Better output quality
- ✅ Consistent behavior
- ✅ Error prevention
- ✅ Brand voice consistency

---

### 7. **Putting It All Together: A Real System**

```python
def answer_company_question(user_question):
    # Step 1: Retrieve relevant docs (guardrails applied)
    docs = retrieve_policy_docs(user_question)
    
    # Step 2: Create context-rich prompt
    prompt = f"""
    You are a helpful company support AI.
    
    User Question: {user_question}
    
    Relevant Policies:
    {docs}
    
    Guidelines:
    - Only answer using above information
    - Be concise (max 100 words)
    - If unsure, say "I don't know"
    - Format as JSON
    """
    
    # Step 3: Get answer
    response = call_llm(prompt)
    
    # Step 4: Validate response
    if is_valid_json(response) and is_appropriate(response):
        return response
    else:
        return "I need human assistance for this query"
```

---

## 🔬 Key Concepts

| Concept | Definition | When to Use |
|---------|-----------|-------------|
| **Prompt** | A program in natural language | Every LLM call |
| **Pipeline** | Multiple prompts in sequence | Complex tasks |
| **Guardrails** | Constraints on AI behavior | Production systems |
| **System Message** | Defines AI role/behavior | Always include |
| **Refinement Loop** | Iterative improvement | When quality matters |

---

## 💡 The BIG Insight

> **You are now programming intelligence, not asking questions!**

When you move from single prompts to pipelines:
- You shift from *using* AI to *building systems with* AI
- Python becomes the orchestrator of intelligence
- You're doing **software engineering**, not just prompt engineering

---

## 🎯 Hierarchy of AI Work

```
Level 1: "ChatGPT user"          → Just type prompts
Level 2: "Prompt Engineer"       → Write good prompts
Level 3: "AI Systems Builder"    → Build pipelines
Level 4: "AI Architect"          → Design full systems
```

**You're moving from Level 2 to Level 3 today!**

---

## 📖 Files in This Class
- `ai_assistant_v1_student_tushar.py` - Initial AI assistant
- `ai_assistant_v2_student_tushar.py` - Improved version with pipelines
- `prompt_validation.py` - Prompt validation examples
- `validate_json_code.py` - Output validation
- `wk1_class2_notes.txt` - Raw class notes

---

## 🚀 What You Can Now Do

✅ Write prompts that are actually programs  
✅ Build multi-step prompt pipelines  
✅ Understand AI system architecture levels  
✅ Apply guardrails for better control  
✅ Validate AI outputs properly  

---

## 🔮 What's Next?

In **Week 2**, we'll learn to:
- Structure AI outputs as JSON
- Create even more sophisticated pipelines
- Validate and ensure output quality
- Stay tuned! The real building begins!

---

**Remember:** You're not just learning to use AI—**you're learning to build systems with it!** 🚀
