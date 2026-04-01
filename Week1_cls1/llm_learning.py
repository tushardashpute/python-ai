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
# client =OpenAI() 


# response = client.chat.completions.create(
#     model = "gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "Answer clearly and concisely."},# we are telling this to the GPT 
#         {"role": "user", "content": "Explain Hallucination in AI in one sentence"}
#     ],
#     temperature=0.0
# )

# print(response.choices[0].message.content)

'''
sytem role = behavior controller
user role = This is your actual prompt question.

So now based on the above api call , the gpt model is receiving this:
System instrcution -> behave precisely 
User question -> answer correctly and precisely.

response struture
    choices-(is a list)
        message
            content

            [0] - first answer -> actual text context


'''

#print(response.usage)
'''
CompletionUsage(completion_tokens=29, prompt_tokens=27, total_tokens=56, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0))
prompt_tokens=27
completion_tokens=29
total_tokens = abvoe two 
total_tokens=56

tokens =cost 

'''
# print("Prompt Tokens: ", response.usage.prompt_tokens)
# print("Completion Tokens: ", response.usage.completion_tokens)
# print("Total Tokens: ", response.usage.total_tokens)


prompt = "Explain Hallucination in one sentence for software engineers"

for temp in [0.0,0.5,0.8]:
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
         {"role": "user", "content": prompt}
        ],
        temperature=temp
    )

    print(f"\n Temperature :{temp}")
    print(response.choices[0].message.content)
    print("Completion Tokens: ", response.usage.completion_tokens)
    print("Total Tokens: ", response.usage.total_tokens)

