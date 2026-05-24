# Week 6, Class 1: Frameworks & Integration Patterns

## 📚 Overview
You've built RAG, agents, and judges from scratch. Now: **why rebuild when frameworks exist?** This class introduces **frameworks and integration patterns**—pre-built abstractions that handle orchestration, error handling, and observability. Think of them as "scaffolding for AI systems."

---

## 🎯 What You'll Learn Today

### 1. **The Abstraction Layers Problem**

**Building from scratch:**
```python
# You write everything manually
pdf_text = load_pdf(file)
chunks = chunk_text(pdf_text)
embeddings = [embed(chunk) for chunk in chunks]
vector_store = build_store(embeddings)
query_embedding = embed(query)
similar = retrieve(query_embedding, vector_store)
prompt = build_prompt(query, similar)
answer = call_llm(prompt)
validate = judge_answer(answer)
log_decision(query, answer, validate)
```

**Problems:**
- Boilerplate everywhere
- Error handling scattered
- Logging inconsistent
- Testing difficult
- Hard to swap components

**With frameworks:**
```python
# Framework handles orchestration
pipeline = RAGPipeline(
    retriever=SemanticRetriever(vector_store),
    llm=GPT4,
    judge=AnswerJudge(),
    logging=ProductionLogger()
)

answer = pipeline.run(query)
```

**Benefits:**
- Cleaner code
- Consistent patterns
- Error handling built-in
- Easy testing
- Swap components easily

---

### 2. **What Are AI Frameworks?**

**Definition:**
```
An AI Framework is a library that provides:
- Composable components (Retriever, LLM, Judge, etc)
- Orchestration (how components connect)
- Error handling (fallbacks, retries)
- Observability (logging, metrics, tracing)
- Testing utilities (mocking, evaluation)
```

**Analogy:**
```
Web Framework: Django, Flask, FastAPI
├─ Routing (handle requests)
├─ Middleware (transform requests)
├─ ORM (database)
└─ Templates (responses)

AI Framework: LangChain, LlamaIndex, AutoGen
├─ Retrieval (get context)
├─ Prompting (prepare input)
├─ LLM calls (process)
├─ Memory (state)
└─ Tools (external actions)
```

---

### 3. **Popular AI Frameworks**

**LangChain:**
```python
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Easy RAG setup
retriever = vector_store.as_retriever()
llm = ChatOpenAI(model="gpt-4o-mini")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

answer = qa_chain.run(query)
```

**Benefits:**
- Batteries included (chains, agents, memory)
- Large ecosystem (integrations)
- Community support

**Challenges:**
- Heavy abstraction (hard to customize)
- Frequent breaking changes
- Can be slower than needed

---

**LlamaIndex (formerly GPT Index):**
```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader

documents = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

response = query_engine.query("What is...?")
```

**Benefits:**
- Optimized for retrieval
- Simple, opinionated defaults
- Good docs

**Challenges:**
- Less flexible than LangChain
- Smaller ecosystem

---

**Pydantic & Structured Outputs:**
```python
from pydantic import BaseModel

class CompanyDecision(BaseModel):
    decision: str  # "approve" | "deny"
    reasoning: str
    confidence: float
    next_steps: list[str]

# Framework handles validation
output = CompanyDecision.parse_obj(llm_response)
# If wrong schema → automatic error
```

**Benefits:**
- Type safety
- Automatic validation
- Serialization/deserialization

---

### 4. **Core Framework Patterns**

**Pattern 1: The Chain**
```
Component → Component → Component → Result
(Sequential composition)

Example:
Query → Retriever → LLM → Judge → User
```

**Pattern 2: The Agent**
```
State → Decide → Act → Update State → Loop?
(Interactive loop)

Example:
Goal → Planner → Choose Tool → Execute → Check Goal?
```

**Pattern 3: The Memory System**
```
Conversation History
├─ Short-term (current session)
├─ Long-term (persistent)
└─ Semantic (related concepts)
```

**Pattern 4: Tools / Integrations**
```
LLM can call → Search, Database, API, Calculator
Framework manages tool registration, calling, result handling
```

---

### 5. **Building Your Own Mini-Framework**

