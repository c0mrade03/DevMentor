from .file_collector import collect_target_files
from .embedding_generator import embedding_model
from .logger import logger
from . import config

import os
import argparse
import shutil
from git import Repo
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, NotebookLoader


def main():
    """
    Main function to run the data ingestion and vector store creation pipeline.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="Github url")
    args = parser.parse_args()

    repo_path = ""
    if args.url:
        storage_dir = "data/github_repos"
        repo_name = args.url.split("/")[-1].replace(".git", "")
        clone_path = os.path.join(storage_dir, repo_name)

        logger.info(f"Cloning repository from {args.url} into {clone_path}...")

        os.makedirs(storage_dir, exist_ok=True)

        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)
        Repo.clone_from(args.url, clone_path)
        repo_path = clone_path
        logger.info("Repository cloned successfully.")

    else:
        repo_path = config.TARGET_REPO_PATH
        logger.info(f"Using local repository at {repo_path}.")

    logger.info("Ingestion pipeline is starting.")

    # Collect files from the target repository
    collected_files = collect_target_files(
        repo_path)
    if not collected_files:
        logger.warning(
            "No files collected. Please check the TARGET_REPO_PATH and FILE_EXTENSIONS in config.py.")
        return
    logger.info(f"Collected {len(collected_files)} files.")

    # Process each file to create Langchain documents
    all_langchain_documents = []

    # Initialize a text splitter that we can use for all document types.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )

    for file_path in collected_files:
        # As a safety measure, skip files larger than 2MB to avoid memory issues.
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 2 * 1024 * 1024:  # 2MB limit
                logger.warning(
                    f"Skipping large file: {file_path} ({file_size / (1024*1024):.2f} MB)")
                continue
        except OSError:
            # This can happen for broken symlinks or other file system issues.
            logger.warning(
                f"Could not get size of file, skipping: {file_path}")
            continue

        logger.info(f"Processing file: {file_path}")
        file_extension = os.path.splitext(file_path)[1].lower()

        specially_loaded_documents = []
        if file_extension == '.ipynb':
            loader = NotebookLoader(file_path)
            specially_loaded_documents = loader.load()
        elif file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
            specially_loaded_documents = loader.load()
        elif file_extension == '.docx':
            loader = Docx2txtLoader(file_path)
            specially_loaded_documents = loader.load()
        else:
            loader = TextLoader(file_path, encoding='utf-8')
            try:
                specially_loaded_documents = loader.load()
            except Exception as e:
                logger.warning(
                    f"Skipping file {file_path} due to loading error: {e}")

        if specially_loaded_documents:
            chunk = text_splitter.split_documents(specially_loaded_documents)
            all_langchain_documents.extend(chunk)

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
    vector_store_dir = "data/vector_stores"
    store_save_path = os.path.join(vector_store_dir, repo_name)
    os.makedirs(store_save_path, exist_ok=True)
    vector_store.save_local(store_save_path)
    logger.info(f"Vector store saved locally at: {store_save_path}")


if __name__ == "__main__":
    main()
