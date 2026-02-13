import chromadb
import os

def get_client():
    host = os.getenv("CHROMA_HOST", "chromadb")
    return chromadb.HttpClient(host=host, port=8000)