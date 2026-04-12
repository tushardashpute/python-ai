from openai import OpenAI 

import os, json

api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def run_prompt(prompt):
    response = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
    return response.choices[0].message.content 

# prompt = "Explain APIs"

# print(run_prompt(prompt))


# print("=======================")
# prompt = """
# Explain APIs.

# Steps:
# 1. Give Definition
# 2. Give example
# 3. Keep it under 50 words
# """

# print(run_prompt(prompt))

print("=======================")

# def get_definition(topic):
#     return run_prompt(f"Define {topic} in 1 sentence ")

# def simplify(text):
#     return run_prompt(f"Simplify this for a beginner:\n {text} ")

# def add_example(topic):
#     return run_prompt(f"Give a real-world example of {topic}") # later change it to just -one example 


# topic = "API" # starting prompt 

# defintion = get_definition(topic)
# simple = simplify(defintion)
# example = add_example(topic)


# print("Definiton is: ", defintion)
# print("Simple : ",simple)
# print("Example: ", example)


# print("=======RAW=========")
# raw = run_prompt("Explain API's")
# print("Raw output: \n ", raw)

# def improve_answer(answer):
#     return run_prompt(f"""
# Improve this answer:
# - make it clearer
# - add structure 
# - remove ambiguity 
                      
# Answer:
# {answer}
# """)

# improved =  improve_answer(raw)

# print("=======Improved=========")
# print("Improved output: \n ", improved)

