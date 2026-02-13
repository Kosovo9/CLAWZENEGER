
import chromadb
from chromadb.config import Settings
import os

class ChromaMemory:
    def __init__(self, collection_name="default"):
        host = os.getenv("CHROMA_HOST", "chromadb")
        port = int(os.getenv("CHROMA_PORT", "8000"))
        
        # In a real scenario you might need retry logic here
        self.client = chromadb.HttpClient(
            host=host, 
            port=port, 
            settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(collection_name)

    def add(self, doc_id: str, data: dict, metadata: dict = None):
        # Convert data dict to string representation for the document content
        text_content = str(data)
        
        self.collection.add(
            documents=[text_content],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )

    def search(self, query: str, n_results=5):
        return self.collection.query(
            query_texts=[query], 
            n_results=n_results
        )
