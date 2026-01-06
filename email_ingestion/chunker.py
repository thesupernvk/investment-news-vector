def chunk_email(
    text: str,
    max_chars: int = 2000,
    overlap: int = 200
):
    """
    Chunk email content intelligently with overlap
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) <= max_chars:
            current += para + "\n\n"
        else:
            chunks.append(current.strip())
            current = para + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    # Add overlap
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            final_chunks.append(chunk)
        else:
            overlap_text = chunks[i - 1][-overlap:]
            final_chunks.append(overlap_text + "\n\n" + chunk)

    return final_chunks