'''
=======RAW=========
Raw output: 
  An API, or Application Programming Interface, is a set of rules and protocols that allows different software applications to communicate and interact with each other. APIs define the methods and data formats that applications can use to request and exchange information, enabling developers to leverage the functionality of other software, services, or platforms without needing to understand their internal workings.

### Key Components of APIs:

1. **Endpoints**: URLs that represent specific functions or resources offered by the API. Each endpoint corresponds to a certain action or data retrieval.

2. **HTTP Methods**: APIs often use standard HTTP methods such as:
   - **GET**: Retrieve data from the server.
   - **POST**: Send new data to the server.
   - **PUT**: Update existing data.
   - **DELETE**: Remove data.

3. **Requests and Responses**: In an API interaction, a client application sends a request to an API endpoint, and the API processes this request and returns a response, typically in a structured format like JSON or XML.

4. **Authentication**: Many APIs require authentication to ensure that the requester has permission to access the requested resources. Common methods include API keys, OAuth tokens, and Basic Authentication.

5. **Rate Limiting**: APIs often implement restrictions on how many requests a client can make in a given time frame to prevent abuse and ensure quality of service.

### Types of APIs:

1. **Web APIs**: Accessible over the internet using standard web protocols (HTTP/HTTPS). Examples include RESTful APIs and GraphQL APIs.

2. **Library/Framework APIs**: Built as part of software libraries or frameworks that provide built-in functions for developers (e.g., jQuery API).

3. **Operating System APIs**: Allow applications to interact with the underlying operating system, such as file management or hardware communication (e.g., Windows API).

4. **Database APIs**: Enable communication between applications and databases, allowing for data retrieval and manipulation (e.g., SQL commands).

5. **Remote APIs**: Allow for communication between completely disparate systems over a network, often facilitated by web standards.

### Advantages of Using APIs:

- **Integration**: Easily integrate with other systems and services to enhance functionality without building everything from scratch.
- **Modularity**: Promote a modular architecture where different parts of a system can be developed, updated, and maintained independently.
- **Scalability**: Services can be scaled independently based on demand.
- **Ecosystem Growth**: Third-party developers can build applications that work with your service, expanding its ecosystem.

### Use Cases for APIs:

- **Social Media**: Allow applications to share content, fetch user profiles, or display social feeds.
- **Payment Processing**: Facilitate online transactions through services like PayPal or Stripe.
- **Data Integration**: Enable data sharing between different systems, like CRM systems and marketing automation tools.
- **Maps and Geolocation**: Use mapping services to embed maps or location services in applications.

In summary, APIs are essential components of modern software development, enabling seamless interaction between systems and empowering developers to build rich, integrated applications efficiently.
=======Improved=========
Improved output: 
  ### Understanding APIs: A Comprehensive Overview

An **API** (Application Programming Interface) is a set of defined rules and protocols that enables different software applications to communicate and interact. APIs facilitate the integration of functionalities from various software, services, or platforms, allowing developers to use their capabilities without needing insight into their internal processes.

---

### Key Components of APIs

1. **Endpoints**  
   - **Definition:** URLs that represent specific resources or functions.
   - **Functionality:** Each endpoint maps to a particular action or data retrieval.

2. **HTTP Methods**  
   APIs generally use standard HTTP methods to perform operations:
   - **GET:** Retrieve data from the server.
   - **POST:** Send new data to the server.
   - **PUT:** Update existing data.
   - **DELETE:** Remove data.

3. **Requests and Responses**  
   - **Process:** A client application sends a request to an API endpoint. 
   - **Response:** The API processes the request and returns a response, typically in structured formats like JSON or XML.

4. **Authentication**  
   - **Purpose:** Ensures secure access to resources.
   - **Common Methods:** Include API keys, OAuth tokens, and Basic Authentication.

5. **Rate Limiting**  
   - **Definition:** Restrictions on the number of requests a client can make within a specific time frame.
   - **Purpose:** Prevents abuse and maintains service quality.

---

### Types of APIs

1. **Web APIs**  
   - **Description:** Accessible over the internet using HTTP/HTTPS protocols.
   - **Examples:** RESTful APIs, GraphQL APIs.

2. **Library/Framework APIs**  
   - **Description:** Part of software libraries or frameworks.
   - **Examples:** jQuery API.

3. **Operating System APIs**  
   - **Description:** Facilitate interaction between applications and the operating system.
   - **Examples:** Windows API for file management and hardware communication.

4. **Database APIs**  
   - **Description:** Enable communication between applications and databases.
   - **Examples:** SQL commands for data manipulation.

5. **Remote APIs**  
   - **Description:** Allow communication between distinct systems over a network.
   - **Functionality:** Often utilize web standards for interoperability.

---

### Advantages of Using APIs

- **Integration:** Simplify the process of connecting with other systems and services, enhancing functionality without redundant development efforts.
- **Modularity:** Support a modular architecture, enabling independent development, updates, and maintenance of system components.
- **Scalability:** Allow services to scale independently according to demand.
- **Ecosystem Growth:** Enable third-party developers to build applications that enhance the core service, thereby expanding the ecosystem.

---

### Use Cases for APIs

- **Social Media:** Interface for sharing content, retrieving user profiles, and displaying social feeds.
- **Payment Processing:** Facilitate online transactions through services like PayPal or Stripe.
- **Data Integration:** Enable seamless data exchange between disparate systems such as CRM and marketing automation tools.
- **Maps and Geolocation:** Integrate mapping services to embed maps or geolocation features within applications.

---

### Conclusion

APIs are indispensable elements in modern software development, fostering efficient interactions among systems and empowering developers to create complex, integrated applications effortlessly. By understanding their structure and function, developers can leverage APIs to enhance their software and expand their capabilities.

'''


# def better_improve_answer(answer):
#     return run_prompt(f"""
# Rewrite this answer to be:
# - structured like documentation
# - easy to scan
# - beginner-friendly 
# - more professional tone
                      
# Answer:
# {answer}
# """)

# raw = run_prompt("Explain API's")
# better_improved =  better_improve_answer(raw)

# print("=======Next level=========")
# print("\n Next level output: \n ", better_improved)


'''
- draw inputs from specifically melting point
- find the overlapping datapoints if more than one 
- pka values-(use your own value)
'''


# Guardrail prompt

# prompt = """
# Explain APIs.

# Rules:
# - Do NOT exceed 50 words
# - Must include example
# - Must be beginner friendly
# - No jargon
# """

# print(run_prompt(prompt))


#strict guardrail
prompt = """
Explain Quantum computing.

Rules:
- If unsure, say "I dont know"
- Do NOT make up information
- Keep under 40 words
"""

print(run_prompt(prompt))