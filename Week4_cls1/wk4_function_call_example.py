# wk4_function_call_example.py
# Simple function-call interface example and lightweight validation.

from typing import Dict, Any


def add_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    # expected schema: {"action": "add", "task": "...", "priority": int}
    if payload.get("action") != "add":
        return {"ok": False, "error": "unsupported action"}

    task = payload.get("task")
    priority = payload.get("priority", 5)
    if not isinstance(task, str) or not task:
        return {"ok": False, "error": "invalid task"}
    if not isinstance(priority, int):
        return {"ok": False, "error": "invalid priority"}

    # pretend to add to a DB
    task_id = 123
    return {"ok": True, "task_id": task_id, "task": task, "priority": priority}


# Example of an agent calling the function
if __name__ == "__main__":
    incoming = {"action": "add", "task": "Write README", "priority": 2}
    result = add_task(incoming)
    print("Function call result:", result)
