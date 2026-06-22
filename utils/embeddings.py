import google.generativeai as genai
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
            model="models/embedding-001",
            content=chunk,
            task_type=task_type
        )
        embeddings.append(result["embedding"])
    
    return np.array(embeddings)