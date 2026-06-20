import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-lite")

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
    response = model.generate_content(prompt)
    return response.text