```python
from abc import ABC, abstractmethod
from typing import Any, List
import json

# Abstract base classes
class Component(ABC):
    @abstractmethod
    def process(self, input: Any) -> Any:
        pass

class Retriever(Component):
    def process(self, query: str) -> List[str]:
        # Return top-k chunks
        pass

class LLMComponent(Component):
    def process(self, prompt: str) -> str:
        # Call LLM
        pass

class Pipeline:
    def __init__(self):
        self.components = []
    
    def add(self, component: Component) -> "Pipeline":
        self.components.append(component)
        return self
    
    def run(self, input: Any) -> Any:
        current = input
        for component in self.components:
            current = component.process(current)
        return current

# Usage
pipeline = Pipeline()
pipeline.add(Retriever()).add(LLMComponent()).run(query)
```

---

### 6. **Error Handling & Retries in Frameworks**

**Standard pattern:**
```python
def call_with_retry(fn, max_retries=3, backoff_factor=2):
    wait_time = 1
    for attempt in range(max_retries):
        try:
            return fn()
        except APIError as e:
            if attempt < max_retries - 1:
                time.sleep(wait_time)
                wait_time *= backoff_factor
            else:
                raise
        except ValueError as e:
            # Not retryable
            raise

# Framework usage
@retry(max_retries=3, backoff_factor=2)
def call_llm(prompt):
    return client.chat.completions.create(...)
```

---

### 7. **Logging & Observability**

**What to log:**
```
1. Input: Query/request
2. Routing decision: Which path was taken?
3. Components executed: Which ones, in order
4. Retrieval: What was retrieved, scores
5. LLM call: Tokens used, temperature, model
6. Output: Generated answer
7. Judge decision: Score, passed/failed
8. Errors: What went wrong, where, when
9. Latency: How long did each step take
10. Cost: Token usage, API costs
```

**Structured logging:**
```python
import logging

logger = logging.getLogger("RAG_PIPELINE")
logger.info({
    'event': 'query_started',
    'query': query,
    'timestamp': datetime.now(),
    'user_id': user_id
})

logger.info({
    'event': 'retrieval_complete',
    'chunks_retrieved': 5,
    'avg_score': 0.87
})

logger.error({
    'event': 'llm_call_failed',
    'error': str(e),
    'attempt': 2
})
```

---

### 8. **Testing Framework Components**

```python
import unittest

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = RAGPipeline()
        self.mock_retriever = MockRetriever()
    
    def test_retrieval_integration(self):
        query = "What is the refund policy?"
        results = self.mock_retriever.retrieve(query)
        self.assertEqual(len(results), 3)
        self.assertGreater(results[0]['score'], 0.8)
    
    def test_json_parsing(self):
        """Test that LLM output parses correctly"""
        response = '{"decision": "approve", "confidence": 0.9}'
        parsed = CompanyDecision.parse_raw(response)
        self.assertEqual(parsed.decision, "approve")
    
    def test_error_handling(self):
        """Test fallback when LLM fails"""
        with patch('openai.ChatCompletion.create', side_effect=APIError):
            result = self.pipeline.run(query)
            self.assertEqual(result.recommendation, "escalate")
```

---

### 9. **When to Use Frameworks vs Build from Scratch**

| Scenario | Use Framework | Build Custom |
|----------|--------------|-------------|
| MVP / Prototype | ✅ Fast to build | ❌ Slow |
| Standard RAG | ✅ Batteries included | ⚠️ Can work |
| Complex custom logic | ❌ Hard to extend | ✅ Full control |
| Performance critical | ⚠️ May be too heavy | ✅ Optimized |
| Learning / Understanding | ❌ Too abstracted | ✅ Learn internals |
| Production system | ✅ Mature, tested | ⚠️ Need expertise |
| Rapid iteration | ✅ Easy to swap | ❌ Takes longer |

---

### 10. **Framework Integration Checklist**

```
Before adopting a framework:

□ Does it support your LLM provider?
□ Can you integrate your vector DB?
□ Is observability built-in or easy to add?
□ What's the learning curve?
□ Is the community active?
□ How often do breaking changes happen?
□ Can you test components in isolation?
□ Does it support the patterns you need?
  □ RAG
  □ Agents
  □ Tools/Functions
  □ Memory
□ Performance: Does it meet your latency requirements?
□ Cost: Does the abstraction cost more in tokens?
```

---

### 11. **Real Example: LangChain RAG Pipeline**

```python
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.callbacks import OpenAICallbackHandler

# Initialize components
embedding_fn = OpenAIEmbeddings()
vector_store = Chroma(
    embedding_function=embedding_fn,
    persist_directory="./data"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.0
)

# Create chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# With callbacks for observability
with OpenAICallbackHandler() as cb:
    result = qa_chain({"query": "What is the return policy?"})
    print(f"Tokens used: {cb.total_tokens}")
    print(f"Cost: ${cb.total_cost}")

print(result['result'])
print(result['source_documents'])
```

