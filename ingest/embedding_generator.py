from . import config
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document


embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)



def generate_embeddings(documents: List[Document], embedding_model: HuggingFaceEmbeddings) -> List[List[float]]:
    """Generates embeddings for a list of documents using a HuggingFace model.

    Args:
        documents (List[Document]): A list of LangChain Document objects.
        model (HuggingFaceEmbeddings): The embedding model instance.

    Returns:
        List[List[float]]: A list of embeddings, where each embedding is a list of floats.
    """
    
    embeddings = embedding_model.embed_documents([doc.page_content for doc in documents])
    return embeddings
