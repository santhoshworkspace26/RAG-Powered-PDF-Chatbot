from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(chunks, task_type=None):
    embeddings = model.encode(chunks)
    return np.array(embeddings)import google.generativeai as genai
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_embeddings(chunks, task_type="retrieval_document"):
    if isinstance(chunks, str):
        chunks = [chunks]
    
    embeddings = []
    for chunk in chunks:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=chunk,
            task_type=task_type
        )
        embeddings.append(result["embedding"])
    
    return np.array(embeddings)