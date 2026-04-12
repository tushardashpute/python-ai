
# Week 1 Class 2 - Structured AI Assistant

import os
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
    
# TODO: structured prompt
prompt = f"""

Explain the Devops concept {topic}.

Constraints:
- max 100 words
- include 1 example

Output:
- bullet points
"""

# TODO: call model
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system","content":"You are a senior devops and Jenkins expert"},
        {"role":"user","content":prompt}
    ],
    temperature=temp,
    max_tokens=150,
)

print(response.choices[0].message.content)
print(f"Completion_Tokens : {response.usage.completion_tokens}")
print(f"Prompt_Tokens : {response.usage.prompt_tokens}")
print(f"Total_Tokens : {response.usage.total_tokens}")
