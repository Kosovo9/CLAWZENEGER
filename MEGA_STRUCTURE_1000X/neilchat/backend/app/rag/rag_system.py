import os
import chromadb
from chromadb.config import Settings
import logging
from typing import List, Dict, Optional
import hashlib
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("JOANNA_RAG_3000")

class RAGSystem:
    """Núcleo de memoria a largo plazo para Joanna con soporte multiformato"""
    
    def __init__(self):
        self.chroma_host = os.getenv("CHROMA_HOST", "chromadb")
        self.chroma_port = int(os.getenv("CHROMA_PORT", 8000))
        self.client = None
        self.collection = None

    async def initialize(self):
        """Conecta con la base de datos de vectores"""
        try:
            self.client = chromadb.HttpClient(host=self.chroma_host, port=self.chroma_port)
            self.collection = self.client.get_or_create_collection(
                name="joanna_knowledge",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("📚 RAG System Operativo (ChromaDB).")
        except Exception as e:
            logger.error(f"❌ Error conectando a ChromaDB: {e}")

    async def ingest_pdf(self, pdf_path: str):
        """Extrae e indexa un PDF"""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page in doc:
                text += page.get_text()
            await self.add_text(text, {"source": pdf_path, "type": "pdf"})
        except Exception as e:
            logger.error(f"❌ Error procesando PDF {pdf_path}: {e}")

    async def ingest_url(self, url: str):
        """Extrae e indexa contenido de una URL"""
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            await self.add_text(text, {"source": url, "type": "url"})
        except Exception as e:
            logger.error(f"❌ Error procesando URL {url}: {e}")

    async def add_text(self, text: str, metadata: Dict):
        """Añade fragmentos de texto a la memoria"""
        if not self.collection or not text.strip(): return
        
        # Split text into chunks (simplified for now)
        chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
        for i, chunk in enumerate(chunks):
            doc_id = hashlib.md5(f"{metadata.get('source')}:{i}".encode()).hexdigest()
            self.collection.add(
                documents=[chunk],
                metadatas=[metadata],
                ids=[doc_id]
            )
        logger.info(f"✅ Conocimiento inyectado desde {metadata.get('source')}")

    async def query(self, query_text: str, n_results: int = 2) -> str:
        """Busca en la memoria y devuelve el contexto más relevante"""
        if not self.collection: return ""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            if not results['documents'] or not results['documents'][0]:
                return ""
                
            context = "\n".join(results['documents'][0])
            return f"\n--- CONTEXTO DE MEMORIA LARGA ---\n{context}\n------------------------------\n"
        except Exception as e:
            logger.error(f"⚠️ Error en consulta RAG: {e}")
            return ""

# Singleton
rag_system = RAGSystem()
