FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir langchain-google-genai

COPY . .

CMD ["python", "query_rag.py"]