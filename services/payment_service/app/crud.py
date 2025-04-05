from sqlalchemy.orm import Session
from app.models import Payment
from app.schemas import PaymentCreate, PaymentUpdate

def get_payment(db: Session, payment_id: int):
    """Récupère un paiement par son ID"""
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_payment_by_order(db: Session, order_id: int):
    """Récupère un paiement par l'ID de la commande associée"""
    return db.query(Payment).filter(Payment.order_id == order_id).first()

def get_payments(db: Session, skip: int = 0, limit: int = 100):
    """Récupère une liste de paiements avec pagination"""
    return db.query(Payment).offset(skip).limit(limit).all()

def create_payment(db: Session, payment: PaymentCreate):
    """Crée un nouveau paiement"""
    db_payment = Payment(
        order_id=payment.order_id,
        amount=payment.amount,
        payment_status="en attente"
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment(db: Session, payment_id: int, payment_data: PaymentUpdate):
    """Met à jour le statut d'un paiement"""
    db_payment = get_payment(db, payment_id)
    if db_payment:
        update_data = payment_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_payment, key, value)
        db.commit()
        db.refresh(db_payment)
    return db_payment

def delete_payment(db: Session, payment_id: int):
    """Supprime un paiement"""
    db_payment = get_payment(db, payment_id)
    if db_payment:
        db.delete(db_payment)
        db.commit()
        return True
    return False
