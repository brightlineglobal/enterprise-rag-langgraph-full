def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if not text:
        return []
    cleaned = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    chunks: list[str] = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunk = cleaned[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(cleaned):
            break
        start = max(0, end - overlap)
    return chunks
