import chromadb
from .config import settings
from datetime import datetime
from typing import List, Dict

class NeilMemory:
    def __init__(self):
        self.client = None
        self.collection = None

    def _ensure_connected(self):
        if not self.client:
            try:
                self.client = chromadb.HttpClient(host=settings.CHROMADB_HOST, port=settings.CHROMADB_PORT)
                self.collection = self.client.get_or_create_collection(name="neilchat_history")
            except Exception as e:
                print(f"NeilMemory: Could not connect to ChromaDB: {e}")
                return False
        return True
    
    async def save_interaction(self, user_id: str, text: str, response: Dict):
        if not self._ensure_connected():
            return
        timestamp = datetime.now().isoformat()
        self.collection.add(
            documents=[text, response.get("mensaje", "")],
            metadatas=[{"user_id": user_id, "role": "user", "time": timestamp}, 
                       {"user_id": user_id, "role": "neil", "time": timestamp}],
            ids=[f"{user_id}_u_{timestamp}", f"{user_id}_n_{timestamp}"]
        )
    
    async def get_recent(self, user_id: str, limit: int = 10) -> List[Dict]:
        if not self._ensure_connected():
            return []
        # Simplificado para prototipo
        results = self.collection.get(
            where={"user_id": user_id},
            limit=limit
        )
        # Convertir a formato de chat
        history = []
        if results['documents']:
            for i in range(len(results['documents'])):
                history.append({
                    "role": results['metadatas'][i]['role'],
                    "text": results['documents'][i],
                    "timestamp": results['metadatas'][i]['time']
                })
        return history
