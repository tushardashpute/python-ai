# Week 1, Class 1: Understanding LLMs - The Foundation

## 📚 Overview
Welcome to your first step into the world of AI! This class focuses on **demystifying Large Language Models (LLMs)** and understanding how they actually work under the hood. Think of this as learning the "DNA of AI."

---

## 🎯 What You'll Learn Today

### 1. **What is an LLM? The Basic Concept**
**LLM = "Probabilistic Next-Token Prediction Engine"**

Don't let the fancy name intimidate you! Here's the simple version:
- LLMs are trained on massive amounts of text data
- They use something called **Transformer Architecture** as their brain
- Instead of truly "understanding" language, they predict the most likely next piece of text

**Real-world analogy:** It's like your phone's auto-complete feature, but on steroids!

### 2. **Tokens: The Building Blocks**
A **token** is NOT a word—it's a small chunk of text. Understanding this is crucial!

**Example:**
```
Text: "Artificial Intelligence"

Could be tokenized as:
- ["Artificial", "Intelligence"]  (2 tokens)
- ["Arti", "fical", "Intell", "igence"]  (4 tokens)

Different models tokenize differently!
```

**Why this matters:**
- Models work with numbers, not words
- Each token has a cost (especially important for APIs!)
- ~1 token ≈ 0.75 words (rough estimate)

### 3. **How Next-Token Prediction Works**
The magic trick behind every AI response:

```
Input: "The capital of France is"

The model assigns probabilities:
├─ Paris    → 91% probability
├─ London   → 3% probability
└─ Berlin   → 2% probability

Output: "Paris" (highest probability)
```

**Key insight:** There's NO pre-knowledge. The model is essentially doing sophisticated probability math based on patterns it learned!

### 4. **The Transformer: Attention Mechanism + Parallel Processing**
The engine that makes modern LLMs work:

- **Attention Mechanism:** Finds which previous tokens matter most for the current prediction
- **Parallel Processing:** Can process multiple tokens simultaneously (unlike older models)

**Example of attention in action:**
```
Sentence: "I went to the bank to deposit money"
When predicting the next word after "bank":
- "money" gets high attention (this is probably a financial context)
- "river" gets low attention (even though banks exist next to rivers)
- Context is the king! 👑
```

### 5. **Context Window: The Memory Limit**
Every LLM has a maximum token limit it can process:

```
Common limits:
├─ GPT-3.5: 4k tokens
├─ GPT-4: 8k-128k tokens
├─ Claude: 100k tokens
└─ This is where different LLMs are competing!
```

**What happens when you exceed the limit?**
- Older tokens get dropped
- Memory pressure increases
- Performance degrades
- **Costs increase** (in production, this is critical!)

### 6. **Hallucination: Not a Bug, It's a Feature**
The model literally making things up. Why?

**Why hallucination happens:**
- Model predicts statistically likely continuations
- It doesn't verify facts or access truth
- It optimizes for *likelihood*, not *correctness*
- No real-time access to data (unless you provide it)

**Example:**
```
Prompt: "List the top 5 employees of Company XYZ"
Response: (Makes up realistic-sounding names!)

Why? Because it has NO knowledge of Company XYZ's employees.
```

**Important:** Hallucination is not a flaw to "fix"—it's a design consequence of how LLMs work. This is why we need **RAG** (Retrieval Augmented Generation) and other techniques. More on that in Week 3!

### 7. **Model vs System: The Critical Distinction**
This is where most people get confused:

**Model (Just the engine):**
- GPT
- Claude
- Gemini
- Stateless: Each call is independent
- No memory between requests

**System (What builds value):**
- Input processing (your prompt)
- Logic layer (your code)
- Output handling (validation, formatting)
- Memory management
- Retrieval capabilities
- Guardrails

**Real-world example:**
```
ChatGPT (Product) = OpenAI's system + GPT (model)
What you'll build = Your system + an LLM model
```

**Companies don't compete on models—they compete on systems!**

---

## 🔬 Key Takeaways

| Concept | Key Point |
|---------|-----------|
| **Tokens** | Not words, but text chunks that models process |
| **Prediction** | LLMs predict the next token based on probability |
| **Context** | Much more powerful than individual words |
| **Attention** | The mechanism that makes transformers work |
| **Hallucination** | A feature, not a bug—plan for it! |
| **System** | What matters is the system around the model |

---

## 💡 What This Means for Your AI Journey

✅ **You now understand:** How the black box actually works  
✅ **You can explain:** Why models sometimes fail or hallucinate  
✅ **You're ready for:** Week 1, Class 2 - where we start building!

---

## 📖 Files in This Class
- `llm_learning.py` - Code examples and demonstrations
- `wk1_class1_notes.txt` - Raw class notes

---

## 🚀 Next Steps
In **Class 2**, we'll learn how to properly structure prompts and understand the different levels of AI systems. Get ready to start building!

---

**Remember:** AI isn't magic—it's sophisticated mathematics. Once you understand the fundamentals, everything else is just engineering! 🎯
