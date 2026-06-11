from langchain_core.messages import FunctionMessage
from langchain_groq import ChatGroq
from app.vector.pinecone_store import SecureVectorStoreManager
from app.config import settings

vector_manager = SecureVectorStoreManager()

async def erp_auditor_node(state: dict):
    invoice_id = state.get("target_invoice_id", "UNKNOWN")
    mock_db_extraction = f"[DB_RESULT] Invoice {invoice_id} shows Amount: 45,000 INR; Vendor: TechCorp."
    
    llm = ChatGroq(model="llama3-70b-8192", temperature=0, groq_api_key=settings.GROQ_API_KEY)
    response = llm.invoke([FunctionMessage(name="erp_database_lookup", content=mock_db_extraction)] + list(state["messages"]))
    
    return {
        "messages": [response],
        "reconciliation_status": "DB_VERIFIED"
    }

async def compliance_specialist_node(state: dict):
    latest_msg = state["messages"][-1].content if state["messages"] else ""
    
    compliance_rules = await vector_manager.secure_query_policies(
        query=latest_msg,
        clearance_level=state.get("clearance_level", "L1"),
        department=state.get("department", "FINANCE")
    )
    
    llm = ChatGroq(model="llama3-70b-8192", temperature=0, groq_api_key=settings.GROQ_API_KEY)
    system_input = f"Corporate Compliance Guidelines Found:\n{compliance_rules}\n\nAssess validity:"
    
    response = llm.invoke([FunctionMessage(name="vector_store_policy_lookup", content=system_input)] + list(state["messages"]))
    
    return {
        "messages": [response],
        "reconciliation_status": "COMPLIANCE_CHECKED"
    }