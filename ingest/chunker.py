import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"[ERROR] Skipping file {file_path}: {e}")
        return []

    file_name = os.path.basename(file_path)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
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


def create_langchain_documents(chunks):
    langchain_documents = []
    for chunk in chunks:
        doc = Document(
            page_content= chunk['content'],
            metadata= {"chunk_id": chunk['chunk_id'], "source": chunk['source'], "file_name": chunk['file_name']}
        )
        langchain_documents.append(doc)
    
    return langchain_documents

