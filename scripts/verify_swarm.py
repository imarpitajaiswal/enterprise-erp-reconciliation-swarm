import asyncio
import json
import httpx

BASE_URL = "http://127.0.0.1:8000"

async def run_integration_pipeline():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=" * 70)
        print("⚡ STARTING ENTERPRISE SWARM INTEGRATION TESTING SUITE")
        print("=" * 70)

        # ----------------------------------------------------------------------
        # SYSTEM HEALTH CHECK
        # ----------------------------------------------------------------------
        try:
            health_response = await client.get(f"{BASE_URL}/health")
            print(f"[HEALTH CHECK] Status Code: {health_response.status_code}")
            print(f"[HEALTH CHECK] Payload: {health_response.text}\n")
        except httpx.ConnectError:
            print("❌ Error: FastAPI server is not running. Execute 'uvicorn app.main:app --reload' first.")
            return

        # ----------------------------------------------------------------------
        # SCENARIO A: END-TO-END HAPPY PATH RECONCILIATION
        # ----------------------------------------------------------------------
        print("🔹 SCENARIO A: Executing Standard Enterprise Invoice Reconciliation Flow...")
        payload_a = {
            "invoice_id": "INV-2026-001",
            "clearance": "L2",
            "dept": "FINANCE",
            "raw_document_text": "Invoice from TechCorp for cloud infrastructure migration deployment. Total amount billed is 45,000 INR. Cross-verify with recorded SAP transaction ledgers."
        }
        
        headers = {"X-Request-ID": "E2E-TEST-TRACKING-001"}
        
        response_a = await client.post(
            f"{BASE_URL}/api/v1/reconcile-invoice", 
            json=payload_a, 
            headers=headers
        )
        
        print(f"[SCENARIO A] Response Code: {response_a.status_code}")
        if response_a.status_code == 200:
            data = response_a.json()
            print(f"[SCENARIO A] Thread Allocated: {data.get('thread_id')}")
            print(f"[SCENARIO A] Final Status: {data.get('reconciliation_state')}")
            print(f"[SCENARIO A] Resolution Summary: {data.get('resolution_summary')}\n")
        else:
            print(f"[SCENARIO A] ❌ Execution Failed: {response_a.text}\n")

        # ----------------------------------------------------------------------
        # SCENARIO B: SWARM STATE FAULT-TOLERANCE AND RECOVERY CHECK
        # ----------------------------------------------------------------------
        print("🔹 SCENARIO B: Simulating Processing Interruption & Thread State Recovery...")
        
        # 1. Initiate an unverified transaction thread
        target_invoice_id = "INV-FAULT-999"
        payload_b_initial = {
            "invoice_id": target_invoice_id,
            "clearance": "L1",
            "dept": "PROCUREMENT",
            "raw_document_text": "Anomalous transaction document matching vendor code Vendor_X. Flagged for immediate human compliance review due to incomplete metadata fields."
        }
        
        print(f"[SCENARIO B] Initializing interrupted thread context: thread_rec_{target_invoice_id}")
        init_response = await client.post(
            f"{BASE_URL}/api/v1/reconcile-invoice", 
            json=payload_b_initial
        )
        
        if init_response.status_code == 200:
            init_data = init_response.json()
            allocated_thread = init_data.get("thread_id")
            print(f"[SCENARIO B] Thread Target Registered: {allocated_thread}")
            
            # 2. Emulate an operation manager injecting a corrective override into the exact same thread
            print(f"[SCENARIO B] Injecting corrective override context into Thread: {allocated_thread}")
            recovery_payload = {
                "thread_id": allocated_thread,
                "corrective_input": "Managerial override: Compliance clearance certificate validated manually via security portal. Force execution termination with an approved flag."
            }
            
            recovery_response = await client.post(
                f"{BASE_URL}/api/v1/swarm/recover-state", 
                json=recovery_payload
            )
            
            print(f"[SCENARIO B] Recovery Endpoint Response Code: {recovery_response.status_code}")
            if recovery_response.status_code == 200:
                recovery_data = recovery_response.json()
                print(f"[SCENARIO B] Post-Recovery State: {recovery_data.get('reconciliation_state')}")
                print(f"[SCENARIO B] Post-Recovery Resolution Summary: {recovery_data.get('resolution_summary')}")
            else:
                print(f"[SCENARIO B] ❌ State Recovery Failed: {recovery_response.text}")
        else:
            print(f"[SCENARIO B] ❌ Initial Execution Setup Failed: {init_response.text}")

        print("\n" + "=" * 70)
        print("⚡ ENTERPRISE INTEGRATION VERIFICATION RUN COMPLETE")
        print("=" * 70)

if __name__ == "__main__":
    # Ensure standard async loop orchestration matches our production standards
    asyncio.run(run_integration_pipeline())