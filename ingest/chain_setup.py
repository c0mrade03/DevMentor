# This script is main engine of our code
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from ingest.embedding_generator import embedding_model
from ingest.logger import logger
from ingest import config


@st.cache_resource
def load_rag_chain():
    """
    Loads and configures the complete RAG chain.

    This function handles all the expensive setup operations, including loading the
    FAISS vector store and initializing the Gemini language model. It uses
    Streamlit's caching to ensure this setup runs only once.

    Returns:
        A runnable LangChain object representing the RAG chain.
    """
    # Load environment variables from .env file for the GOOGLE_API_KEY.
    load_dotenv()
    logger.info("Environment variables loaded.")

    if not os.path.exists(config.VECTOR_STORE_PATH):
        logger.warning(
            "Vector Store is not yet created.")
        return None
    # Load the FAISS vector store from the local disk.
    logger.info(
        f"Attempting to load vector store from path: '{config.VECTOR_STORE_PATH}'")
    db = FAISS.load_local(
        config.VECTOR_STORE_PATH,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )
    logger.info("Vector store loaded successfully.")

    # Create a retriever from the vector store to fetch relevant documents.
    retriever = db.as_retriever(search_kwargs={"k": 5})

    # Initialize the Google Gemini language model.
    logger.info("Initializing Google Gemini model...")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)

    # Create the prompt template from the config file.
    prompt = PromptTemplate.from_template(config.RAG_PROMPT_TEMPLATE)

    # Define the RAG chain using LangChain Expression Language (LCEL).
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.info("RAG chain created.")

    # Return the fully constructed RAG chain.
    return rag_chain
