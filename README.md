# 🤖 DevMentor: AI Software Architecture Assistant

**DevMentor** is a Retrieval-Augmented Generation (RAG) system designed to act as an AI assistant for developers.  
It helps users, especially those new to a project, understand complex software codebases by answering natural-language questions about architecture, code logic, and historical decisions.

---

## 🧠 Core Concept

Onboarding onto a new, large software project is a major challenge for developers.  
Finding out *why* a certain technology was chosen, *how* a specific module works, or *where* to start contributing can take days or weeks of digging through documentation and asking colleagues.

DevMentor solves this by ingesting an entire codebase—including source code, documentation (`.md`, `.pdf`, `.docx`), Jupyter Notebooks, and Architecture Decision Records (ADRs)—and making it conversationally accessible.  
It acts as an infinitely patient senior developer, ready to answer your questions and guide you through the project.

---

## ✨ Key Features (Current Phase)

- **Flexible Data Ingestion:** Ingests knowledge from either local repositories or directly from a public GitHub URL.  
- **Multi-Repository Support:** The application can manage and query multiple, distinct knowledge bases.  
- **Smart File Processing:** Uses a multi-layered filtering system to automatically ignore irrelevant files and a dispatcher to correctly parse various file types.  
- **Conversational Q&A:** Ask questions about the codebase in plain English and get detailed, context-aware answers.  
- **Intelligent RAG Pipeline:** Built with LangChain, using a FAISS vector store for efficient retrieval and the Google Gemini 2.5 Flash API for powerful generation.  
- **Persona-Driven AI:** The prompt is engineered to make the AI act as a helpful and patient mentor, capable of explaining concepts in a beginner-friendly way.  
- **Streaming Responses:** The user interface displays answers with a real-time "typewriter" effect for a responsive and modern user experience.  
- **Dockerized Environment:** The entire application is containerized using Docker and managed with Docker Compose, ensuring a consistent and reproducible setup for both the web app and a command-line interface.  
- **Interactive Web UI:** A clean and user-friendly web interface built with Streamlit, featuring a full chat history and a knowledge base management page.  
- **GPU Acceleration:** Provides an optional GPU-enabled installation path for faster ingestion and retrieval.

---

## 🛠️ Tech Stack

| Component | Technologies Used |
|------------|-------------------|
| **Backend & AI** | Python, LangChain, Google Gemini 2.5 Flash |
| **Vector Store** | FAISS (CPU & GPU versions) |
| **Embeddings** | Hugging Face Sentence Transformers (`BAAI/bge-small-en-v1.5`) |
| **Frontend** | Streamlit |
| **Deployment & Tooling** | Docker, Docker Compose, GitPython |

---

## 🚀 Getting Started

Follow these steps to set up and run **DevMentor** on your local machine.

### 🧩 Prerequisites

- [Git](https://git-scm.com/)  
- [Docker](https://www.docker.com/products/docker-desktop/)  
- [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)  
- *(Optional)* For GPU support: A compatible NVIDIA GPU with the appropriate drivers and CUDA toolkit installed.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/c0mrade03/DevMentor.git
cd DevMentor
```
### 2️⃣ Set Up Environment Variables

The application requires a **Google API key** to function.

1. Create a file named `.env` in the root of the project.  
2. Copy the contents of `.env.example` into your new `.env` file.  
3. Add your **Google Gemini API key** to the `.env` file.

Example `.env` file:
```bash
GOOGLE_API_KEY="your_google_api_key_here"
```
### 3️⃣ Installation

This project supports both **CPU-only** and **GPU-accelerated** environments.

#### 🖥️ Default Installation (CPU-only)

1. Create and activate a Python virtual environment:
    ```bash
   python3 -m venv venv_cpu
   source venv_cpu/bin/activate

2. Insall all required packages:
    ```bash
   pip install -r requirements.txt

#### ⚡ Optional: GPU Acceleration

1. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv_gpu
   source venv_gpu/bin/activate

2. Install the GPU-specific packages:
    ```bash
   pip install -r requirements_gpu.txt

### 4️⃣ Build a Knowledge Base

You must ingest a repository before you can ask questions.

#### Option A: From a GitHub URL (Recommended)

```bash
python -m ingest.create_vectorstore --url https://github.com/cookiecutter/cookiecutter
```

#### Option B: From a Local Path (Fallback)

If no URL is provided, the script will default to the path specified in `ingest/config.py`.

```bash
python -m ingest.create_vectorstore
```

### 5️⃣ Build the Docker Images

Build the necessary Docker images using Docker Compose:

```bash
docker compose build
```
## 🖥️ Usage

You can run DevMentor as either a **Streamlit web app** or a **command-line tool**.

### Running the Web Application

#### CPU Version

```bash
docker compose up app-cpu
```
Once the container is running, open your web browser and navigate to:  
**http://localhost:8501** (CPU version)

#### GPU Version

```bash
docker compose up app-gpu
```
For GPU, navigate to: **http://localhost:8502**

### Running the Command-Line Interface (CLI)

#### CPU Version

```bash
docker compose run --rm cli-cpu --repo <repo_name>
```
#### GPU Version

```bash
docker compose run --rm cli-gpu --repo <repo_name>
```
> Replace `<repo_name>` with the name of a folder inside `data/vector_stores/`.

---

## 🔮 Future Scope

- **Agentic Capabilities (MCP):** Give the AI "tools" to perform live actions, such as interacting with the GitHub API to find "Good First Issues" for new contributors.  
- **Conversational Memory:** Implement an explicit memory module to allow for more natural, multi-turn follow-up conversations.  
- **Source Citing:** Add a "Show Sources" feature in the UI to display the exact document chunks used to generate an answer.  
- **CI/CD Pipeline:** Implement a full GitHub Actions workflow for automated testing and linting.

---

## 📜 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.
