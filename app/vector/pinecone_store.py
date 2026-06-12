from pinecone import Pinecone
from langchain_pinecone import PineconeEmbeddings
from app.config import settings

class SecureVectorStoreManager:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        
        # Bypassing local memory limits by utilizing Pinecone's Serverless Inference
        self.embeddings = PineconeEmbeddings(
            model="multilingual-e5-large",
            pinecone_api_key=settings.PINECONE_API_KEY
        )

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