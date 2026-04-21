"""
Week 3 Class 1 - Structured AI Assistant Module
Reusable helper functions for structured responses and refinement
"""

import os
import json
from openai import OpenAI

class Wk3Cls1Assistant:
    """Structured AI Assistant - Refines RAG answers into JSON"""
    
    def __init__(self, system_role="You are a senior technical writer. You only output structured JSON."):
        """Initialize OpenAI client and system role"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_role = system_role
    
    # ===== STEP 1: GET USER INPUTS =====
    @staticmethod
    def get_user_inputs(prompt_text="Enter your query: ", temp_range=(0.2, 1.0), default_temp=0.5):
        """Handles terminal input for queries and temperature"""
        topic = input(prompt_text)
        try:
            temp_input = input(f"Temperature ({temp_range[0]} to {temp_range[1]}, default {default_temp}): ")
            temp = float(temp_input) if temp_input.strip() else default_temp
            if not (temp_range[0] <= temp <= temp_range[1]):
                print(f"Temperature should be between {temp_range[0]} and {temp_range[1]}. Defaulting to {default_temp}")
                temp = default_temp
        except ValueError:
            print("Invalid Input. Defaulting to 0.5")
            temp = default_temp
        return topic, temp
    
    # ===== STEP 2: RUN PROMPT =====
    def run_prompt(self, prompt, system_role=None, temperature=0.5, model="gpt-4o-mini", max_tokens=500):
        """Send prompt to OpenAI and get response"""
        system = system_role or self.system_role
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    
    # ===== STEP 3: REFINE TO STRUCTURED JSON =====
    def refine_to_structured_json(self, raw_answer, topic, temperature=0.5, output_keys=None):
        """Refines raw answer into structured JSON"""
        if output_keys is None:
            output_keys = ['ERROR', 'Description', 'Resolution', 'Debugging Commands']
        
        keys_str = ", ".join([f"'{k}'" for k in output_keys])
        
        prompt = f"""
Explain the following solution for the topic: '{topic}'.

Constraints:
- Under 150 words
- Beginner-friendly (no jargon)
- Return as JSON object with keys: {keys_str}

Raw Answer:
{raw_answer}
"""
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": self.system_role},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    
    # ===== STEP 4: CLEAN OUTPUT =====
    @staticmethod
    def clean_output(output):
        """Remove code block markers if present"""
        output = output.strip()
        
        if output.startswith("```json"):
            output = output[len("```json"):].strip()
        
        if output.endswith("```"):
            output = output[:-3].strip()
        
        return output
    
    # ===== STEP 5: PARSE AND VALIDATE JSON =====
    @staticmethod
    def parse_json_safely(json_str):
        """Safely parse JSON string"""
        try:
            cleaned = Wk3Cls1Assistant.clean_output(json_str)
            return json.loads(cleaned), True
        except json.JSONDecodeError as e:
            return {"error": str(e), "raw": json_str}, False
    
    # ===== STEP 6: FORMAT RESPONSE =====
    @staticmethod
    def format_response(json_data, include_sources=False, sources=None):
        """Format JSON response for display"""
        output = json.dumps(json_data, indent=4)
        
        if include_sources and sources:
            output += "\n\n" + "="*70
            output += "\nSOURCE ATTRIBUTION:"
            output += "\n" + "="*70
            for s in sources:
                output += f"\n- Chunk {s['chunk_id']} | Similarity: {s['score']:.4f}"
        
        return output
    
    # ===== STEP 7: CREATE POLICY RESPONSE =====
    def create_policy_response(self, policy_question, context, temperature=0.0):
        """Generate policy response with context"""
        prompt = f"""Use ONLY the context below to answer the policy question.
If the answer is not in the context, say "I don't have information about this policy."

Context:
{context}

Question:
{policy_question}

Provide a clear, concise answer."""
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
    
    # ===== STEP 8: REFINE POLICY RESPONSE =====
    def refine_policy_to_json(self, response_text, question, temperature=0.5):
        """Convert policy response to structured JSON"""
        prompt = f"""
Convert the following policy response into a structured JSON format.

Question: {question}
Response: {response_text}

Return a JSON object with keys:
- 'policy_topic': The main policy topic
- 'answer': The clear answer to the question
- 'details': Important details or conditions
- 'note': Any additional notes or disclaimers

Keep it beginner-friendly and concise."""
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a policy expert. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content


# ===== FOR TESTING ONLY =====
if __name__ == "__main__":
    """Example usage"""
    assistant = Wk3Cls1Assistant(system_role="You are a helpful policy assistant.")
    
    # Example: Get user input
    # topic, temp = assistant.get_user_inputs("What would you like to know? ")
    
    # Example: Run prompt
    # response = assistant.run_prompt("Explain refund policies in simple terms", temperature=0.7)
    # print(response)
    
    print("✅ Wk3Cls1Assistant module loaded successfully!")
    print("\nAvailable Methods:")
    print("- get_user_inputs()")
    print("- run_prompt()")
    print("- refine_to_structured_json()")
    print("- clean_output()")
    print("- parse_json_safely()")
    print("- format_response()")
    print("- create_policy_response()")
    print("- refine_policy_to_json()")
