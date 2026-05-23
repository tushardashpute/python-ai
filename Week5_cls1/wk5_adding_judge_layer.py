from pathlib import Path 
import json 
from typing import List, Dict 
from openai import OpenAI
from pydantic import BaseModel 
import numpy as np 
from pypdf import PdfReader


client = OpenAI()
BASE_DIR = Path(__file__).resolve().parent 
RESUME_DIR = BASE_DIR
# if you want to create sep dir, then for eg resumes/ - BASE_DIR/"resumes"

JOB_DESCRIPTION = """
We are hiring a Python Automation Engineer to design, maintain, and improve automation frameworks for API,
UI, and workflow testing. The ideal candidate is strong in Python scripting, debugging, REST API validation, Selenium or UI automation, and maintainable automation design.
Nice to have : CI/CD, LLM exposure, LongChain basics, vector database familiarity, and cloud basics.
"""


RESUME_FILES = [

    "Candidate_Ananya_Patel.pdf",
    "Candidate_Daniel_Lee.pdf",
    "Candidate_Michael_Chen.pdf",
    "Candidate_Sarah_James.pdf",
]



class ResumePlan(BaseModel):
    role_title: str 
    must_have_skills: List[str] # list of strings. can use list[str]
    nice_to_have_skills: List[str]
    reason: str 



'''

This is the schema for the planner output 


'''   

class CandidateMatch(BaseModel):
    candidate_name: str 
    match_score: float 
    matched_skills: List[str]
    possible_gaps: List[str]
    summary: str 
    recommendation: str 

'''
this is the schema for the shortlisted candidate. 
For each canidate, the llm returns:
    name
    match score
    what skills matched
    what gaps exxist
    summary
    recommendation

This is actually going to make the final output more production-like.

'''


class ShortListOuput(BaseModel):
    job_title: str 
    top_candidates: List[CandidateMatch]


'''
raw= resoon.choice[o]
cleaned = clean_raw_data
data=json.loads(cleaned)

return only json format 

each field is of the right type
["python","UI","API Automation"]

contract
ResumePlan (BaseModel)
    role_title: str 
    must_have_skills: List[str] # list of strings. can use list[str]
    nice_to_have_skills: List[str]
    reason: str 

    
Pydantic is a class-based schema and most importantly validation system.

later in the program we can access this as
object.attributes.

plan=ResumePlan()
plan.nice_to_have_skills 

After our llm planning - we will get a json - older version
raw={

"role_title": "Python Automation engineer" - null
must_have_skills: List[str] # list of strings. can use list[str]
nice_to_have_skills: List[str]
reason: str 
}


Benefits:
missing field - imm validation error is raised
wrong type - imm validation error is raised
nested structure - can be checked too.
cleaner code afterwards - that can be used as an input to the next stage without worrying.
coz if "ANYTHING" not matching the schema fails - its going to raise an error and stop processing. 

'''


class CandidateJudgement(BaseModel):
    candidate_name: str 
    evidence_grounded: bool 
    matched_skills_correct: bool
    gaps_reasonable: bool
    judge_summary: str 
    recommendation_reasonable: bool 
    confidence: float


class EvaluationReport(BaseModel):
    overall_verdict: str 
    strongest_candidate: str 
    concerns: List[str]
    candidate_judgements: List[CandidateJudgement]



def clean_json_output(output):
    output = output.strip()

    if output.startswith("```json"):
        output = output[len("```json"):].strip()
    elif output.startswith("```"):
        output = output[len("```"):].strip()

    if output.endswith(("```")):
        output = output[:3].strip()

    return output 


def load_pdf_text(file_path:Path) -> str:

    reader = PdfReader(str(file_path))

    full_text = ""

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if  text:
            full_text += f"\n -----PAGE {page_num} ---\n{text}\n"
    return full_text




def chunk_text(text:str, chunk_size:int=500) -> List[str]:

    chunks = []
    for i in range(0,len(text),chunk_size):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
    return chunks


# A list of smaller chunks is returned.


def get_embedding(text:str) -> List[float]:

    response = client.embeddings.create(

        model= 'text-embedding-3-small',
        input=text
    )

    return response.data[0].embedding 


