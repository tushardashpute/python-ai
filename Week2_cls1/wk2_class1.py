from openai import OpenAI 

import os, json

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# response = client.chat.completions.create(
#     model = "gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Explain prompt engineering."}
#     ],
#     temperature=0.3,
#     max_tokens=150,
# )

# print(response.choices[0].message.content)
# print(response.usage)

'''
Prompt engineering is the process of designing and refining the input prompts given to language models, such as GPT-3 or similar AI systems, to elicit the most accurate, relevant, and useful responses. It involves crafting the wording, structure, and context of prompts to guide the model's output effectively. Here are some key aspects of prompt engineering:

1. **Clarity and Specificity**: A well-defined prompt helps the model understand exactly what is being asked. Vague or ambiguous prompts can lead
'''

'''
The problem is
    - hard to parse.
    - not consistent 
    - not reliable 

Text is hard to use in systems

Machines need a defined structure.


what is the solution? JSON ouptut is the sol
'''

# response = client.chat.completions.create(
#     model = "gpt-4o-mini",
#     messages=[
#         {"role": "system", "content": "You output only valid JSON"},
#         {"role": "user", "content": "Explain prompt engineering with keys: definition, cause, example"}
#     ],
#     temperature=0.0
# )

# print(response.choices[0].message.content)

""" {
  "definition": "Prompt engineering is the process of designing and refining input prompts to optimize the performance of AI models, particularly in natural language processing tasks. It involves crafting specific queries or instructions that guide the model to produce desired outputs.",
  "cause": "The need for prompt engineering arises from the inherent variability in AI model responses based on how questions or tasks are framed. By carefully constructing prompts, users can improve the relevance, accuracy, and creativity of the model's outputs, making it a crucial skill for effective interaction with AI systems.",
  "example": {
    "basic_prompt": "Tell me about the benefits of exercise.",
    "engineered_prompt": "List three specific benefits of regular exercise for mental health, and provide a brief explanation for each."
  }
} """


def validate_json(output):
    try:
        data = json.loads(output)
        return data 
    except json.JSONDecodeError:
        print("INVALID JSON")
        return None 
    
bad_output = '''


{
"definition": "Prompt engineering is the process of designing and refining input.",
"example": "Asking for "
}

'''

result=validate_json(bad_output)
print("Result: ", result)

'''
YAML vs JSON

yaml is a superset of json

JSON is how we talk to AI
YAML is how systems talk to infrastruture.
 

{
"app" :{
    "name" :"my-app",
    "replicas" : 3,
    "ports" : [80,444]
    }
}

vs
same thing in yaml

app :
    name :my-app
    replicas : 3
    ports :
     - 80
     - 444

'''

def clean_output(output):
    output=output.strip()

    if output.startswith("```json"):
        output=output[len["```json"]:].strip()
    
    elif output.startswith("```"):
        output=output[len["```"]:].strip()

    return output

def get_valid_json(prompt, retries=2):

    for attempt in range(retries):    
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                #{"role": "system", "content": "Respond ONLY in raw JSON"},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        output=response.choices[0].message.content
        print(f"====Raw output attempt {attempt +1 }======")
        print(output)

        cleaned_output=clean_output(output)

        try:
            data = json.loads(cleaned_output)
            return data 
        except json.JSONDecodeError as e:
            print(f"Retrying..attempt{attempt +1 }")
            print("the error,",e)
    return None


def explain_topic(topic):
    prompt=f"""
    Return ONLY valid JSON.
    Use exactly this schema and no extra top-level keys:
    {{
        "definition":"string",
        "real_world_example": "string",
        "use_case": "string:
    }}
    Topic:{topic}
    """
    data=get_valid_json(prompt)

    if not data:
        return{"error":"Invalid response"}
    
    return data 

topic =input("Enter a topic you'd like AI assistant to respond back with : ")


result= explain_topic(topic)
#print(result)


print(result["definition"])
print(result["real_world_example"])
print(result["use_case"])

#prompt="Explain prompt engineering with keys: definition, cause, example"

#data = get_valid_json(prompt)


'''
```json
{
  "definition": "Prompt engineering is the process of designing and refining input prompts to optimize the performance of AI models, particularly in natural language processing tasks. It involves crafting specific queries or instructions that guide the model to produce desired outputs.",
  "cause": "The need for prompt engineering arises from the inherent variability in AI model responses based on the input they receive. By carefully constructing prompts, users can influence the model's behavior, improve accuracy, and achieve more relevant and contextually appropriate results.",
  "example": {
    "basic_prompt": "Tell me about climate change.",
    "engineered_prompt": "Explain the causes and effects of climate change in a way that a 10-year-old can understand, and provide three examples of its impact on the environment."
  }
}
```


We did eth right, still AI can fail.

USer Input -> Prompt Template -> API CALL -> JSON output -> Validation layer (failed here) -> App logic

this is exatly how
chatbots work
ai tools or bots work
SaaS product work

AI becomes more usable when it is structured.
AI becomes reliable when validated.
AI becomes a product when systemized correctly.

'''


'''
User input (prompt engineering) -> Prompt(converted to structured instructions) -> LLM (unreliable) -> Cleaning Layer -> Validation Layer -> Retry Layer -> Final output (reliable)

This is an AI system

'''