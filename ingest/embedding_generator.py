from . import config
from langchain_huggingface import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)



def generate_embeddings(documents, embedding_model):
    embeddings = embedding_model.embed_documents([doc.page_content for doc in documents])
    return embeddings
