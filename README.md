DevMentor: AI Software Architecture Assistant 🤖
================================================

DevMentor is a Retrieval-Augmented Generation (RAG) system designed to act as an AI assistant for developers. It helps users, especially those new to a project, understand complex software codebases by answering natural-language questions about architecture, code logic, and historical decisions.

🧠 Core Concept
---------------

Onboarding onto a new, large software project is a major challenge for developers. Finding out _why_ a certain technology was chosen, _how_ a specific module works, or _where_ to start contributing can take days or weeks of digging through documentation and asking colleagues.

DevMentor solves this by ingesting an entire codebase—including source code, documentation, and Architecture Decision Records (ADRs)—and making it conversationally accessible. It acts as an infinitely patient senior developer, ready to answer your questions and guide you through the project.

✨ Key Features (Current Phase)
------------------------------

*   **Conversational Q&A:** Ask questions about the codebase in plain English and get detailed, context-aware answers.
    
*   **Intelligent RAG Pipeline:** Built with LangChain, using a FAISS vector store for efficient retrieval and the Google Gemini API for powerful generation.
    
*   **Persona-Driven AI:** The prompt is engineered to make the AI act as a helpful and patient mentor, capable of explaining concepts in a beginner-friendly way.
    
*   **Streaming Responses:** The user interface displays answers with a real-time "typewriter" effect for a responsive and modern user experience.
    
*   **Dockerized Environment:** The entire application is containerized using Docker and managed with Docker Compose, ensuring a consistent and reproducible setup for both the web app and a command-line interface.
    
*   **Interactive Web UI:** A clean and user-friendly web interface built with Streamlit, featuring a full chat history.
    

🛠️ Tech Stack
--------------

*   **Backend & AI:** Python, LangChain, Google Gemini 2.5 Flash
    
*   **Vector Store:** FAISS (Facebook AI Similarity Search)
    
*   **Embeddings:** Hugging Face Sentence Transformers (BAAI/bge-small-en-v1.5)
    
*   **Frontend:** Streamlit
    
*   **Deployment:** Docker & Docker Compose
    

🚀 Getting Started
------------------

Follow these steps to set up and run DevMentor on your local machine.

### Prerequisites

*   [Git](https://git-scm.com/)
    
*   [Docker](https://www.docker.com/products/docker-desktop/)
    
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)
    

### 1\. Clone the Repository

` git clone [https://github.com/c0mrade03/DevMentor.git](https://github.com/c0mrade03/DevMentor.git) `

` cd DevMentor   `

### 2\. Set Up Environment Variables

The application requires a Google API key to function.

*   Create a file named .env in the root of the project.
    
*   Copy the contents of .env.example into your new .env file.
    
*   Add your Google Gemini API key to the .env file.
    

` # Your .env file should look like this: `

` GOOGLE_API_KEY="your_google_api_key_here"   `

### 3\. Configure the Target Repository

Before building the knowledge base, you must specify which local repository you want to index.

* Open the file `ingest/config.py`.
* Modify the variables according to your preferences

**Example:**
` in ingest/config.py `

` TARGET_REPO_PATH = "../path/to/your/cloned-repo" (default is "../cookiecutter-django" that's the open source repo I have been experimenting with small shoutout to them)`

` You may change all the variables there. I know it's pretty inconvenient for now but I am working on automating them like dynamically selecting file extensions etc. For now please bear with it `

### 4\. Build the Vector Store (One-Time Setup)

Before you can ask questions, you need to process a repository into a vector store. This command ingests the code and creates the necessary index files.

_For this example, we will use the cookiecutter-django repository, which you should have downloaded in a directory adjacent to the DevMentor project._

` # From the DevMentor root directory, run: `

` python -m ingest.create_vectorstore  `

This process may take some time. It will create a vector\_store directory in the parent folder.

### 5\. Build the Docker Image

Build the devmentor image using Docker Compose.

`   docker compose build   `

🖥️ Usage
---------

You can run DevMentor as either a Streamlit web app or a command-line tool.

### Running the Web Application

This is the primary way to use DevMentor.

`   docker compose up app   `

Once the container is running, open your web browser and navigate to:**http://localhost:8501**

### Running the Command-Line Interface (CLI)

For quick tests or debugging, you can use the interactive CLI.

`   docker compose run --rm cli   `

🔮 Future Scope
---------------

This project has a clear roadmap for adding more powerful features:

*   **Advanced Data Ingestion:** Add support for cloning public GitHub repositories directly via a URL.
    
*   **Agentic Capabilities:** Give the AI "tools" to perform live actions, such as interacting with the GitHub API to find "Good First Issues" for new contributors.
    
*   **Conversational Memory:** Implement an explicit memory module to allow for more natural, multi-turn follow-up conversations.
    

📜 License
----------

This project is licensed under the MIT License.