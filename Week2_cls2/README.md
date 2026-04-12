# Week 2, Class 2: Advanced Prompt Pipelines & Refinement Loops

## 📚 Overview
It's time to orchestrate intelligence. You'll learn to chain multiple prompts together, creating sophisticated systems where each step builds on the previous one. This is where you move from asking questions to designing algorithmic solutions.

---

## 🎯 What You'll Learn Today

### 1. **From Prompt to Pipeline**
Single prompts are limiting. Real systems need orchestration.

**Evolution:**
```
Level 1: One Prompt
    Input → Prompt → Output

Level 2: Multiple Prompts (Pipeline)
    Input → Prompt1 → Prompt2 → Prompt3 → Output

Level 3: Intelligent Pipeline
    Input → Prompt1 → Validate → Prompt2 → Refine → Output
```

**Why pipelines?**
- ✅ Decomposition: Each prompt does one thing well
- ✅ Control: You can adjust each step independently
- ✅ Debugging: Easier to find where things go wrong
- ✅ Orchestration: Python controls the logic, not just calling one API

---

### 2. **Breaking Down Complex Tasks**

The fundamental pattern:

```
Complex Task = Multiple Simpler Tasks

Example: "Create a learning guide for AI"

Instead of:
❌ "Create a comprehensive learning guide about AI" → One big request

Do this:
✅ Step 1: "Define AI for beginners"
✅ Step 2: "Simplify the definition"
✅ Step 3: "Give a real-world example"
✅ Step 4: "Suggest next steps"
← Combine all into a guide
```

**Each step is simpler, more controllable, more predictable!**

---

### 3. **The Basic Pipeline Pattern**

```python
def build_learning_guide(topic):
    # Step 1: Definition
    definition = llm_call(
        prompt=f"Define {topic} for beginners in 50 words"
    )
    
    # Step 2: Simplification
    simplified = llm_call(
        prompt=f"Make this even simpler: {definition}"
    )
    
    # Step 3: Example
    example = llm_call(
        prompt=f"Give a real example: {simplified}"
    )
    
    # Step 4: Combine
    guide = f"""
    Definition: {definition}
    Simplified: {simplified}
    Example: {example}
    """
    
    return guide
```

**THIS is a pipeline. Each step is independent but coordinated!**

---

### 4. **The Refinement Loop Pattern**
This is the breakthrough pattern:

```python
def refine_until_good(initial_answer, max_iterations=3):
    answer = initial_answer
    
    for i in range(max_iterations):
        # Check if good enough
        quality = evaluate_quality(answer)
        if quality > QUALITY_THRESHOLD:
            print(f"Good enough at iteration {i}")
            break
        
        # Not good? Improve it
        answer = llm_call(
            prompt=f"Improve this answer: {answer}"
        )
    
    return answer
```

**This is everywhere in production AI!**

---

### 5. **Real-World Pipeline Example**

```python
def create_product_description(product_name):
    """
    Pipeline to create a professional product description
    """
    
    # Step 1: Gather basic info
    basic_info = llm_call(f"Describe {product_name} basics")
    
    # Step 2: Add benefits
    benefits = llm_call(
        f"List key benefits of: {basic_info}"
    )
    
    # Step 3: Create call-to-action
    cta = llm_call(
        f"Create compelling CTA for: {basic_info}"
    )
    
    # Step 4: Format for marketing
    description = format_marketing(basic_info, benefits, cta)
    
    # Step 5: Validate (JSON structure)
    if is_valid_marketing_description(description):
        return description
    else:
        # Retry with different prompts
        return create_product_description_retry(product_name)
```

---

### 6. **Using AI to Improve AI (Self-Critique)**

The most powerful pattern:

```python
def self_improving_answer(question):
    """
    Step 1: Get initial answer
    Step 2: Critique the answer
    Step 3: Improve based on critique
    """
    
    # Step 1: Initial answer
    answer = llm_call(
        prompt=f"Answer this question: {question}"
    )
    
    # Step 2: Self-critique
    critique = llm_call(
        prompt=f"""
        Critique this answer: {answer}
        
        Evaluate:
        - Accuracy
        - Completeness  
        - Clarity
        
        What's missing or wrong?
        """
    )
    
    # Step 3: Improve
    improved = llm_call(
        prompt=f"""
        Original answer: {answer}
        Critique: {critique}
        
        Provide an improved version addressing all critiques
        """
    )
    
    return improved
```

**You're using AI to fix AI outputs!** This is incredibly powerful.

---

### 7. **Multi-Level Pipelines**

Handling different complexity levels:

```python
def generate_content_at_level(topic, level):
    """
    Create content at different complexities
    
    level 1 = beginner
    level 2 = intermediate  
    level 3 = advanced
    """
    
    # Context depends on level
    context_prompts = {
        1: "Explain to a 10-year-old",
        2: "Explain to a software engineer",
        3: "Explain to a PhD researcher"
    }
    
    # Generate base content
    base = llm_call(f"Explain {topic}: {context_prompts[level]}")
    
    # Enhance with examples suitable for level
    examples = llm_call(
        f"Give {level*2} examples for: {base}"
    )
    
    # Add advanced depth if needed
    if level >= 2:
        depth = llm_call(
            f"Add technical depth to: {base}"
        )
    else:
        depth = ""
    
    return combine(base, examples, depth)
```

---

### 8. **Pipeline Guardrails**

Enforcing behavior throughout the pipeline:

