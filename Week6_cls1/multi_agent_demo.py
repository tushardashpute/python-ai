# multi_agent_demo.py
# Toy multi-agent coordinator: two agents (retriever + summarizer) exchange data via a coordinator.


def retriever(query):
    # pretend retrieval
    return "Document: Refunds are allowed within 30 days."


def summarizer(doc):
    # pretend summarization
    return "You can request a refund within 30 days."


def coordinator(query):
    doc = retriever(query)
    summary = summarizer(doc)
    return {"query": query, "doc": doc, "summary": summary}


if __name__ == "__main__":
    print(coordinator("How long for refund?"))
