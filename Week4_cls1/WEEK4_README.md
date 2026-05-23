# Week 4: Agents, Tools & Function Calling

## 🎯 Week Overview

Week 4 shows how to make AI do things: call functions, use tools, and coordinate multi-step agentic behaviour. You'll learn how to safely expose capabilities and design agents that act reliably.

### What You'll Master This Week:
1. **Day 1**: Function calling & tool interfaces
2. **Day 2**: Agent architectures and safe orchestration

---

## 📚 Daily Breakdown

### **Day 1: Function Calling & Tools**
**Duration:** 2 hours | **Level:** Advanced

**Topics Covered:**
- Function calling patterns (schema-driven interfaces)
- Designing tool wrappers (APIs, DBs, search)
- Safety and input validation for tool calls
- Observability and logging of tool use

**Key Takeaway:**
> Agents should treat tools as well-defined, validated primitives — not magic boxes.

---

### **Day 2: Agentic Systems & Orchestration**
**Duration:** 2 hours | **Level:** Advanced

**Topics Covered:**
- Architectures for agents (planner, executor, critic)
- Looping patterns and retries
- Error recovery and human-in-the-loop fallbacks
- Multi-agent coordination patterns

**Key Takeaway:**
> Build agents that fail gracefully and log intent, actions and outcomes.

---

## 🎓 Learning Outcomes

By the end of Week 4 you will:

✅ Understand function-calling contracts and schemas  
✅ Build safe tool wrappers and validation layers  
✅ Design a simple planner-executor agent loop  
✅ Handle errors, retries and human fallbacks  

---

## 🚀 Week 4 Practice Projects

1. Implement a function-call schema for a simple calculator tool
2. Wrap a document search API as a tool and call it from prompts
3. Build a planner that breaks tasks into tool calls
4. Add logging and a human confirmation step for risky actions

---

## 📝 Files in Week 4

```
Week4_cls1/
├── wk4_class1.py             # Examples & exercises
├── wk4_class1.txt            # Raw notes
└── TPAI_Week4_Class1.pdf     # Slides

Week4_cls2/
├── ai_assistant_v3_student_tushar.py  # Agent examples
├── ai_assistant_v4_student_tushar.py  # Advanced agent
└── TPAI_Week4_Class2_AgenticRAG.pdf   # Class materials
```

---

## 📂 Class Materials (Week 4)

- Slides (class 1): `TPAI_Week4_Class1.pdf` (in `Week4_cls1`)
- Slides (class 2 / agentic RAG): `TPAI_Week4_Class2_AgenticRAG.pdf` (in `Week4_cls2`)
- Example agents: `ai_assistant_v3_student_tushar.py`, `ai_assistant_v4_student_tushar.py`
- Exercises: `wk4_class1.py`, `wk4_class2.py`

---

**Ready to make AI act in the world?**
👉 **Start with Day 1: function calling examples in `wk4_class1.py`**

---

*Last Updated: 2026*
