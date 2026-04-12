import os, json

data = """```json{
  "DevOps_Concept_Jenkins": {
    "Definition": "Jenkins is an open-source automation server used for continuous integration and continuous delivery (CI/CD).",
    "Key_Features": [
      "Automates building, testing, and deploying applications.",
      "Supports plugins for integration with various tools.",
      "Facilitates collaboration between development and operations teams."
    ],
    "Example": "A team uses Jenkins to automatically run tests and deploy a web application to a staging environment whenever code is pushed to the repository."
  }
}```"""



# def clean_output(output):
#   if output.startswith("```json"):
#     output=output[len["```json"]:].strip()
  
#   elif output.startswith("```"):
#     output=output[len["```"]:].strip()
  
#   return output

def clean_output(output):
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

try:
  cleaned_data = clean_output(data)
  json_data = json.loads(cleaned_data)
  print(cleaned_data)
except json.JSONDecodeError:
  print("Invalid Json")
  