```python
def orchestrated_pipeline(user_input):
    """
    Pipeline with guardrails at each step
    """
    
    # Step 1: Validate input
    if not validate_input(user_input):
        return error("Invalid input")
    
    # Step 2: Get initial response with guardrails
    response1 = llm_call(
        prompt=f"""
        Answer: {user_input}
        
        GUARDRAILS:
        - Keep under 100 words
        - Use simple language
        - Cite sources if applicable
        """
    )
    
    # Step 3: Validate output
    if not is_valid_json(response1):
        return error("Step 1 failed")
    
    # Step 4: Refine with different guardrails
    response2 = llm_call(
        prompt=f"""
        Improve this response: {response1}
        
        GUARDRAILS:
        - Add specific examples
        - Make it more engaging
        - Add call-to-action
        """
    )
    
    # Step 5: Final validation
    if evaluate_quality(response2) > THRESHOLD:
        return response2
    else:
        return retry_pipeline()
```

---

### 9. **When to Stop Refinement**

This is a practical question:

**Stopping criteria:**
```python
def should_stop_refining(answer, iteration):
    # Stop if good enough
    if quality_score(answer) >= 0.95:
        return True
    
    # Stop if max iterations reached
    if iteration >= MAX_ITERATIONS:
        return True
    
    # Stop if last N iterations show no improvement
    if not improving_significantly(last_iterations):
        return True
    
    # Stop if cost exceeds budget
    if total_cost() > BUDGET_LIMIT:
        return True
    
    return False
```

**Rules of thumb:**
- 🔴 Don't refine forever (set hard limit)
- 🟡 Use quality thresholds
- 🟢 Set diminishing returns threshold
- 🟢 Consider cost/benefit

---

## 🏗️ Architecture Patterns

### Pattern 1: Sequential Pipeline
```
Input → Process1 → Process2 → Process3 → Output
```
Simple, linear flow.

### Pattern 2: Conditional Pipeline
```
Input → Process1 → If quality? 
                    ├─ Yes → Output
                    └─ No → Process2 → Output
```
Intelligent branching.

### Pattern 3: Parallel Pipeline
```
Input → Process1 ─┐
      → Process2 ─┤→ Merge → Output
      → Process3 ─┘
```
Multiple parallel refinements.

### Pattern 4: Feedback Loop
```
Input → Process → Evaluate → If bad:
                               ↓
                            [Improve]
                               ↓ (feedback)
                             Process
```
Refinement until satisfaction.

---

## 💡 The Key Insights

1. **Decompose complex tasks** into simpler steps
2. **Each prompt should do ONE thing well**
3. **Use pipelines instead of one mega-prompt**
4. **Use AI to refine AI outputs** (meta!)
5. **Always validate between steps**
6. **Set stopping criteria** to avoid infinite loops

---

## 🎯 Production Patterns You Can Use Today

### Pattern: Definition + Simplification + Examples
```python
# Great for explanations
step1 = define(topic)
step2 = simplify(step1)
step3 = illustrate(step2)
```

### Pattern: Draft + Review + Improve
```python
# Great for content
step1 = draft(requirements)
step2 = review(step1)  # "What's wrong?"
step3 = improve(step1, step2)
```

### Pattern: Decompose + Process + Aggregate
```python
# Great for complex analysis
parts = decompose(big_input)
processed = [process(p) for p in parts]
result = aggregate(processed)
```

---

## 🔬 Real Example: Comprehensive Learning Guide

```python
def create_comprehensive_guide(topic):
    # Phase 1: Foundation
    definition = llm("Define {topic}")
    why_it_matters = llm("Why does {topic} matter?")
    
    # Phase 2: Building Blocks
    concepts = llm("What are core concepts of {topic}?")
    
    # Phase 3: Practical
    examples = llm("Give practical examples of {topic}")
    use_cases = llm("Real-world use cases")
    
    # Phase 4: Advanced
    advanced = llm("Advanced aspects of {topic}")
    
    # Phase 5: Learning Path
    learning_path = llm(
        f"Create learning path for: {definition}"
    )
    
    # Combine all
    guide = {
        "definition": definition,
        "importance": why_it_matters,
        "concepts": concepts,
        "examples": examples,
        "use_cases": use_cases,
        "advanced": advanced,
        "learning_path": learning_path
    }
    
    return validate_guide(guide)
```

**This is NOT one prompt. This is ARCHITECTURE!**

---

## 🚀 What You Can Now Do

✅ Design multi-step prompt pipelines  
✅ Build refinement loops that iterate  
✅ Decompose complex tasks effectively  
✅ Use AI to improve AI outputs  
✅ Know when to stop refining  
✅ Apply guardrails throughout pipelines  

---

## 🔮 Connecting to Week 3

Next week, we'll add the missing piece: **knowledge**.

You'll learn RAG systems where:
- Instead of asking AI to generate info
- You retrieve relevant information first
- THEN ask AI to reason about it

This combination (Week 2 pipelines + Week 3 RAG) = Production systems!

---

## 📖 Files in This Class
- `wk2_class2.py` - Pipeline examples
- `wk2_class2_notes.txt` - Raw class notes

---

## 🎯 Success Criteria

You're ready for Week 3 when you can:
- [ ] Architect 3-step pipelines
- [ ] Implement refinement loops
- [ ] Decompose a complex task into steps
- [ ] Use AI to critique AI
- [ ] Know when to stop iterating
- [ ] Handle validation errors in pipelines

---

**Remember:** You're not writing prompts anymore—**you're writing systems!** 🚀

