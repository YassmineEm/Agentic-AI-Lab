from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="MCP Tool Server")


ORDERS_DB = {
    "12345": {"status": "Shipped", "delivery": "2 days", "tracking": "TRK123456"},
    "67890": {"status": "Processing", "delivery": "5 days", "tracking": "TRK789012"},
}

REFUNDS_DB = {}

class OrderRequest(BaseModel):
    order_id: str

class RefundRequest(BaseModel):
    order_id: str
    reason: str

@app.get("/")
def root():
    return {"message": "MCP Tool Server Running"}

@app.post("/tools/get_order_status")
def get_order_status(request: OrderRequest):
    """Récupérer le statut d'une commande"""
    order = ORDERS_DB.get(request.order_id)
    if order:
        return {
            "success": True,
            "order_id": request.order_id,
            **order
        }
    return {"success": False, "message": "Commande introuvable"}

@app.post("/tools/create_refund")
def create_refund(request: RefundRequest):
    """Créer une demande de remboursement"""
    refund_id = f"REF{len(REFUNDS_DB) + 1}"
    REFUNDS_DB[refund_id] = {
        "order_id": request.order_id,
        "reason": request.reason,
        "status": "pending"
    }
    return {
        "success": True,
        "refund_id": refund_id,
        "message": "Demande de remboursement créée"
    }

@app.post("/tools/create_support_ticket")
def create_support_ticket(request: dict):
    """Créer un ticket de support"""
    ticket_id = f"TICKET{hash(str(request)) % 10000}"
    return {
        "success": True,
        "ticket_id": ticket_id,
        "message": "Ticket créé, un agent vous contactera"
    }

if __name__ == "__main__":
    print("🚀 Démarrage du serveur MCP sur http://localhost:3333")
    uvicorn.run(app, host="0.0.0.0", port=3333)