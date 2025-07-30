import os
from . import config
from .logger import logger
from typing import List, Dict, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_file(file_path: str) -> List[Dict[str, Any]]:
    """Reads a file and splits its text into overlapping chunks.

    Args:
        file_path (str): The path to the file to be chunked.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary
                               represents a chunk with its metadata.
    """

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        logger.error(f"[ERROR] Skipping file {file_path}: {e}")
        return []

    file_name = os.path.basename(file_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_text(text)

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
    """Converts a list of chunk dictionaries into LangChain Document objects.

    Args:
        chunks (List[Dict[str, Any]]): The list of chunks from the chunk_file function.

    Returns:
        List[Document]: A list of LangChain Document objects.
    """

    langchain_documents = []
    
    for chunk in chunks:
        doc = Document(
            page_content=chunk['content'],
            metadata={"chunk_id": chunk['chunk_id'],
                      "source": chunk['source'], "file_name": chunk['file_name']}
        )
        langchain_documents.append(doc)

    return langchain_documents
