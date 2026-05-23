# json_enforcer.py
# Simple loop to request JSON-like output from an LLM (pseudo-demo) and validate it.
# This is a local demo that simulates responses and validates JSON structure.

import json


def is_valid_json(s):
    try:
        obj = json.loads(s)
        return True, obj
    except Exception as e:
        return False, str(e)


def simulate_model_response(correct=True):
    if correct:
        return '{"summary": "This is a summary.", "key_points": ["a","b"], "confidence": 0.95}'
    # malformed response
    return 'Summary: This is a summary. KeyPoints: a,b'


def enforce_json(max_retries=3):
    for i in range(max_retries):
        resp = simulate_model_response(correct=(i>0))
        valid, data = is_valid_json(resp)
        print(f"Attempt {i+1}: valid={valid}")
        if valid:
            return data
    raise RuntimeError("Failed to obtain valid JSON after retries")


if __name__ == "__main__":
    print("Enforcing JSON from simulated model...")
    result = enforce_json()
    print("Obtained JSON:", result)
