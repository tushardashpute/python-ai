import random 

distributuion ={
    "Paris" : 0.91, 
    "London" : 0.03,
    "Berlin": 0.02,
}

choices = list(distributuion.keys())
weights = list(distributuion.values())

for _ in range(5):
    print("The capital of France is ",random.choices(choices,weights=weights)[0])



short_prompt = "Explain AI"
long_prompt = "Explain AI in simple temrs with 3 egs, and some analgoies and a short summary for software engineers"

print(len(short_prompt))
print(len(long_prompt))


