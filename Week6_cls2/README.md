# Week 6, Class 2: Multi-Agent Patterns & Production Deployment

## 📚 Overview
Single agents are powerful. **Multi-agent systems are revolutionary.** This class shows you how to split complex problems into specialized agents that coordinate, communicate, and scale. Then: how to ship it all to production safely.

---

## 🎯 What You'll Learn Today

### 1. **From Single Agent to Multi-Agent**

**Single Agent System:**
```
User Query
    ↓
[Single Large Agent]
  (Retriever + Reasoner + Decider + Executor)
    ↓
Answer
```

**Problem:**
- Agent does everything (slow)
- One failure breaks everything
- Hard to test individual pieces
- Difficult to scale

---

**Multi-Agent System:**
```
User Query
    ↓
[Coordinator] decides which agents to use
    ↓
    ├─ [Retriever Agent] → Gathers context
    ├─ [Analyzer Agent]  → Understands requirements
    └─ [Executor Agent]  → Takes action
    ↓
Coordinator aggregates results
    ↓
Answer
```

**Benefits:**
- Each agent specialized (does one thing well)
- Parallel execution (faster)
- Failure isolation (one fails, others continue)
- Easy testing (mock individual agents)
- Scales (add agents as needed)

---

### 2. **What is a Multi-Agent System?**

```
Definition:
A multi-agent system is a collection of specialized agents
that work together toward a shared goal through communication
and coordination.

Key Components:
1. Agents: Specialized workers
2. Messages: Communication protocol
3. Coordinator: Routes work
4. Shared State: Common context
5. Fallbacks: Error handling
```

**Real-world analogy:**
```
Single Agent:  One person doing all jobs (slow, burned out)
Multi-Agent:  Team where:
              ├─ Retriever specialist (gets data)
              ├─ Analyzer specialist (understands)
              ├─ Writer specialist (formats)
              └─ Quality specialist (checks)
              → Faster, higher quality, scalable
```

---

### 3. **Types of Multi-Agent Architectures**

**Type 1: Sequential**
```
Task A → Task B → Task C → Done

Example:
Parse Request → Retrieve Context → Generate Answer → Validate
```

**Type 2: Parallel with Aggregation**
```
    ├─ Task A
    ├─ Task B  ──→ Aggregate → Result
    └─ Task C
```

**Type 3: Hierarchical**
```
        [Master Coordinator]
           /    |    \
         /      |      \
    [Team A] [Team B] [Team C]
    (each team has sub-agents)
```

**Type 4: Peer Network**
```
    Agent A ←→ Agent B
      ↓  ↖        ↗  ↓
      ↓   Agent D ←  ↓
    Agent C ←→ Agent E

(Agents communicate peer-to-peer)
```

---

### 4. **Agent Types & Specialization**

**Retriever Agent:**
```
Role: Find relevant information
Input: Query
Output: Ranked chunks with metadata
Specialization: Semantic search, filtering, ranking
```

**Analyzer Agent:**
```
Role: Understand intent and constraints
Input: Query + Retrieved context
Output: Structured analysis (what's needed, constraints)
Specialization: Classification, entity extraction, NLP
```

**Reasoner Agent:**
```
Role: Synthesize information
Input: Analysis + Context
Output: Decision + Reasoning
Specialization: Logic, multi-hop reasoning
```

**Executor Agent:**
```
Role: Take action
Input: Decision
Output: Action result
Specialization: APIs, databases, external systems
```

**Judge Agent:**
```
Role: Validate quality
Input: All outputs from other agents
Output: Pass/Fail with score
Specialization: Evaluation, quality metrics
```

---

### 5. **Building a Multi-Agent System**

**Step 1: Define Agent Roles**

