AI PDF Chatbot using RAG
📌 Overview

AI PDF Chatbot is a Retrieval-Augmented Generation (RAG) application built with Flask, FAISS, SQLite, and Google's Gemini API.

Users can upload PDF documents, ask questions about their content, and receive accurate, context-aware responses generated using a RAG pipeline.

The application extracts text from PDFs, converts text into embeddings, stores them in a FAISS vector database, retrieves the most relevant chunks based on the user's query, and uses Gemini to generate answers.

🚀 Features
🔐 User Authentication (Signup/Login)
📄 PDF Upload & Processing
✂️ Intelligent Text Chunking
🧠 Embedding Generation
🔎 FAISS Vector Similarity Search
🤖 Retrieval-Augmented Generation (RAG)
💬 Context-Aware Question Answering
🗂 Chat History Management
📱 Responsive User Interface
🏗 System Architecture
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
FAISS Vector Database
    ↓
Relevant Context Retrieval
    ↓
Gemini API
    ↓
Answer Generation
🛠 Tech Stack
Technology	Purpose
Python	Backend Development
Flask	Web Framework
SQLite	Database
FAISS	Vector Search
Gemini API	LLM Response Generation
HTML	Frontend
CSS	Styling
RAG	Retrieval-Augmented Generation
📂 Project Structure
AI-PDF-Chatbot/
│
├── app.py
├── utils/
│   ├── pdf_reader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── faiss_db.py
│   └── rag.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── signup.html
│
├── static/
│   ├── style.css
│   └── auth.css
│
├── uploads/
├── chatbot.db
├── requirements.txt
└── README.md
⚙️ Installation
Clone Repository
git clone https://github.com/santhoshworkspace26/RAG-Powered-PDF-Chatbot.git

cd AI-PDF-Chatbot-RAG
Create Virtual Environment
python -m venv venv
Activate Environment

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
🔑 Configure Gemini API

Create a .env file:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
▶️ Run Application
python app.py

Open:

http://127.0.0.1:5000
📸 Screenshots
Login Page
![Login Page](screenshots/login.png)
Signup Page
![Signup Page](screenshots/signup.png)
Home Dashboard
![Dashboard](screenshots/dashboard.png)
PDF Upload
![PDF Upload](screenshots/upload.png)
Chat Interface
![Chat Interface](screenshots/chat.png)
🔍 How RAG Works
User uploads a PDF document.
Text is extracted from the PDF.
Text is divided into smaller chunks.
Embeddings are generated for each chunk.
Embeddings are stored in a FAISS vector database.
User submits a question.
Relevant chunks are retrieved using similarity search.
Retrieved context is sent to Gemini API.
Gemini generates a context-aware response.
🎯 Future Improvements
Multi-PDF Support
Conversation Memory
PDF Summarization
Voice-Based Queries
Cloud Deployment
User Profile Management
👨‍💻 Author

Sandy

Aspiring AI/ML & Full Stack Developer

⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