---

## 🚀 What You Can Now Do

✅ Understand framework abstractions and benefits  
✅ Choose appropriate frameworks for your use case  
✅ Integrate components using framework patterns  
✅ Implement error handling and retries  
✅ Add logging and observability  
✅ Test framework components effectively  
✅ Build custom mini-frameworks when needed  

---

## 📖 Files in This Class
- `wk6_class1.py` - Framework patterns and examples
- `multi_agent_demo.py` - Multi-agent framework example
- `TPAI_Week6_Class1_FrameworksAfterFoundations.pdf` - Detailed slides

---

## 🎯 Interview Questions & Answers

### **Beginner Level Questions**

**Q1: What's a framework and why use one?**  
**A:** A framework provides pre-built components (Retriever, LLM, Judge) and orchestration logic (how they connect, error handling, logging). Instead of writing everything manually, you compose components. Benefit: faster development, fewer bugs, consistent patterns.

**Q2: What's the difference between LangChain and LlamaIndex?**  
**A:** LangChain is more general—it handles RAG, agents, tools, and memory. LlamaIndex (formerly GPT Index) is optimized specifically for retrieval + LLM. LangChain is more flexible; LlamaIndex is simpler for retrieval-only tasks.

**Q3: Why would I build from scratch instead of using a framework?**  
**A:** For learning purposes, full control, extreme performance needs, or highly custom logic. Frameworks abstract away details that are important to understand. But for production systems, frameworks save time and reduce errors.

### **Intermediate Level Questions**

**Q4: How do you handle component failures in a framework?**  
**A:** Frameworks typically use retry logic with exponential backoff, fallbacks (use simpler/faster alternative if primary fails), and structured error handling. You configure thresholds—e.g., retry API errors 3 times, but escalate validation errors immediately.

**Q5: How do frameworks reduce token usage?**  
**A:** By optimizing prompts (removing redundancy), caching embeddings (don't re-embed same text), batching requests, and using smaller models where possible. Some frameworks also implement token budgets: if you're approaching limits, simplify the task.

**Q6: What should you log for observability?**  
**A:** Log: input query, routing decision, each component's execution, latency per component, token usage, LLM call details (model, temperature), output, judge score, any errors. Use structured logging (JSON) so you can parse and analyze later.

### **Advanced Level Questions**

**Q7: Can you build your own framework instead of using established ones?**  
**A:** Yes, and sometimes it's better (fewer dependencies, full control, optimized). But frameworks solve hard problems: memory management, streaming responses, function calling, cost tracking. Building your own is faster for simple cases but scales poorly.

**Q8: How do frameworks handle streaming responses?**  
**A:** They implement callback systems. As the LLM streams tokens, each token triggers a callback that can log, display, or aggregate. Framework manages buffering and consistency. This is important for real-time UX (see answers appear live).

**Q9: What's the production deployment difference for framework-based vs custom systems?**  
**A:** Framework-based: less custom code to maintain, but you're locked into framework updates/changes. Custom: more code, but full control. For production, use frameworks from established projects (LangChain, LlamaIndex) with good stability records.

---

## 📊 Framework Decision Matrix

| Requirement | Weight | LangChain | LlamaIndex | Custom |
|------------|--------|----------|-----------|--------|
| Time to MVP | High | ✅ 1 day | ✅ 1 day | ❌ 1 week |
| Flexibility | Med | ✅ High | ⚠️ Medium | ✅✅ Max |
| Observability | Med | ✅ Built-in | ⚠️ Basic | ❌ DIY |
| Performance | Med | ⚠️ Good | ✅ Good | ✅✅ Optimized |
| Learning | Low | ⚠️ Steep | ✅ Gentle | ❌ Very steep |
| Maintenance | High | ⚠️ Updates | ✅ Stable | ✅ Your code |

---

## 📚 Key Takeaways

1. **Frameworks trade control for speed**: You get built-in patterns but less customization.
2. **Observability is non-negotiable**: Log everything so you can debug and optimize in production.
3. **Start with a framework, understand it, then build custom if needed**: This is the pro path.
4. **Components are your currency**: Think in terms of retriever, LLM, judge, tools—mix and match as needed.

