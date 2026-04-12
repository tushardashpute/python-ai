# Week 3: Knowledge & Semantic Understanding - RAG & Embeddings

## 🎯 Week Overview

You've understood AI and controlled its output. Now comes the big piece: **giving AI actual knowledge**. Week 3 is where your systems become production-ready by learning to augment AI with real, retrieval-based knowledge.

### What You'll Master This Week:
1. **Day 1**: RAG fundamentals - shifting from "generation" to "retrieval + generation"
2. **Day 2**: Embeddings & semantic search - making AI understand meaning, not just keywords

---

## 📚 Daily Breakdown

### **Day 1: RAG Foundations - Context Engineering**
**Duration:** 2 hours | **Level:** Advanced

**Topics Covered:**
- From Prompt Engineering to Context Engineering
- RAG architecture and why it matters
- The retrieval + augmentation + generation pipeline
- Building your first RAG system
- Vector databases and indexes

**Key Takeaway:**
> The model hasn't changed since Week 1. Your SYSTEM around it has evolved. Now you're giving it access to knowledge it didn't learn during training.

**Get Started:** [Day 1 README](../Week3_cls1/README.md)

---

### **Day 2: Embeddings & Semantic Search**
**Duration:** 2 hours | **Level:** Advanced

**Topics Covered:**
- What embeddings are (and why they're not just numbers)
- Converting text to vectors
- Semantic similarity through cosine distance
- Building semantic search systems
- Vector databases and efficient storage
- Production-ready retrieval

**Key Takeaway:**
> Embeddings let you find MEANING, not just keywords. "Refund" and "return" are different words but similar meaning—embeddings capture that.

**Get Started:** [Day 2 README](../Week3_cls2/README.md)

---

## 🎓 Learning Outcomes

By the end of Week 3, you will:

✅ Understand RAG architecture and why it's needed  
✅ Build a basic RAG system from scratch  
✅ Know what embeddings are and how they work  
✅ Implement semantic search  
✅ Use vector databases effectively  
✅ Combine RAG + Pipelines from Week 2  
✅ Build production-ready knowledge systems  

---

## 🏗️ The Complete AI System Stack

After Week 3, you'll understand the complete stack:

```
Week 1: Understanding
└─ How models work, what they can/can't do

Week 2: Control
├─ Structured output (JSON validation)
└─ Advanced orchestration (pipelines, refinement)

Week 3: Knowledge ← YOU ARE HERE
├─ Retrieval: Finding relevant information
├─ Augmentation: Injecting into prompt
└─ Generation: AI answers based on knowledge

Week 4: Agency (Preview)
└─ Tools + Function calling
```

---

## 🔄 The RAG Architecture

```
Traditional AI:
    Question → Model → Answer (might be wrong!)

RAG AI:
    Question → [Retrieve] → Find Documents 
                             ↓
                        [Augment] → Add to Context
                             ↓
                        [Generate] → Model → Answer (grounded in docs!)
```

**Why RAG?**
- ✅ No hallucination about company-specific things
- ✅ Always sources from truth
- ✅ Explains where answer comes from
- ✅ Can be updated without retraining model

---

## 💡 Embeddings: The Bridge Between Meaning and Math

**The Problem:**
- Humans understand meaning
- Machines understand numbers
- How do we bridge this gap?

**The Solution: Embeddings**
```
Text: "The company offers a 30-day refund policy"
     ↓ [Embedding model]
Vector: [-0.234, 0.892, -0.445, 0.123, ... 1536 dimensions]
```

**The Magic:**
- Similar meaning = Similar vectors
- "Refund" ≈ "Return" (mathematically close)
- "Refund" ≠ "Spaceship" (mathematically far)

---

## 🔍 What Makes Week 3 Different

| Aspect | Before Week 3 | Week 3+ |
|--------|---|---|
| **Knowledge** | In model parameters | Retrieved from documents |
| **Search** | Keyword matching | Semantic similarity |
| **Accuracy** | Model guesses | Grounded in sources |
| **Hallucination** | Common problem | Mostly prevented |
| **Scope** | Fixed at training time | Updated in real-time |
| **Cost** | Lower per query | Slightly higher (retrieval) |

---

## 🚀 Week 3 Practice Projects

By end of week, try building:

1. **Simple RAG**: Retrieve and augment basic queries
2. **Semantic Search**: Find documents by meaning, not keywords
3. **RAG Pipeline**: Combine all Week 2 patterns + Week 3 knowledge
4. **Document Processor**: Chunk, embed, and index documents
5. **Production RAG**: With validation, error handling, and metrics

---

## 🎯 Success Criteria for Week 3

You'll know you've mastered Week 3 when you can:
- [ ] Explain RAG vs traditional prompting
- [ ] Build a complete RAG system
- [ ] Understand embeddings conceptually
- [ ] Implement semantic search
- [ ] Chunk documents effectively
- [ ] Design a vector database index
- [ ] Combine RAG with pipelines from Week 2

---

## 🔗 Integration: The Complete System

By end of Week 3, you'll have built:

```
┌─────────────────────────────────────────┐
│ USER QUERY                              │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │ PREPROCESSING  │ (Week 2 pattern 1)
         └───────┬────────┘
                 │
      ┌──────────▼──────────┐
      │ SEMANTIC RETRIEVAL  │ (Week 3 pattern)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │ PROMPT WITH CONTEXT │ (Week 1 pattern)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │ LLM GENERATION      │ (Week 1 core)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │ JSON OUTPUT + VALID │ (Week 2 pattern)
      └──────────┬──────────┘
                 │
      ┌──────────▼──────────┐
      │ REFINEMENT IF NEEDED│ (Week 2 pattern 2)
      └──────────┬──────────┘
                 │
         ┌───────▼────────┐
         │ FINAL RESPONSE │
         └────────────────┘

THIS IS A PRODUCTION AI SYSTEM!
```

---

## 📊 Three Weeks Evolution

**Week 1:**
- You learn WHAT (what is an LLM?)
- Result: Understanding

**Week 2:**
- You learn HOW (how to use it?)
- Result: Control and structure

**Week 3:**
- You learn WITH WHAT (with what knowledge?)
- Result: Production systems

---

## 🔮 Looking Ahead to Week 4

**Preview of Week 4: Agents & Tools**

You'll learn what happens when AI needs to **do** something:
- Function calling
- Tool use
- Agent loops
- Error recovery

This is the final piece to build fully autonomous AI systems!

---

## 🌍 Real-World Applications

After Week 3, you can build:

1. **Customer Support Bot**: RAG + your company docs → Accurate support
2. **Internal Knowledge Base**: Employees ask questions → Retrieve relevant policies
3. **Document QA System**: Ask questions about PDFs → Get grounded answers
4. **Research Assistant**: Search academic papers semantically
5. **Product Recommendation**: Understand user intent → Recommend intelligently

---

## 📝 Files in Week 3

```
Week3_cls1/
├── wk3_class1.py               # RAG examples
└── wk3_class1.txt             # Raw notes

Week3_cls2/
├── wk3_class2.py              # Embeddings & semantic search
├── wk3_cls2_rag.py           # Full RAG system
└── wk3_class2.txt            # Raw notes
```

---

## 🎬 How to Succeed in Week 3

1. **Understand the WHY first**
   - Why do we need RAG?
   - Why do embeddings matter?
   
2. **Study both daily READMEs**
   - Architecture before code
   
3. **Run the provided code**
   - See RAG and embeddings in action
   
4. **Experiment**
   - Try different retrieval strategies
   - Play with similarity thresholds
   
5. **Build something**
   - Apply to a real use case

---

## 💡 The Aha Moment

When you connect all three weeks:

**Week 1:** "AI predicts next token"  
**Week 2:** "I can structure what it predicts"  
**Week 3:** "I can give it knowledge to predict better!"  

**Total:** Professional AI system architecture! 🚀

---

## 🔗 Quick Navigation

- 📖 [Day 1: RAG Foundations](../Week3_cls1/README.md)
- 📖 [Day 2: Embeddings & Semantic Search](../Week3_cls2/README.md)
- 🔙 [Week 2 Overview](../Week2_cls1/WEEK2_README.md)
- 🏠 [Main Course README](#)

---

**Ready to give AI superpowers with knowledge?**  
👉 **[Start with Day 1: RAG Foundations](../Week3_cls1/README.md)**

---

*Last Updated: 2026*  
*Where you build production AI systems*
