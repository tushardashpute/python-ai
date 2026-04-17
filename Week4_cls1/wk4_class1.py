'''
code will be split into 
1. Regular python tools
2. LLM Planner + tool runner
3. agent loop + reflection

A customer wants a refund after 20 weeks and says the product was damaged. What should we do?”
'''

from openai import OpenAI
import json 
client = OpenAI()

# tools

def get_refund_policy():
    return "Refunds are allowed within 30 days with receipt"

def get_damage_policy():
    return "Damaged items can be replaced or issued store credits"

def classify_issue(user_input):

    text = user_input.lower() # Refund, refund...

    if "refund" in text and "damage" in text:
        return "refund_damage_case"
    elif "refund" in text:
        return "refund_case"
    elif "damage" in text:
        return "damage_case"
    else:
        return "general_case"
    
'''
This is our issue classifier
it reads user input and converts it into the case type.

'''
    
def recommended_action(issue_type):
    if issue_type == "refund_damage_case":
        return f"Offer Replacement or refund depending on the receipt and item status."
    elif issue_type == "refund_case":
        return f"Check refund window and receipt."
    if issue_type == "damage_case":
        return f"Offer replacement or store credit."
    else:
        return f"Escalate to manual review"
    

user_request = "A customer wants a refund after 2 weeks and says the product was damaged"

issue_type = classify_issue(user_request)
refund_policy = get_refund_policy()
damage_policy = get_damage_policy()
action = recommended_action(issue_type)

print("=========Regular chat bot version==========")
print("Issue type: ", issue_type)
print("Refund policy: ", refund_policy)
print("Damage Policy: ", damage_policy)
print("Recommended Action: ", action)

# LLM planner
# Planner prompt 

'''
Akso we ask the llm to output:
    - current reasoning
    - next tool 
    - tool input
    - whether done or not - give the final
'''

# Planner prompt - m imp funciton.
def plan_next_step(user_request, state):
    prompt = f"""
You are an AI support agent planner.

Available tools:
- classify_issue
- get_refund_policy
- get_damage_policy
- recommended_action
- finalize_answer

User Request:
{user_request}

Current State:
{json.dumps(state, indent=2)}

Return ONLY valid JSON in this format:
{{
"thought": "short reasoning",
"next_tool": "tool name",
"tool_input": "input for tool",
"done":  true or false
}}

"""

    response = client.chat.completions.create(

        model ="gpt-4o-mini",
        messages= [ {"role":"user","content":prompt}],
        temperature=0.0 
    )

    return json.loads(response.choices[0].message.content)


# execution layer

def run_tool(tool_name,tool_input):
    if tool_name == "classify_issue":
        return classify_issue(tool_input)
    elif tool_name == "get_refund_policy":
        return get_refund_policy()
    elif tool_name == "get_damage_policy":
        return get_damage_policy()
    elif tool_name == "recommended_action":
        return recommended_action(tool_input)
    else:
        return "Unknown tool in our repo"


'''
The planner decides the tool
the runner executed that tool whcih planner decides 
'''

state = {
    "issue_type": None,
    "refund_policy": None,
    "damage_policy": None,
    "recommended_action": None,
    "steps": []
}

'''
state - agent's working memory 
it stores:
what kind of oissue it is 
what policies have been gathered
what action has been recpmmended
step-by-step trace -v v vimp for validation.

'''

# final step - the LOOP

def support_resolution_agent(user_request,max_steps=5):
    state = {
        "issue_type": None,
        "refund_policy": None,
        "damage_policy": None,
        "recommended_action": None,
        "steps": []
    }

    for step in range(max_steps):
        plan = plan_next_step(user_request, state)

        thought = plan["thought"]
        next_tool = plan ["next_tool"]
        tool_input = plan ["tool_input"]
        done = plan['done']

        state ["steps"].append({

            "step" : step +1,
            "thought": thought,
            "tool": next_tool,
            "tool_input": tool_input

        })

        # loop break conditon.
        if done or next_tool == "finalize_answer":
            break 
        
        result = run_tool(next_tool, tool_input)

        if next_tool == "classify_issue":
            state["issue_type"] = result
        if next_tool == "get_refund_policy":
            state["refund_policy"] = result
        if next_tool == "get_damage_policy":
            state["damage_policy"] = result
        if next_tool == "recommended_action":
            state["recommended_action"] = result

    final_prompt = f"""

You are a customer support AI assistant.

User Request:
{user_request}

State collected:
{json.dumps(state,indent=2)}

Write a final helpful response to the user.
"""

    response = client.chat.completions.create(

        model ="gpt-4o-mini",
        messages= [ {"role":"user","content":final_prompt}],
        temperature=0.0 
    )

    return {
        "state": state,
        "final_answer": response.choices[0].message.content
    }


result =  support_resolution_agent("A customer wants a refund after 2 weeks and says the item was damaged.")


print("========AI AGent===========")
print("Final answer:")
print(result["final_answer"])

print("\n State: ")
print(json.dumps(result["state"], indent=2))


'''
    state = {
        "issue_type": None,
        "refund_policy": None,
        "damage_policy": None,
        "recommended_action": None,
        "steps": []
    }
'''

def reflection_check(state):
    missing = []

    if state['issue_type'] is None:
        missing.append("issue_type")
    if state['recommended_action'] is None:
        missing.append("recommended_action")

    
    if missing :
        return f"Missing required fields : {missing}"
    
    return "State looks complete!"

print(reflection_check(result['state']))