```python
class Agent(ABC):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.memory = []
    
    @abstractmethod
    def execute(self, input: Any) -> Any:
        """Each agent implements its own logic"""
        pass

class RetrieverAgent(Agent):
    def __init__(self, vector_store):
        super().__init__("Retriever", "Find relevant information")
        self.vector_store = vector_store
    
    def execute(self, query: str) -> List[dict]:
        """Retrieve top-k chunks"""
        return self.vector_store.search(query, k=3)

class AnalyzerAgent(Agent):
    def __init__(self):
        super().__init__("Analyzer", "Understand requirements")
    
    def execute(self, query_and_context: dict) -> dict:
        """Analyze what's needed"""
        return {
            "intent": extract_intent(query_and_context),
            "constraints": extract_constraints(query_and_context),
            "confidence": 0.92
        }
```

**Step 2: Create Coordinator**

```python
class MultiAgentCoordinator:
    def __init__(self, agents: List[Agent]):
        self.agents = {agent.name: agent for agent in agents}
        self.execution_log = []
    
    def run(self, query: str) -> Any:
        """Orchestrate agent execution"""
        state = {"query": query, "step": 0}
        
        # Step 1: Retrieve
        retrieval_result = self.agents["Retriever"].execute(query)
        state["retrieved_chunks"] = retrieval_result
        self.log_execution("Retriever", retrieval_result)
        
        # Step 2: Analyze
        analysis_result = self.agents["Analyzer"].execute({
            "query": query,
            "context": retrieval_result
        })
        state["analysis"] = analysis_result
        self.log_execution("Analyzer", analysis_result)
        
        # Step 3: Reason
        reasoning_result = self.agents["Reasoner"].execute({
            "query": query,
            "context": retrieval_result,
            "analysis": analysis_result
        })
        state["reasoning"] = reasoning_result
        self.log_execution("Reasoner", reasoning_result)
        
        # Step 4: Judge
        judgment = self.agents["Judge"].execute(state)
        state["judgment"] = judgment
        
        if judgment["score"] < 70:
            state["status"] = "escalate"
        else:
            state["status"] = "approved"
        
        return state
    
    def log_execution(self, agent_name: str, result: Any):
        """Track execution for debugging"""
        self.execution_log.append({
            "agent": agent_name,
            "result": result,
            "timestamp": datetime.now()
        })
```

**Step 3: Compose System**

```python
# Initialize agents
retriever = RetrieverAgent(vector_store)
analyzer = AnalyzerAgent()
reasoner = ReasonerAgent(llm)
judge = JudgeAgent()

# Compose into coordinator
coordinator = MultiAgentCoordinator([
    retriever, analyzer, reasoner, judge
])

# Run
result = coordinator.run("What's your return policy?")
print(result)
```

---

### 6. **Agent Communication Patterns**

**Pattern 1: Hub and Spoke**
```
        [Coordinator]
       / | | \
      /  |  \ \
   Agent Agent Agent Agent
```

**Pattern 2: Pipeline**
```
Agent1 → Agent2 → Agent3 → Agent4
```

**Pattern 3: Tree**
```
       [Root Agent]
        /  |  \
    Agent Agent Agent
    /      |      \
   A      B      C
```

**Message Protocol:**
```python
class Message:
    sender: str
    recipient: str
    content: dict
    timestamp: float
    message_type: str  # "request", "response", "error"
```

---

### 7. **Handling Failures in Multi-Agent Systems**

**Failure Modes:**

```
1. Agent Timeout
   Solution: Set timeout, use fallback agent or cached result

2. Agent Returns Bad Output
   Solution: Judge validates, retry or escalate

3. Agent Dependency Failure
   Solution: Skip dependent agents, provide degraded results

4. Coordination Deadlock
   Solution: Set execution timeout, force decision

5. State Inconsistency
   Solution: Maintain log, verify state before each step
```

**Resilience Pattern:**
```python
class ResilientCoordinator(MultiAgentCoordinator):
    def run_with_fallbacks(self, query: str) -> Any:
        try:
            return self.run(query)
        except TimeoutError:
            logger.warning("Timeout, using fallback")
            return self.fallback_simple_answer(query)
        except Exception as e:
            logger.error(f"Execution failed: {e}")
            return {
                "status": "escalate",
                "reason": "System error",
                "query": query
            }
```

