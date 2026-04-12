# Week 2: Mastering Structured Output & Advanced Prompting

## 🎯 Week Overview

You've understood how AI works. Now learn to **control it**. Week 2 is about making AI output exactly what you want, in exactly the format you need.

### What You'll Master This Week:
1. **Day 1**: JSON as a contract - making AI outputs structured and predictable
2. **Day 2**: Advanced prompt pipelines - orchestrating multiple AI calls for sophisticated results

---

## 📚 Daily Breakdown

### **Day 1: Structured Output with JSON**
**Duration:** 2 hours | **Level:** Intermediate

**Topics Covered:**
- JSON: Not just formatting, but a CONTRACT
- Making AI output JSON consistently
- Why structure matters in production
- Validation strategies
- Common pitfalls and fixes

**Key Takeaway:**
> JSON is a contract between your system and the AI. Clean structure ≠ Correct data, but it sets clear expectations.

**Get Started:** [Day 1 README](../Week2_cls1/README.md)

---

### **Day 2: Advanced Prompt Pipelines & Refinement**
**Duration:** 2 hours | **Level:** Advanced

**Topics Covered:**
- Multi-step refinement loops
- Decomposing complex tasks
- Using multiple prompts strategically
- Self-critique loops
- Building production-ready pipelines
- Guardrails in pipelines

**Key Takeaway:**
> You're not just improving outputs—you're creating intelligent workflows where each step builds on the previous.

**Get Started:** [Day 2 README](../Week2_cls2/README.md)

---

## 🎓 Learning Outcomes

By the end of Week 2, you will:

✅ Make AI output valid, structured JSON  
✅ Validate AI responses before using them  
✅ Build multi-step refinement loops  
✅ Orchestrate multiple AI calls effectively  
✅ Understand guardrails in production systems  
✅ Know how to decompose complex tasks  

---

## 🏗️ Architecture Evolution

```
Week 1: One Prompt
    User → Prompt → LLM → Output

Week 2: Controlled Outputs
    User → Prompt → LLM → JSON Output → Validation

Week 2+: Pipelines
    User → Prompt1 → Prompt2 → Prompt3 → Output
         → Validate → Refine if needed
```

---

## 🔄 The Refinement Loop Pattern

This is the Week 2 breakthrough:

```python
def get_perfect_answer(question, max_iterations=3):
    answer = initial_answer(question)
    
    for i in range(max_iterations):
        # Is it good enough?
        if quality_score(answer) > THRESHOLD:
            break
        
        # No? Improve it
        answer = improve_answer(answer)
    
    return answer
```

**This pattern is EVERYWHERE in production AI systems!**

---

## 💡 Core Concepts This Week

| Concept | Week 1 | Week 2 |
|---------|--------|--------|
| **Prompts** | "How to write them" | "How to chain them" |
| **Output** | "What to ask for" | "How to validate it" |
| **Structure** | "Why it helps" | "How to enforce it" |
| **Pipelines** | "Concept introduced" | "Patterns and practices" |

---

## 🔍 JSON: From Formatting to Architecture

**Before Week 2 (You write):**
```
Prompt: "Summarize this"
Output: A paragraph of text
Problem: Unstructured, hard to use programmatically
```

**After Week 2 (You'll write):**
```python
prompt = """
Summarize this text.

Output MUST be valid JSON:
{
  "summary": "...",
  "key_points": [...],
  "sentiment": "...",
  "confidence": 0.0-1.0
}
"""

# And then validate:
if is_valid_json(response):
    process(response)
```

---

## 🚀 Week 2 Practice Projects

By end of week, try building:

1. **JSON Enforcer**: Repeat calling AI until valid JSON is returned
2. **Quality Scorer**: Build a function that scores answer quality
3. **Refinement Loop**: Make AI improve its own answers
4. **Multi-step Pipeline**: Chain 3 prompts together intelligently
5. **Guardrail Enforcer**: Ensure outputs follow specific rules

---

## 🎯 Success Criteria for Week 2

You'll know you're ready for Week 3 when you can:
- [ ] Enforce JSON output from AI consistently
- [ ] Validate and handle malformed outputs
- [ ] Build a 3-step prompt pipeline
- [ ] Explain what structure vs correctness means
- [ ] Implement a refinement loop
- [ ] Design guardrails for production use

---

## 📊 Week 2 Progression

```
Monday: "Why JSON matters?"
        → Because it's a contract

Tuesday: "How to enforce it?"
        → Prompts + validation loops

Wednesday: "How to refine?"
          → Multi-step pipelines

Thursday: "How to scale?"
         → Orchestration patterns

Friday: "Let's build!"
       → Production-ready system
```

---

## 🔮 Connection to Other Weeks

**← Week 1 (Foundation):**
You know how LLMs work and how to write prompts.

**Week 2 (Control):**  
You learn to make outputs predictable and structured.

**→ Week 3 (Knowledge):**
You'll add actual knowledge through RAG systems.

---

## 📝 Files in Week 2

```
Week2_cls1/
├── wk2_class1.py               # Structured output examples
└── wk2_class1_notes.txt        # Raw notes

Week2_cls2/
├── wk2_class2.py               # Pipeline examples
└── wk2_class2_notes.txt        # Raw notes
```

---

## 💡 The Big Insight

> In Week 1 you learned to TALK to AI.
> In Week 2 you learn to TRUST AI's output.
> In Week 3 you learn to AUGMENT AI with knowledge.

---

## ⚠️ Common Pitfalls

❌ **"Valid JSON means correct content"**  
✅ **Always validate both structure AND content**

❌ **"One refinement pass is enough"**  
✅ **Use loops; set quality thresholds**

❌ **"AI will always output what you ask"**  
✅ **Always have fallback/retry logic**

---

## 🎬 Getting the Most from Week 2

1. **Read both Daily READMEs** - Get the conceptual foundation
2. **Study the .py files** - See patterns in action
3. **Run the code** - Modify and experiment
4. **Build something** - Apply to your own problem

---

## 🔗 Quick Navigation

- 📖 [Day 1: JSON & Validation](../Week2_cls1/README.md)
- 📖 [Day 2: Pipelines & Refinement](../Week2_cls2/README.md)
- 🔙 [Back to Week 1](../Week1_cls1/README.md)
- ⏭️ [Forward to Week 3](../Week3_cls1/README.md)

---

## 🎓 Quiz: Do You Know These?

- **Q: What's the difference between "valid JSON" and "correct content"?**
  A: JSON validates structure; you must validate meaning separately

- **Q: Why use multiple prompts instead of one complex prompt?**
  A: Decomposition, controllability, and predictability

- **Q: When should a refinement loop stop?**
  A: Either max iterations or quality threshold met

---

**Ready to take control of AI outputs?**  
👉 **[Start with Day 1: JSON as a Contract](../Week2_cls1/README.md)**

---

*Last Updated: 2026*  
*For developers ready to build production AI systems*
