import os
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embeddings(chunks, task_type="retrieval_document"):
    if isinstance(chunks, str):
        chunks = [chunks]
    
    embeddings = []
    for chunk in chunks:
        result = client.models.embed_content(
            model="gemini-embedding-exp-03-07",
            contents=chunk
        )
        embeddings.append(result.embeddings[0].values)
    
    return np.array(embeddings)