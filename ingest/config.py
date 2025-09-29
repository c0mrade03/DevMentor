# Config file change according to your choice
import os

# Default repository path for local ingestion.
TARGET_REPO_PATH = "../cookiecutter-django"

# A list of directory names to completely ignore during the file collection process.
# This is crucial for skipping version control, virtual environments, and build artifacts.
IGNORE_DIRS = [
    ".git",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "build",
    "dist",
    "github_repos",  # To avoid re-indexing repos we have cloned
]

# A list of file extensions for common binary or non-text files to ignore.
# This provides a fast first-pass filter before the more robust content-based check.
IGNORE_EXTS = [
    # Compiled files
    ".pyc",
    ".so",
    ".exe",
    ".dll",
    ".jar",
    ".o",

    # Archives
    ".zip",
    ".tar.gz",
    ".rar",

    # Media files
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".svg",
    ".mp4",
    ".mov",
    ".avi",
    ".mp3",
    ".wav",

    # Other
    ".db",
    ".sqlite3",
    ".env", # Avoid indexing environment variables
]

# Path to the FAISS vector store, configurable via environment variable.
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "../vector_store")

# Maximum characters per text chunk.
CHUNK_SIZE = 500
# Overlap between consecutive text chunks.
CHUNK_OVERLAP = 100

# Hugging Face model for generating embeddings.
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# The prompt template that defines the AI's persona and instructions for the RAG chain.
RAG_PROMPT_TEMPLATE = """
You are DevMentor, a helpful and patient AI assistant for developers who are new to this project. Your main goal is to provide clear, step-by-step, beginner-friendly guidance.

Use the following retrieved context as your primary source of truth to answer the user's question.

If the context gives high-level steps (like 'Fork the repo'), you MUST use your own general software development knowledge to explain those steps in detail for a beginner (e.g., explain what forking is, provide a sample git command).

If the context does not contain the answer, you are allowed to say that the information is not in the repository's documentation and provide a typical answer based on your general knowledge (for example, suggesting 'pip install -r requirements.txt' if asked about dependencies).

Context:
{context}

Question: {question}
"""
