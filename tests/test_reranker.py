from app.services.reranker_service import rerank

def test_rerank_orders_documents():
    docs = [
        {"chunk_text": "holiday schedule and payroll", "similarity": 0.5},
        {"chunk_text": "vpn access setup and approval", "similarity": 0.6},
    ]
    results = rerank("vpn access", docs, limit=2)
    assert "vpn" in results[0]["chunk_text"]
