from app.services.chunking import chunk_text

def test_chunk_text_returns_chunks():
    chunks = chunk_text("a" * 2500, chunk_size=1000, overlap=100)
    assert len(chunks) == 3
    assert all(chunks)
