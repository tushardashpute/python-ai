# Week 1: Understanding AI Fundamentals

## 🎯 Week Overview

Welcome to your AI learning journey! **Week 1 is all about understanding**, not yet about building. We'll tear down the mystique around AI and understand how these systems actually work.

### What You'll Master This Week:
1. **Day 1**: The fundamentals of LLMs - tokens, prediction, and how the magic works
2. **Day 2**: How to properly use LLMs - from prompts to complete systems

---

## 📚 Daily Breakdown

### **Day 1: Understanding LLMs**
**Duration:** 2 hours | **Level:** Foundational

**Topics Covered:**
- What is an LLM really?
- Tokens: The building blocks
- Next-token prediction
- Transformers and attention mechanisms
- Context windows
- Hallucination
- Model vs Systems

**Key Takeaway:**
> LLMs are probabilistic prediction engines, not thinking machines. Understand this, and everything else makes sense.

**Get Started:** [Day 1 README](./README.md) (in Week1_cls1 folder)

---

### **Day 2: Prompt Systems & Architecture**
**Duration:** 2 hours | **Level:** Intermediate

**Topics Covered:**
- Prompts are programs, not questions
- Four levels of AI systems (Prompts → RAG → Tools → Workflows)
- Real prompt anatomy
- From single prompts to pipelines
- Prompt refinement loops
- Guardrails for behavior control

**Key Takeaway:**
> You're learning to build systems around AI, not just asking it questions.

**Get Started:** [Day 2 README](../Week1_cls2/README.md)

---

## 🎓 Learning Outcomes

By the end of Week 1, you will:

✅ Understand how LLMs process text at a fundamental level  
✅ Know the difference between models and systems  
✅ Be able to write effective prompts as programs  
✅ Understand the four levels of AI architecture  
✅ Know when to use retrieval vs tools vs workflows  
✅ Be ready to start building your own AI systems  

---

## 🏗️ Architecture Map: Where Week 1 Fits

```
Week 1: UNDERSTANDING
├── How LLMs Work (Deep Dive)
└── How to Use Them (System Architecture)
    
Week 2: CONTROLLING
├── Structured Output (JSON)
└── Multiple Prompt Pipelines

Week 3: KNOWLEDGE
├── RAG Systems
└── Semantic Search & Embeddings

Week 4: AGENTS
└── Tool Use & Agentic Systems
```

---

## 💡 Core Concepts You'll Understand

| Concept | Why It Matters |
|---------|---|
| **Tokens** | The unit of AI understanding; crucial for cost and performance |
| **Context Window** | The limit of what AI can see; critical in production |
| **Hallucination** | A feature, not a bug; plan for it |
| **Prompt Engineering** | Your most important skill this week |
| **Systems Thinking** | Model + Code + Logic = AI System |
| **Pipelines** | How to build sophisticated AI applications |

---

## 🔍 Common Misconceptions Cleared

❌ **"AI understands language like humans"**  
✅ **AI predicts likely token sequences based on patterns**

❌ **"A prompt is just a question"**  
✅ **A prompt is a complete program in natural language**

❌ **"ChatGPT is what you build AI with"**  
✅ **ChatGPT is one product; you build systems around models**

❌ **"Hallucination is a bug to fix"**  
✅ **Hallucination is inherent; you prevent it through system design**

❌ **"More parameters = Better AI"**  
✅ **Better systems + better prompts = Better results**

---

## 📖 Recommended Reading Order

1. Start with **Day 1**: Foundations and LLM internals
2. Progress to **Day 2**: Practical prompt design and systems
3. Review both before starting **Week 2**

---

## 🚀 Week 1 Challenge Projects

By end of week, try building:
1. A prompt that gets consistent JSON output (preview of Week 2!)
2. A simple 2-step prompt pipeline
3. A prompt with effective guardrails
4. Compare hallucination rates with/without context

---

## 🎯 Success Criteria for Week 1

You'll know you're ready for Week 2 when you can:
- [ ] Explain what tokens are and why they matter
- [ ] Describe the attention mechanism in simple terms
- [ ] Write a system message + user message effectively
- [ ] Build a simple prompt pipeline
- [ ] Explain why hallucination happens
- [ ] Distinguish between model capabilities and system capabilities

---

## 📞 Getting Unblocked

**Confused about:**
- **Tokens?** Re-read the Day 1 section on tokenization
- **Prompts?** Day 2 has the complete anatomy explained
- **Systems?** Look at the four levels in Day 2

---

## 🔮 Sneak Peek: What's Coming

**Week 2:** You'll learn to output structured JSON and build multi-step refinement loops.

**Week 3:** Get into the REAL power—RAG systems and semantic search!

**Week 4:** Make AI actually DO things with tools and agents.

---

## 📝 Files in Week 1

```
Week1_cls1/
├── README.md                 # Day 1: Understanding LLMs
├── llm_learning.py           # Code examples
├── random_eg.py              # Additional examples  
├── verify_api.py             # API verification
└── wk1_class1_notes.txt      # Raw notes

Week1_cls2/
├── README.md                 # Day 2: Prompt Systems
├── ai_assistant_v1_student_tushar.py  # First assistant
├── ai_assistant_v2_student_tushar.py  # Improved version
├── prompt_validation.py               # Validation examples
├── validate_json_code.py              # JSON validation
└── wk1_class2_notes.txt              # Raw notes
```

---

## 🎬 How to Use These Materials

Each file builds on the previous. Follow this flow:
1. **Read** the README files first (conceptual understanding)
2. **Review** the .py files (see concepts in action)
3. **Experiment** with the code (modify and test)
4. **Practice** by writing your own prompts

---

## ⭐ Remember

> You're not just learning about AI—**you're learning how to think systemically about AI!**
> 
> The model is just one component. **Your job is to build the system around it.**

---

**Ready to understand the foundation of modern AI?**  
👉 **[Start with Day 1: Understanding LLMs](./README.md)**

---

*Last Updated: 2026*  
*Designed for absolute beginners with programming experience*
