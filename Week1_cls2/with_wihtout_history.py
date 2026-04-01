from openai import OpenAI 

import os 

api_key=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=api_key)


response_without_history = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": "what is my name? "}
    ]
)

response_with_history = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": "My name is Ankit. "},
        {"role": "assistant", "content": "Nice to meet you , Ankit "},
        {"role": "user", "content": "what is my name? "}
    ]
)

print("\n Without history:")
print(response_without_history.choices[0].message.content)
print("====================")
print("\n With history:")
print(response_with_history.choices[0].message.content)
print(response_with_history.usage)
print(response_without_history.usage)

'''
We are "simulating" memory like condition using context.
but context has limits
thats why architecture matters.

the model is stateless
the system creates state by replaying context

Every API call is basically like:
response =  model.predict(next_tokens | given_text )
given_text = your messages (prompts)


A prompt is the full structured input sent to the model, including system instructions, user input, and conversation history.

'''