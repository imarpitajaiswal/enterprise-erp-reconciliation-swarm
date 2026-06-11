from typing import Annotated, Sequence, TypedDict, Literal
import operator
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.config import settings
from app.agents.nodes import erp_auditor_node, compliance_specialist_node

class SwarmAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_node: str
    clearance_level: str
    department: str
    target_invoice_id: str
    reconciliation_status: str

def run_supervisor_router(state: SwarmAgentState):
    # Swapped to Groq's free Llama 3 70B model for high-tier reasoning
    llm = ChatGroq(model="llama3-70b-8192", temperature=0, groq_api_key=settings.GROQ_API_KEY)
    
    system_prompt = (
        "You are the Big 4 Executive Routing Supervisor. Analyze the current conversation state.\n"
        "If the invoice data needs database validation, route to 'erp_auditor'.\n"
        "If the document requires compliance policy checks via corporate rules, route to 'compliance_specialist'.\n"
        "If reconciliation assessment is complete, return 'FINISH'."
    )
    
    messages = [HumanMessage(content=system_prompt)] + list(state["messages"])
    response = llm.invoke(messages)
    
    content = response.content.strip()
    if "erp_auditor" in content:
        return {"next_node": "erp_auditor"}
    elif "compliance_specialist" in content:
        return {"next_node": "compliance_specialist"}
    else:
        return {"next_node": "FINISH"}

def create_compiled_swarm_graph():
    workflow = StateGraph(SwarmAgentState)
    workflow.add_node("supervisor", run_supervisor_router)
    workflow.add_node("erp_auditor", erp_auditor_node)
    workflow.add_node("compliance_specialist", compliance_specialist_node)
    workflow.set_entry_point("supervisor")
    
    def routing_condition(state: SwarmAgentState) -> Literal["erp_auditor", "compliance_specialist", END]:
        target = state.get("next_node", "FINISH")
        if target == "erp_auditor":
            return "erp_auditor"
        elif target == "compliance_specialist":
            return "compliance_specialist"
        return END

    workflow.add_conditional_edges("supervisor", routing_condition)
    workflow.add_edge("erp_auditor", "supervisor")
    workflow.add_edge("compliance_specialist", "supervisor")
    
    memory_layer = MemorySaver()
    return workflow.compile(checkpointer=memory_layer)

compiled_swarm = create_compiled_swarm_graph()