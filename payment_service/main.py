
from fastapi import FastAPI, HTTPException
from dto import PaymentDTO
from models import Payment
from repositories import InMemoryPaymentRepository
from typing import List

app = FastAPI(
    title="Payment Service API",
    description="API for managing payments",
    version="1.0.0"
)
payment_repository = InMemoryPaymentRepository()

@app.post("/api/payments", response_model=PaymentDTO)
def create_payment(payment: PaymentDTO):
    new_payment = Payment(
        payment_id=payment.payment_id,
        order_id=payment.order_id,
        amount=payment.amount,
        payment_status=payment.payment_status,
        created_at=datetime.now()
    )
    return payment_repository.create_payment(new_payment)

@app.get("/api/payments/{payment_id}", response_model=PaymentDTO)
def get_payment(payment_id: str):
    payment = payment_repository.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.get("/api/orders/{order_id}/payments", response_model=List[PaymentDTO])
def get_order_payments(order_id: str):
    return payment_repository.get_payments_by_order_id(order_id)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
