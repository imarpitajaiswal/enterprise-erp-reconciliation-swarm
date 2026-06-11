from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

class SecureVectorStoreManager:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        # Using a free, local, enterprise-grade open-source embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    async def secure_query_policies(self, query: str, clearance_level: str, department: str, top_k: int = 3):
        query_vector = await self.embeddings.aembed_query(query)
        
        metadata_filter = {
            "clearance_required": {"$lte": clearance_level},
            "department": {"$in": [department, "GLOBAL"]}
        }
        
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            filter=metadata_filter,
            include_metadata=True
        )
        
        context_chunks = []
        for match in results.get("matches", []):
            if "text" in match.get("metadata", {}):
                context_chunks.append(match["metadata"]["text"])
                
        return "\n\n".join(context_chunks)