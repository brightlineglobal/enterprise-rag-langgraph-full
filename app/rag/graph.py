from langgraph.graph import StateGraph, END
from app.core.config import settings
from app.rag.prompts import ANSWER_PROMPT, QUERY_REWRITE_PROMPT
from app.rag.state import RAGState
from app.services.db_service import search_documents
from app.services.gemini_service import gemini_service
from app.services.reranker_service import rerank

def rewrite_query(state: RAGState) -> dict:
    prompt = QUERY_REWRITE_PROMPT.format(question=state["question"])
    rewritten = gemini_service.generate_text(prompt).strip() or state["question"]
    return {"rewritten_question": rewritten}

def retrieve_docs(state: RAGState) -> dict:
    embedding = gemini_service.embed_text(state["rewritten_question"])
    docs = search_documents(embedding, settings.retrieval_limit, state.get("access_groups") or [])
    return {"retrieved_docs": docs}

def rerank_docs(state: RAGState) -> dict:
    docs = rerank(state["question"], state["retrieved_docs"], settings.rerank_limit)
    return {"reranked_docs": docs}

def generate_answer(state: RAGState) -> dict:
    if not state["reranked_docs"]:
        return {"answer": "I could not find this in the knowledge base."}

    blocks = []
    for i, doc in enumerate(state["reranked_docs"], start=1):
        metadata = doc.get("metadata") or {}
        chunk_text = doc.get("chunk_text") or ""
        blocks.append(f"""
[Source {i}]
File: {doc.get('source_file')}
Title: {doc.get('title')}
Metadata: {metadata}
Content:
{chunk_text}
""")

    prompt = ANSWER_PROMPT.format(context="\n\n".join(blocks), question=state["question"])
    return {"answer": gemini_service.generate_text(prompt).strip()}

workflow = StateGraph(RAGState)
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("retrieve_docs", retrieve_docs)
workflow.add_node("rerank_docs", rerank_docs)
workflow.add_node("generate_answer", generate_answer)
workflow.set_entry_point("rewrite_query")
workflow.add_edge("rewrite_query", "retrieve_docs")
workflow.add_edge("retrieve_docs", "rerank_docs")
workflow.add_edge("rerank_docs", "generate_answer")
workflow.add_edge("generate_answer", END)
rag_graph = workflow.compile()
