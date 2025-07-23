from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_file(file_path):

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"[ERROR] Skipping file {file_path}: {e}")
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_text(text)

    return [
        {
            "content": chunk,
            "source": file_path,
            "chunk_id": i
        }
        for i, chunk in enumerate(chunks)
    ]
