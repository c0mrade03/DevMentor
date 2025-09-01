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
    # Load environment variables from .env file (for GOOGLE_API_KEY)
    load_dotenv()
    logger.info("Environment variables loaded.")

    # Load the FAISS vector store from local disk
    logger.info(f"Attempting to load vector store from path: '{config.VECTOR_STORE_PATH}'")
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

    prompt = PromptTemplate.from_template(config.RAG_PROMPT_TEMPLATE)

    # The RAG chain structure
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.info("RAG chain created.")

    return rag_chain
