def create_chunks(text, chunk_size=500, overlap=0):
    """
    Split text into overlapping chunks for better context retrieval.
    """
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        if chunk.strip():  # skip empty chunks
            chunks.append(chunk)

    return chunks
