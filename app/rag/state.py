from typing import TypedDict, Any

class RAGState(TypedDict):
    question: str
    user_id: str | None
    department: str | None
    access_groups: list[str]
    rewritten_question: str
    retrieved_docs: list[dict[str, Any]]
    reranked_docs: list[dict[str, Any]]
    answer: str
