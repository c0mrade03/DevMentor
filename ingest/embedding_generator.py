# The script to generate embeddings (for testing purpose)
from . import config
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import torch
from ingest.logger import logger

device = "cpu"
if torch.cuda.is_available():
    device = "cuda"

logger.info(f"Embedding model is using device: {device}")
# Initialize the embedding model from Hugging Face once and reuse it across the application.
embedding_model = HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL_NAME, model_kwargs={'device': device})


def generate_embeddings(documents: List[Document], embedding_model: HuggingFaceEmbeddings) -> List[List[float]]:
    """Generates embeddings for a list of documents using a HuggingFace model.

    Args:
        documents (List[Document]): A list of LangChain Document objects.
        embedding_model (HuggingFaceEmbeddings): The embedding model instance.

    Returns:
        List[List[float]]: A list of embeddings, where each embedding is a list of floats.
    """

    # Generate embeddings for the page content of each document.
    embeddings = embedding_model.embed_documents(
        [doc.page_content for doc in documents])
    return embeddings
