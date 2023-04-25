FROM python:3.9-slim
RUN pip install langchain openai faiss-cpu pypdf2 tiktoken
WORKDIR /app