---

### 8. **Metrics & Observability for Multi-Agent**

**Key Metrics:**

```
Per Agent:
- Execution time (latency)
- Success rate (% successful runs)
- Error rate
- Output quality (judge score)

Per System:
- Total latency (end-to-end)
- Throughput (requests/sec)
- Cost (token usage by agent)
- Escalation rate (% that need human review)

Comparative:
- Agent A vs Agent B: Which is more accurate?
- Agent order: Does sequence matter?
- Parallel vs Sequential: Which is faster?
```

**Monitoring Dashboard:**
```
Dashboard shows:
├─ Active agents
├─ Queue depth (pending requests)
├─ Error rate (red if > 5%)
├─ Average latency
├─ Cost per query
└─ Top failure modes
```

---

### 9. **Production Deployment Checklist**

```
System Design:
□ Agents have clear, non-overlapping responsibilities
□ Fallback agents for critical paths
□ Circuit breakers (fail gracefully)
□ Timeouts on all external calls
□ Async/parallel where possible

Testing:
□ Unit tests for each agent
□ Integration tests for coordination
□ Load testing (100 requests/sec concurrent)
□ Failure scenario testing (agent fails, system recovers)
□ Regression tests (new changes don't break old behavior)

Monitoring:
□ Structured logging (JSON format)
□ Alert on error rate > 5%
□ Alert on latency > 5s
□ Daily cost reports by agent
□ Dashboards for each agent type

Scaling:
□ Can run agents on different machines
□ Load balancer for horizontal scaling
□ Message queue for async coordination
□ Database for persistent state

Safety:
□ Judge validates all outputs
□ Rate limiting (max requests per user)
□ Cost limits (stop if too expensive)
□ Human review for escalated decisions
□ Audit trail (log all decisions)
```

---

### 10. **Real Example: Resume Screening Multi-Agent**

```
User uploads 100 resumes + Job Description
     ↓
[Coordinator]
     ├─ [Parser Agent] → Extract resume sections
     ├─ [Requirement Agent] → Extract job requirements
     ├─ [Matcher Agent] → Match resumes to requirements
     ├─ [Scorer Agent] → Score each candidate
     └─ [Judge Agent] → Validate scores
     ↓
Results: Top 10 candidates ranked

Parallel Execution:
├─ Parser: 2 seconds (parsing 100 resumes in parallel)
├─ Requirement: 1 second
├─ Matcher: 5 seconds (comparing all resumes)
├─ Scorer: 3 seconds
└─ Judge: 2 seconds

Total: ~5 seconds (parallel wins!)
vs Sequential: ~13 seconds
```

---

### 11. **When to Use Multi-Agent Systems**

| Scenario | Single Agent | Multi-Agent |
|----------|------------|-----------|
| Simple Q&A | ✅ Optimal | ❌ Overkill |
| Complex reasoning | ⚠️ Works | ✅ Better |
| Real-time requirements | ⚠️ Slow | ✅ Fast (parallel) |
| Scalability needs | ❌ Hard | ✅ Easy (add agents) |
| Team collaboration | ❌ No | ✅ Yes (agents = team) |
| Error isolation | ❌ Fragile | ✅ Robust |
| Learning/understanding | ✅ Simple | ❌ Complex |

---

## 🚀 What You Can Now Do

✅ Design multi-agent system architectures  
✅ Implement specialized agents with clear roles  
✅ Build coordinators to orchestrate agent execution  
✅ Handle failures and provide fallbacks  
✅ Monitor agent performance and system health  
✅ Deploy production multi-agent systems safely  
✅ Optimize for latency through parallelization  

---

## 📖 Files in This Class
- `multi_agent_demo.py` - Multi-agent coordinator example
- `TPAI_Week6_Class2_MCP_MultiAgent_autogen.pdf` - Framework details

