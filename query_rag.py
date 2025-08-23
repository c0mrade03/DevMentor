import os
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from ingest.embedding_generator import embedding_model
from ingest.logger import logger
from ingest import config


def main():
    """
    Main function to load the vector store, build a RAG chain with Gemini, and query it.
    """
    # Load environment variables from .env file (for GOOGLE_API_KEY)
    load_dotenv()
    logger.info("Environment variables loaded.")

    # Load the FAISS vector store from local disk
    logger.info(f"Attempting to load vector store from path: '{config.VECTOR_STORE_PATH}'") # <-- ADD THIS LINE    
    db = FAISS.load_local(
        config.VECTOR_STORE_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
    logger.info("Vector store loaded successfully.")

    # Create a retriever from the vector store to fetch relevant documents
    retriever = db.as_retriever(search_kwargs={"k": 5})

    # LLM Initialization Google Gemini
    logger.info("Initializing Google Gemini model (gemini-2.5-flash)...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    # The prompt template remains the same
    template = """
    Answer the question based only on the following context:
    {context}

    Question: {question}
    """
    prompt = PromptTemplate.from_template(template)

    # The RAG chain structure remains the same
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.info("RAG chain created.")
    print("\n--- DevMentor AI Assistant ---")
    print("Ask questions about the codebase. Type 'quit' or 'exit' to end the session.")

    while True:
        # Ask a question and invoke the chain
        question = input("\nQuestion: ")
        if question.lower().strip() in ['quit', 'exit']:
            break
        logger.info(f"Invoking chain with question: '{question}'")
        answer = rag_chain.invoke(question)

        # Print the final answer
        print("\n--- Answer ---")
        print(answer)
        print("--------------\n")


if __name__ == "__main__":
    main()