def cosine_similarity(a,b) -> float:
    a=np.array(a,dtype=float)
    b=np.array(b,dtype=float)

    return float(np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))) 



def create_plan(job_description: str) -> ResumePlan:

    prompt = f"""
Return ONLY valid JSON.
Do not include markdown.
Do not add explanations before or after the JSON.

Analyze this job description and extract a hiring plan. 

Job description:
{job_description}

Use exactly this schema:

{{
    "role_title": "string", 
    "must_have_skills": ["string"], 
    "nice_to_have_skills": ["string"], 
    "reason": "string"
}}

"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0
    )

    raw=response.choices[0].message.content
    cleaned=clean_json_output(raw)
    return ResumePlan.model_validate_json(cleaned)



def build_resume_vector_store(resume_files:List[str],chunk_size: int=500) -> List[Dict]:
    vector_store=[]
    for file_name in resume_files:
        pdf_path = RESUME_DIR/file_name
        pdf_text = load_pdf_text(pdf_path)
        chunks = chunk_text(pdf_text,chunk_size=chunk_size)
        candidate_name = file_name.replace(".pdf","").replace("Candidate_","").replace("_"," ")
        for i, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            vector_store.append({

                "candidate_name": candidate_name,
                "resume_file": file_name,
                "chunk_id": i,
                "text" : chunk,
                "embedding": emb 
            })

    return vector_store


def retrieve_candidate_chunks(query: str, vector_store:List[Dict], k:int=8) -> List[Dict] :
    query_embedding = get_embedding(query)

    scored = []

    for item in vector_store:
        score = cosine_similarity(query_embedding,item["embedding"])
        scored.append({
            "candidate_name": item["candidate_name"],
            "resume_file": item["resume_file"],
            "chunk_id": item["chunk_id"],
            "text" : item["text"],
            "score": round(score,4)
        })
    scored.sort(key=lambda x:x["score"],reverse=True)
    return scored[:k]


def aggregate_by_candidate(retrieved_chunks:List[Dict]) ->List[Dict]:

    grouped ={}
    for item in retrieved_chunks:
        name = item["candidate_name"]
        grouped.setdefault(name,{
            "candidate_name": name,
            "resume_file": item["resume_file"],
            "scores" : [],
            "chunks": []
        })
        grouped[name]["scores"].append(item["score"])
        grouped[name]["chunks"].append(item["text"])

    candidates = []
    for data in grouped.values():
        avg_score = sum(data["scores"]) / len(data["scores"])
        max_score = max(data["scores"])
        blended_score = round((avg_score * 0.6 ) + (max_score * 0.4),4)
        candidates.append({
            "candidate_name": data["candidate_name"],
            "resume_file": data["resume_file"],
            "match_score" : blended_score,
            "evidence": data["chunks"][:3]

        })

    candidates.sort(key=lambda x:x["match_score"],reverse=True)
    return candidates


'''
Candidata A might have: one very strong matching chunk(skill) while several "decent" matching chunks
avg_score - how consistently good the candidate's retrieved chunks are
max_score = how strong the single best matching chunk was

scores = [0.81,0.77,0.70]
avg_Score = 0.78

max_score=[0.92,0.50,0.48]
max_score=0.92

max_score = [0.81,0.75,.7]
max = 0.81


'''


def summarize_top_candidates(plan:ResumePlan, candidates: List[Dict], top_n: int=3) -> ShortListOuput:

    prompt = f"""


Return ONLY valid JSON.
Do not include markdown.
Do not add explanations before or after the JSON.

You are an AI resume-matching copilot.
Use the plan and evidence below to create a shortlist summary.

Plan:
{plan.model_dump_json(indent=2)}

Candidates:
{json.dumps(candidates[:top_n], indent=2)}

Use exactly this schema:
{{

  "job_title": "string",
  "top_candidates": [
    {{
      "candidate_name":"string",
      "match_score":0.0,
      "matched_skills": ["string"],
      "possible_gaps": ["string"],
      "summary": "string",
      "recommendation": "Shortlist | Maybe | Weak fit"

    }}
 ]

}}

