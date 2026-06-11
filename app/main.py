import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Body, HTTPException, Request, status
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage

from app.config import settings
from app.agents.graph import compiled_swarm
from app.database import init_enterprise_db_schema

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Production lifespan orchestration replacing deprecated startup events
    await init_enterprise_db_schema()
    yield

app = FastAPI(
    title="Cognitive ERP Reconciliation Swarm Engine",
    version="1.0.0",
    description="Enterprise-grade asynchronous multi-agent engine for corporate procurement auditing.",
    lifespan=lifespan
)

@app.middleware("http")
async def ensure_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = correlation_id
    return response

@app.post("/api/v1/reconcile-invoice")
async def execute_swarm_reconciliation(
    invoice_id: str = Body(...),
    clearance: str = Body(...),
    dept: str = Body(...),
    raw_document_text: str = Body(...)
):
    execution_thread_id = f"thread_rec_{invoice_id}"
    runtime_config = {"configurable": {"thread_id": execution_thread_id}}
    
    initial_input_state = {
        "messages": [HumanMessage(content=f"Verify this transaction payload: {raw_document_text}")],
        "clearance_level": clearance,
        "department": dept,
        "target_invoice_id": invoice_id,
        "reconciliation_status": "INITIALIZED",
        "next_node": "supervisor"
    }
    
    try:
        final_output_state = await compiled_swarm.ainvoke(initial_input_state, config=runtime_config)
        terminal_msg = final_output_state["messages"][-1].content if final_output_state["messages"] else "No response generated."
        
        return {
            "status": "success",
            "thread_id": execution_thread_id,
            "reconciliation_state": final_output_state.get("reconciliation_status"),
            "resolution_summary": terminal_msg
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Swarm pipeline execution breakdown: {str(exc)}"
        )

@app.post("/api/v1/swarm/recover-state")
async def recover_halted_swarm_thread(
    thread_id: str = Body(...), 
    corrective_input: str = Body(...)
):
    runtime_config = {"configurable": {"thread_id": thread_id}}
    
    current_historical_state = await compiled_swarm.aget_state(runtime_config)
    if not current_historical_state or not current_historical_state.values:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Requested thread target context state history missing."
        )
        
    updated_state_input = {
        **current_historical_state.values,
        "messages": list(current_historical_state.values["messages"]) + [HumanMessage(content=corrective_input)],
        "next_node": "supervisor"
    }
    
    resumed_output_state = await compiled_swarm.ainvoke(updated_state_input, config=runtime_config)
    return {
        "status": "recovered",
        "thread_id": thread_id,
        "reconciliation_state": resumed_output_state.get("reconciliation_status"),
        "resolution_summary": resumed_output_state["messages"][-1].content
    }