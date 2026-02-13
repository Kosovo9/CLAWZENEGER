import chromadb
from chromadb.config import Settings
import os

class ChromaMemory:
    def __init__(self, host=None, port=8000, collection_name="default"):
        host = host or os.getenv("CHROMA_HOST", "chromadb")
        self.client = chromadb.HttpClient(host=host, port=port)
        self.collection = self.client.get_or_create_collection(collection_name)

    def add(self, doc_id: str, data: dict, metadata: dict = None):
        text = str(data)
        self.collection.add(
            documents=[text],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )

    def search(self, query: str, n_results=5):
        return self.collection.query(query_texts=[query], n_results=n_results)
