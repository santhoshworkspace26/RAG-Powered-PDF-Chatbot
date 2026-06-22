import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer(question, context):
    prompt = f"""
You are a helpful assistant. Answer the question using only the provided context.

Rules:
* Answer in 5 to 8 lines only.
* Be clear and concise.
* No bullet points, just plain paragraph.
* Do not add extra explanations or summaries.

Context:
{context}

Question:
{question}

Answer:
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text