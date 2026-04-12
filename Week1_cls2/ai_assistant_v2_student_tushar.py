
# Week 2 Class 2 - Structured + Guardrails AI Assistant

import os, json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# TODO: input
topic = input("Enter topic: ")
try:
    temp = float(input("Temperature: "))
    if not (0.2 <= temp <= 0.8):
        print("Temperature shoud be etween 0.2 and 1.0, setting it to 0.5")
except ValueError:
    print("Invalid Input, setting it to 0.5")
    temp=0.5


def run_prompt(prompt):
    # TODO: structured prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":"You are a senior devops engineer, Return the output strictly in JSON format"},
            {"role":"user","content":prompt}
        ],
        temperature=temp,
        max_tokens=500,
    )
    return response

def better_improve_answer(answer):
    # This function takes an answer and prompts the model to rewrite it in a more structured, professional, and beginner-friendly way, while keeping it concise. 
    # The output is expected to be in JSON format with sections and bullet points for easy scanning.
    return run_prompt(f"""
Explain {topic}.

Constraints:
- keep it under 150 words

Rules:
- Return the output strictly in JSON format with sections and bullet points
- Must be beginner-friendly
- No jargon, keep it simple
- Write a concise summary in bullet points

Answer:
{answer}
"""
)


def clean_output(output):
    # Remove code block markers if present
    output=output.strip()

    if output.startswith("```json"):
        print("inside if block")
        output=output[len("```json"):].strip()
    
    if output.endswith("```"):
        print("Inside else part")
        code_marker="```"
        end_index = len(output) - len(code_marker)
        output=output[:end_index].strip()

    return output

def refine_until_good(answer, iterations=3):
    # this function takes an initia answer and refins it iteratively for a given number if times.
    for i in range(iterations):
        print(f"Refinement iteration {i+1}")
        answer = better_improve_answer(answer)
    return answer

try:
    raw = run_prompt(topic)
    refined_output = refine_until_good(raw)
    cleaned_data = clean_output(refined_output.choices[0].message.content)
    json_data = json.loads(cleaned_data)
    print(json.dumps(json_data, indent=4))
except json.JSONDecodeError:
    print("Invalid Json")

# print(response.choices[0].message.content)
print(f"Completion_Tokens : {refined_output.usage.completion_tokens}")
print(f"Prompt_Tokens : {refined_output.usage.prompt_tokens}")
print(f"Total_Tokens : {refined_output.usage.total_tokens}")
