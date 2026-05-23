# judge_example.py
# Simple automated judge that scores candidate outputs against a gold answer.

from typing import List


def score_answer(candidate: str, gold: str) -> float:
    # naive overlap score
    cand_tokens = set(candidate.lower().split())
    gold_tokens = set(gold.lower().split())
    if not gold_tokens:
        return 0.0
    return len(cand_tokens & gold_tokens) / len(gold_tokens)


def judge(candidates: List[str], gold: str):
    scores = [(c, score_answer(c, gold)) for c in candidates]
    return sorted(scores, key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    gold = "The refund period is 30 days"
    candidates = [
        "You have thirty days to request a refund",
        "Refunds are not available",
        "Return within 30 days"
    ]
    print(judge(candidates, gold))