---

## 🎯 Interview Questions & Answers

### **Beginner Level Questions**

**Q1: Why use multiple agents instead of one big agent?**  
**A:** Multiple agents divide work into specialized tasks. This makes each agent simpler, testable independently, and enables parallel execution. If one agent fails, others continue. One big agent doing everything is slow and fragile.

**Q2: What's a coordinator in a multi-agent system?**  
**A:** The coordinator is the traffic controller. It decides which agents to run, in what order, passes results between them, and handles failures. It's like a project manager directing specialists.

**Q3: How do agents communicate?**  
**A:** Through structured messages. Agent A sends a message to Agent B: "Here's my output, please process it." Messages have sender, recipient, content, and metadata. This makes communication testable and loggable.

### **Intermediate Level Questions**

**Q4: Can agents run in parallel?**  
**A:** Yes! If agents don't depend on each other's outputs, run them simultaneously. Coordinator waits for all to complete, then aggregates results. This can reduce total latency significantly (4 agents that each take 1s sequentially take only ~1s in parallel).

**Q5: How do you handle an agent that fails?**  
**A:** First: set timeout (fail fast). Second: use fallback logic (skip this agent, use defaults). Third: try a simpler/faster alternative agent. Finally: escalate if no fallback works. Good systems have 3+ levels of fallback.

**Q6: How do you monitor multi-agent systems?**  
**A:** Log each agent's: input, output, execution time, errors. Track per-agent metrics (accuracy, latency, cost). Create dashboards showing system health. Alert on: high error rates, slow agents, high costs. Use this data to optimize which agents to run.

### **Advanced Level Questions**

**Q7: How do you optimize multi-agent system latency?**  
**A:** Identify critical path (longest dependency chain). Parallelize non-critical agents. Use faster models where possible. Cache common results. Pre-compute what you can. Profile to find slowest agent, optimize it first. Usually Coordinator + Judge are bottlenecks.

**Q8: Can multi-agent systems decide dynamically which agents to run?**  
**A:** Yes! Have a Dispatcher agent that analyzes input and decides which agent combination is best. E.g., "Simple question? → Run fast Responder Agent only. Complex? → Run full pipeline." This adapts to query complexity and saves time/cost.

**Q9: What's the difference between multi-agent and workflows?**  
**A:** Workflows have fixed, pre-defined paths (deterministic). Multi-agent systems can dynamically choose paths (adaptive). Workflows: "Always do A then B then C." Multi-agent: "Do A, analyze result, then do B or C based on result."

---

## 📊 Production Readiness Scoring

Rate your system (0-10):

- **Architecture** (Is design sound?): ___
- **Testing** (Do you have coverage?): ___
- **Monitoring** (Can you see what's happening?): ___
- **Failure Handling** (Do you have fallbacks?): ___
- **Performance** (Is it fast enough?): ___
- **Cost** (Is it within budget?): ___
- **Documentation** (Can others maintain it?): ___

**Score:**
- 0-3: Prototype only
- 4-6: Beta ready
- 7-9: Production ready
- 10: Production hardened

---

## 📚 Key Takeaways

1. **Specialization wins**: Each agent does one thing well, not everything poorly.
2. **Parallelization matters**: Multi-agent systems can be 2-5x faster than sequential.
3. **Failures are inevitable**: Design for graceful degradation, not perfection.
4. **Observability is essential**: You can't optimize what you can't measure.
5. **Start simple, add complexity**: Begin with 2-3 agents, scale as needed.

---

## 🎓 Capstone Project

**Build a multi-agent system for:**
- Customer support (Route → Retriever → Reasoner → Action)
- Content generation (Outline → Research → Write → Edit)
- Data analysis (Load → Clean → Analyze → Visualize)

**Requirements:**
- Minimum 3 agents with clear roles
- Coordinator that manages execution
- Error handling and fallbacks
- Logging and monitoring
- Performance metrics

