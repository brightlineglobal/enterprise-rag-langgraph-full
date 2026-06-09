import math
from collections import Counter

def tokenize(text: str) -> list[str]:
    return [t.strip(".,:;!?()[]{}\"'").lower() for t in text.split() if t.strip()]

def lexical_score(question: str, text: str) -> float:
    q_terms = Counter(tokenize(question))
    d_terms = Counter(tokenize(text))
    if not q_terms or not d_terms:
        return 0.0
    overlap = sum(min(q_terms[t], d_terms[t]) for t in q_terms)
    return overlap / math.sqrt(sum(q_terms.values()) * sum(d_terms.values()))

def rerank(question: str, docs: list[dict], limit: int) -> list[dict]:
    reranked = []
    for doc in docs:
        vector_score = float(doc.get("similarity") or 0.0)
        keyword_score = lexical_score(question, doc.get("chunk_text", ""))
        final_score = (0.75 * vector_score) + (0.25 * keyword_score)
        reranked.append({**doc, "rerank_score": final_score})
    return sorted(reranked, key=lambda item: item["rerank_score"], reverse=True)[:limit]
