from openai import OpenAI 

import os 

def init_client():
    api_key= os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY not found. Run source ~/.zshrc"
        )
    print("Environment verified")
    
    return OpenAI(api_key=api_key)
client = init_client()

# Step 2: Basic prompt 
#without sytem 
# response = client.chat.completions.create(
#     model = "gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "Explain Hallucination."}
#     ],
# )

# print("\n Without System:")
# print(response.choices[0].message.content)

# print("\n Token usage:")
# print("Prompt Tokens: ", response.usage.prompt_tokens)
# print("Completion Tokens: ", response.usage.completion_tokens)
# print("Total Tokens: ", response.usage.total_tokens)


# print("==========with system============")
# response = client.chat.completions.create(
#     model = "gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a precise AI instructor"},
#         {"role": "user", "content": "Explain Hallucination in one sentence in AI context."}
#     ],
# )

# print("\n With System:")
# print(response.choices[0].message.content)

# print("\n Token usage:")
# print("Prompt Tokens: ", response.usage.prompt_tokens)
# print("Completion Tokens: ", response.usage.completion_tokens)
# print("Total Tokens: ", response.usage.total_tokens)



""" print("==========with constraints============")
response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Explain AI."}
    ],
    temperature=0.0,
    max_tokens=40
)

print("\n With constraints:")
print(response.choices[0].message.content) """



print("==========with top_p============")
response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Write a creative line for my startup"}
    ],
    temperature=1.0,
    top_p=0.5
)

print("\n With constraints:")
print(response.choices[0].message.content)

print("\n Token usage:")
print("Prompt Tokens: ", response.usage.prompt_tokens)
print("Completion Tokens: ", response.usage.completion_tokens)
print("Total Tokens: ", response.usage.total_tokens)

# Temperature controls variability, not truth.