"""
    response = client.chat.completions.create(

        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0
    )

    raw=response.choices[0].message.content
    cleaned=clean_json_output(raw)
    return ShortListOuput.model_validate_json(cleaned)


# LLM-AS-A-JUDGE EVALUATION Layer

def eval_shortlist_with_judge(plan:ResumePlan,candidate_rankins:List[Dict], shortlist: ShortListOuput) -> EvaluationReport:
    
    prompt = F"""
Return ONLY valid JSON.
Do not include markdown.
Do not add explanations before or after the JSON.

You are an AI evaluation judge.

You job is to evaluate whether the shortlist is well supported by the evidence.

Important:
- Judge the shortlist fairly.
- Check whether the matched skills are supported by evidence.
- Check whether the gaps are reasonable.
- Check whether the recommendation level makes sense.
- If something is weak or overstated, mention it in concerns.

Hiring plan:
{plan.model_dump_json(indent=2)}

Candidate Rankings with evidence:
{json.dumps(candidate_rankins,indent=2)}

Shortlist:
{shortlist.model_dump_json(indent=2)}

Use exactly this schema:
{{

  "overall_verdict": "string",
  "strongest_candidate": "string",
  "concerns": ["string"],
  "candidate_judgements": [
  
    {{
      "candidate_name":"string",
      "evidence_grounded":true,
      "matched_skills_correct": true,
      "gaps_reasonable": true,
      "judge_summary": "string",
      "recommendation_reasonable": true,
      "confidence" : 0.0

    }}
 ]

}}

"""
    
    response = client.chat.completions.create(

        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.0
    )

    raw=response.choices[0].message.content
    cleaned=clean_json_output(raw)
    return EvaluationReport.model_validate_json(cleaned)

# Take the top candidate evidence and turn it into a pydantic structure shortlist.
# Orchestator

def run_resume_mathcing_copilot():

    print("Step 1 : Creating Strucutred hiring plan.....")
    plan = create_plan(JOB_DESCRIPTION)
    print(plan.model_dump_json(indent=2))

    print("\nStep 2 : Building resume vector store.....")
    vector_store=build_resume_vector_store(RESUME_FILES, chunk_size=500)
    print(f"Vector store ready with {len(vector_store)} embedded resume chunks.")

    retrieved_query = " ".join(plan.must_have_skills + plan.nice_to_have_skills)

    print("\nStep 3 : Retreiving top candidate chunks.....")
    retrieved = retrieve_candidate_chunks(retrieved_query, vector_store, k=8)
    print(json.dumps(retrieved,indent=2))

    print("\nStep 4 : Aggregateing by candidate.....")
    candidate_rankins= aggregate_by_candidate(retrieved)
    print(json.dumps(candidate_rankins,indent=2))
    


    print("\nStep 5 : Creating a shortlist summary.....")
    shortlist = summarize_top_candidates(plan,candidate_rankins, top_n=3)
    print(shortlist.model_dump_json(indent=2))


    print("\nStep 6 : Evaluating shortlist with LLM-AS-A-JUDGE.....")
    evaluation_report = eval_shortlist_with_judge(plan,candidate_rankins, shortlist)
    print(evaluation_report.model_dump_json(indent=2))

    return {

        "plan": plan.model_dump(),
        "retrieved_chunks": retrieved,
        "candidate_rankins": candidate_rankins,
        "shortlist" : shortlist.model_dump(),
        "evaluation_report": evaluation_report.model_dump()
    }

if __name__ == "__main__":
    result=run_resume_mathcing_copilot()

#evaluation layer, AI self-critique, 


'''
JD -> Planner -> Retriueval -> Candindate Ranking -> Shortit Summary -> LLM-AS-A-JUDGE Evaluation -> Eval report 
self auditing its own o/p. 

5 evaluations things:
a. Recomm actually follow form the retrieved chunks or not.
b. skill alignmemnt
c. Gap accuracy
d. Recommendation quality - final shortlist /maybe/weak fit  - was it clearly identified.
e. Overall


A schema for judging one candidate which is class CandidateJudgemnet
A schema for full eval report which is class EvalReport
A new function that asks another llm to act like a judge.


'''

