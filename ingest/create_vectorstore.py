from .file_collector import collect_target_files
from .chunker import chunk_file, create_langchain_documents
from .embedding_generator import embedding_model
from .logger import logger
from . import config

import os
from langchain_community.vectorstores import FAISS


def main():
    """
    Main function to run the data ingestion and vector store creation pipeline.
    """
    logger.info("Ingestion pipeline is starting.")

    # Collect files from the target repository
    collected_files = collect_target_files(
        config.TARGET_REPO_PATH, config.FILE_EXTENSIONS)
    if not collected_files:
        logger.warning(
            "No files collected. Please check the TARGET_REPO_PATH and FILE_EXTENSIONS in config.py.")
        return
    logger.info(f"Collected {len(collected_files)} files.")

    # Process each file to create Langchain documents
    all_langchain_documents = []
    for file_path in collected_files:
        logger.info(f"Processing file: {file_path}")

        # Raw text chunk from the file
        raw_chunk = chunk_file(file_path)
        if not raw_chunk:
            continue

        # Convert raw chunk to langchain document object
        documents_for_file = create_langchain_documents(raw_chunk)

        # Add the documents from the current file to the main list
        all_langchain_documents.extend(documents_for_file)

    if not all_langchain_documents:
        logger.error("No langchain documents were created halting pipeline")
        return
    logger.info(
        f"Created a total of {len(all_langchain_documents)} documents (chunks).")

    # Create FAISS vector store from the documents
    logger.info("Creating FAISS vector store...")
    vector_store = FAISS.from_documents(
        documents=all_langchain_documents,
        embedding=embedding_model
    )
    logger.info("FAISS vector store created successfully")

    # Save the vector store locally
    vector_store.save_local(config.VECTOR_STORE_PATH)
    logger.info(f"Vector store saved locally at: {config.VECTOR_STORE_PATH}")


if __name__ == "__main__":
    main()
