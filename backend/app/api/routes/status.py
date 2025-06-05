from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.crud import accept_order, arrive_order
from app.api.deps import get_db

router = APIRouter(prefix="/orders", tags=["orders-status"])

@router.post("/{order_id}/accept")
def accept_order_view(order_id: UUID, driver_id: UUID, db: Session = Depends(get_db)):
    order = accept_order(db, order_id, driver_id)
    return {"status": order.status}

@router.post("/{order_id}/arrive")
def arrive_order_view(order_id: UUID, db: Session = Depends(get_db)):
    order = arrive_order(db, order_id)
    return {"status": order.status}