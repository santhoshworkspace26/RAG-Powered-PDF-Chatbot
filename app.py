from flask import Flask, render_template, request, redirect, url_for, session
import os
import sqlite3
import hashlib
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

from utils.pdf_reader import extract_text
from utils.chunker import create_chunks
from utils.embeddings import get_embeddings
from utils.faiss_db import FAISSDatabase
from utils.rag import generate_answer

faiss_store = {}

# ── Database ────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect("chatbot.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            pdf_name TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def get_history(user_id):
    conn = get_db()
    history = conn.execute(
        """SELECT id, question, answer, pdf_name, created_at
           FROM chat_history WHERE user_id = ?
           ORDER BY created_at DESC LIMIT 5""",
        (user_id,)
    ).fetchall()
    conn.close()
    return history

# ── Auth ─────────────────────────────────────────────────────
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not username or not email or not password:
            error = "All fields are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        else:
            try:
                conn = get_db()
                conn.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, hash_password(password))
                )
                conn.commit()
                return redirect(url_for("login"))

            except sqlite3.IntegrityError:
                error = "Username or email already exists."

            finally:
                if conn:
                    conn.close()
    return render_template("signup.html", error=error)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()  # Clear any old session
    error = None
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, hash_password(password))
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("home"))
        else:
            error = "Invalid email or password."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    response = redirect(url_for("login"))
    response.delete_cookie('session')
    return response


# ── Main ─────────────────────────────────────────────────────
@app.route("/")
@login_required
def home():
    history = get_history(session["user_id"])
    return render_template("index.html", history=history)


@app.route("/chat/<int:chat_id>")
@login_required
def view_chat(chat_id):
    conn = get_db()
    chat = conn.execute(
        "SELECT * FROM chat_history WHERE id = ? AND user_id = ?",
        (chat_id, session["user_id"])
    ).fetchone()
    conn.close()

    history = get_history(session["user_id"])

    if not chat:
        return redirect(url_for("home"))

    return render_template("index.html",
        answer=chat["answer"],
        question=chat["question"],
        upload_success=True,
        history=history
    )


@app.route("/upload", methods=["POST"])
@login_required
def upload_pdf():
    pdf_file = request.files["pdf"]
    if pdf_file.filename == "":
        return "No file selected"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], pdf_file.filename)
    pdf_file.save(filepath)
    session["pdf_name"] = pdf_file.filename

    text = extract_text(filepath)
    chunks = create_chunks(text, chunk_size=1500, overlap=300)
    embeddings = get_embeddings(chunks)

    db = FAISSDatabase(embeddings.shape[1])
    db.add_embeddings(embeddings)

    user_id = session["user_id"]
    faiss_store[user_id] = {"db": db, "chunks": chunks}

    print(f"Total Chunks: {len(chunks)}")

    history = get_history(user_id)
    return render_template("index.html", upload_success=True, history=history)


@app.route("/ask", methods=["POST"])
@login_required
def ask_question():
    question = request.form["question"]
    user_id = session["user_id"]
    history = get_history(user_id)

    store = faiss_store.get(user_id)
    if not store:
        return render_template("index.html",
            answer="Please upload a PDF first.",
            history=history
        )

    db = store["db"]
    chunks = store["chunks"]

    question_embedding = get_embeddings([question])[0]
    distances, indices = db.search(question_embedding, k=10)

    retrieved_chunks = [chunks[idx] for idx in indices[0] if idx < len(chunks)]
    context = "\n\n".join(retrieved_chunks)
    answer = generate_answer(question, context)

    conn = get_db()
    conn.execute(
        "INSERT INTO chat_history (user_id, question, answer, pdf_name) VALUES (?, ?, ?, ?)",
        (user_id, question, answer, session.get("pdf_name", "Unknown"))
    )
    conn.commit()
    conn.close()

    history = get_history(user_id)
    return render_template("index.html",
        answer=answer,
        question=question,
        upload_success=True,
        history=history
    )


if __name__ == "__main__":
    app.run(debug=True)