from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(chunks, task_type=None):
    embeddings = model.encode(chunks)
    return np.array(embeddings)