# temperature_demo.py
# Simple demo to show how "temperature" affects sampling from a probability distribution.
# Requires: numpy

import numpy as np


def softmax(logits, temperature=1.0):
    scaled = np.array(logits) / float(max(temperature, 1e-8))
    exps = np.exp(scaled - np.max(scaled))
    return exps / exps.sum()


def sample_from_logits(logits, temperature=1.0, n=1):
    probs = softmax(logits, temperature=temperature)
    return np.random.choice(len(logits), size=n, p=probs)


if __name__ == "__main__":
    logits = [2.0, 1.0, 0.1]  # an example un-normalized score for 3 tokens

    for temp in [0.0, 0.2, 0.5, 1.0]:
        if temp == 0.0:
            # deterministic: pick the argmax
            choice = int(np.argmax(logits))
            print(f"temperature={temp}: deterministic choice -> {choice}")
            continue

        counts = {0: 0, 1: 0, 2: 0}
        trials = 10000
        for _ in range(trials):
            c = sample_from_logits(logits, temperature=temp)[0]
            counts[c] += 1

        freqs = {k: v / trials for k, v in counts.items()}
        print(f"temperature={temp}: frequencies -> {freqs}")
