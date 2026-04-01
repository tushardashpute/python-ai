
# Week 1 Class 2 - Structured AI Assistant

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# TODO: input
topic = input("Enter topic: ")
temp = float(input("Temperature: "))

# TODO: structured prompt
prompt = f"""
You are a precise AI instructor.

Explain {topic}.

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
        {"role":"system","content":"You are structured"},
        {"role":"user","content":prompt}
    ],
    temperature=temp
)

print(response.choices[0].message.content)
