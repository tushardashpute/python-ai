# Week 2, Class 1: JSON Structured Output - Making AI Predictable

## 📚 Overview
Most developers hope their AI will work correctly. **Professional systems demand it.** Today, you'll learn to enforce structure on AI output so you can actually use it reliably in production code.

---

## 🎯 What You'll Learn Today

### 1. **JSON: It's Not Just Formatting**
Let's be clear: JSON is much more important than styling.

**JSON = A CONTRACT**

```
You define:
├─ Schema: What fields exist
├─ Types: What type each field is  
├─ Structure: How they relate
└─ Expectations: What values are valid
```

**Example - Without Structure:**
```
Output: "The refund policy allows returns within 30 days with a receipt"
Problem: How do you parse this? String matching? Regex? Fragile!
```

**Example - With Structure:**
```json
{
  "refund_allowed": true,
  "days": 30,
  "conditions": ["receipt_required"]
}
```
**Benefit:** Your code can work with this reliably. No parsing needed!

---

### 2. **Why Structure Matters in Production**

**Real-world scenario:**
```
Scenario: You're building a company's support chatbot

Without structure:
├─ Response varies each time
├─ Sometimes answers questions correctly
├─ Sometimes hallucinating company policies
└─ No way to validate before displaying to customers

With structure + validation:
├─ Response format is predictable
├─ You can check if it's accurate
├─ You can block bad responses before showing them
└─ Error handling is possible
```

---

### 3. **Telling AI to Output JSON**

The prompt technique:

```python
prompt = """
You are a helpful company support AI.

User Question: {user_question}

Company Policies:
{relevant_docs}

RESPOND ONLY WITH VALID JSON:
{
  "answer": "Your direct answer here",
  "confidence": 0.0-1.0,
  "from_official_docs": true/false,
  "requires_human_review": true/false
}

Do not include any text outside the JSON.
"""
```

**Keys to success:**
✅ Be explicit: "RESPOND ONLY WITH VALID JSON"  
✅ Show the exact schema  
✅ No other text allowed  
✅ Be clear about types (true/false, not "yes"/"no")  

---

### 4. **The Reality Check: It Still Fails**

Important truth: **AI sometimes won't follow instructions perfectly.**

```python
# What you asked for:
{
  "answer": "...",
  "confidence": 0.9
}

# What you might get:
{
  "answer": "...",
  "confidence": 0.9
}
"I hope this helps!"  # ← Extra text!
```

Or worse:
```
# Invalid JSON:
{
  "answer": "...",
  confidence: 0.9,  # ← Missing quotes!
}
```

**Solution: Always validate!** (We'll get there)

---

### 5. **The Validation Layer**

This is your safety net:

```python
import json

def get_structured_response(prompt):
    try:
        response = call_llm(prompt)
        # Parse JSON
        data = json.loads(response)
        # Validate schema
        validate_schema(data)
        return data
    except json.JSONDecodeError:
        # Retry with better prompt
        return get_structured_response(better_prompt)
    except ValidationError:
        # Data doesn't match expected shape
        return None
```

**Validation strategy:**
1. Parse JSON (structurally valid?)
2. Check schema (has required fields?)
3. Check types (are values the right type?)
4. Check content (does the content make sense?)

---

### 6. **Clean vs True: A Critical Distinction**

This is the biggest insight of the day:

```
CLEAN = Looks good, valid JSON, well-structured
TRUE = Content is actually correct

These are NOT the same!
```

**Example:**
```python
# This is CLEAN but NOT TRUE
{
  "company": "Microsoft",
  "founded": 1975,
  "ceo": "Satya Nadella"  # Actually correct, but
}

# vs this
{
  "company": "Apple",
  "founded": 1975,
  "ceo": "Bill Gates"  # ← Made up! Not true
}
```

**Both are valid JSON. The second one is hallucinating!**

**How to prevent hallucination in structured output:**
1. ✅ Give it context/documents to reference
2. ✅ Ask it to cite sources
3. ✅ Ask for confidence scores
4. ✅ Validate against known data
5. ✅ Use RAG (Week 3!)

---

### 7. **Building a Robust System**

```python
def get_company_info(query):
    # Step 1: Retrieve relevant documentation
    docs = retrieve_docs(query)
    
    # Step 2: Create strict prompt
    prompt = f"""
    You are a company information AI.
    
    User query: {query}
    
    Official documentation:
    {docs}
    
    RESPOND ONLY WITH VALID JSON:
    {{
      "answer": "Answer based only on above docs",
      "found_in_docs": true/false,
      "confidence": 0.0-1.0,
      "sources": ["document names"]
    }}
    """
    
    # Step 3: Get response
    response = call_llm(prompt)
    
    # Step 4: Validate
    try:
        data = json.loads(response)
        # Check required fields
        assert "answer" in data
        assert "confidence" in data
        # Check types
        assert isinstance(data["confidence"], float)
        assert 0 <= data["confidence"] <= 1
        # Check content
        if data["confidence"] < 0.5:
            return handle_low_confidence(data)
        return data
    except (json.JSONDecodeError, AssertionError) as e:
        # Invalid or doesn't match schema
        return fetch_human_support(query)
```

---

### 8. **Real-world Examples**

#### Example 1: Product Recommendation
```json
{
  "product_id": "SKU-123",
  "name": "Product Name",
  "reason": "Why we recommend it",
  "confidence": 0.92,
  "similar_products": ["SKU-124", "SKU-125"]
}
```

#### Example 2: Customer Sentiment Analysis
```json
{
  "sentiment": "positive",
  "score": 0.87,
  "key_phrases": ["great product", "fast delivery"],
  "requires_followup": false
}
```

#### Example 3: Data Extraction
```json
{
  "entities": {
    "name": "John Doe",
    "email": "john@example.com",
    "product": "Widget Pro"
  },
  "extraction_confidence": 0.94,
  "missing_fields": []
}
```

---

## 🔬 Key Takeaways

1. **JSON is a contract**, not just formatting
2. **Structure helps**, but doesn't guarantee correctness
3. **Always validate** both structure and content
4. **CLEAN ≠ TRUE** - You need both
5. **Put guardrails** in your prompts
6. **Expect failures** and handle them gracefully

---

## 💡 The Architecture

```
Your Code
    ↓
[Prompt with JSON schema]
    ↓
LLM
    ↓
Raw Response (might be invalid)
    ↓
[JSON Parser]
    ↓
[Schema Validator]
    ↓
[Content Validator]
    ↓
Trusted Data ✅
or Fallback/Retry ❌
```

---

## 🎯 Production Checklist

Before shipping any structured AI output:

- [ ] Explicit JSON instructions in prompt
- [ ] Clear schema defined in prompt
- [ ] JSON parsing with error handling
- [ ] Schema validation (required fields, types)
- [ ] Content validation (ranges, formats)
- [ ] Logging of failures
- [ ] Fallback/retry strategy
- [ ] Tests with edge cases
- [ ] Human review threshold set

---

## 📖 Files in This Class
- `wk2_class1.py` - Structured output examples
- `wk2_class1_notes.txt` - Raw class notes

---

## 🚀 What You Can Now Do

✅ Enforce JSON output from AI  
✅ Validate both structure and content  
✅ Build error handling for LLM failures  
✅ Distinguish between format and truth  
✅ Create production-ready prompt templates  

---

## 🔮 What's Next?

In **Class 2**, we'll take this to the next level:
- Multi-step refinement loops
- Chaining multiple prompts
- Advanced orchestration patterns

---

**Remember:** Clean JSON ≠ Correct answers. Always validate! 🛡️

