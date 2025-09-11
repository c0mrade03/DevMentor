# This script handles the logic for reading files and splitting their content into smaller, manageable chunks.

import os
from . import config
from .logger import logger
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Reads a file and splits its text into overlapping chunks.

    Args:
        file_path (str): The path to the file to be chunked.

    Returns:
        A list of dictionaries, where each dictionary represents a chunk
        with its content and metadata.
    """
    # Try to read the file with UTF-8 encoding, skipping any files that cause errors.
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        logger.error(f"[ERROR] Skipping file {file_path}: {e}")
        return []

    # Get the base name of the file from its path.
    file_name = os.path.basename(file_path)

    # Initialize the text splitter with parameters from the config file.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # Split the document's text into a list of smaller strings (chunks).
    chunks = text_splitter.split_text(text)

    # Create a list of dictionaries, each representing a chunk with its metadata.
    return [
        {
            "chunk_id": i,
            "content": chunk,
            "source": file_path,
            "file_name": file_name
        }
        for i, chunk in enumerate(chunks)
    ]


def create_langchain_documents(chunks: List[Dict[str, Any]]) -> List[Document]:
    """
    Converts a list of chunk dictionaries into LangChain Document objects.

    Args:
        chunks (List[Dict[str, Any]]): The list of raw chunk dictionaries
                                       from the chunk_file function.

    Returns:
        A list of LangChain Document objects ready for embedding.
    """
    # Initialize an empty list to store the Document objects.
    langchain_documents = []
    
    # Loop through each raw chunk dictionary.
    for chunk in chunks:
        # Create a LangChain Document, mapping 'content' to the required 'page_content'.
        doc = Document(
            page_content=chunk['content'],
            metadata={"chunk_id": chunk['chunk_id'],
                      "source": chunk['source'], "file_name": chunk['file_name']}
        )
        langchain_documents.append(doc)

    # Return the final list of LangChain Document objects.
    return langchain_documents
