import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# Load the AI embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def split_into_chunks(text, chunk_size=120, overlap=30):
    """Split document text into smaller pieces."""

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_search_index(documents):
    """Create searchable embeddings from uploaded documents."""

    all_chunks = []
    metadata = []

    for document in documents:
        filename = document["filename"]
        text = document["text"]

        chunks = split_into_chunks(text)

        for chunk in chunks:
            all_chunks.append(chunk)
            metadata.append({"filename": filename})

    if not all_chunks:
        return None, [], []

    embeddings = model.encode(
        all_chunks,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = np.asarray(embeddings, dtype=np.float32)

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    return index, all_chunks, metadata


def search_documents(question, index, chunks, metadata, top_k=3):
    """Find document sections most relevant to a question."""

    if index is None or not chunks:
        return []

    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype=np.float32,
    )

    number_of_results = min(top_k, len(chunks))

    scores, indices = index.search(
        question_embedding,
        number_of_results,
    )

    results = []

    for score, chunk_index in zip(scores[0], indices[0]):
        if chunk_index < 0:
            continue

        results.append({
            "text": chunks[chunk_index],
            "filename": metadata[chunk_index]["filename"],
            "page": None,
            "score": float(score),
        })

    return results
