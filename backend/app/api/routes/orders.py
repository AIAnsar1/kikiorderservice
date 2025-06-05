from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models import OrderCreate, OrderOut
from app.crud import create_order
from app.api.deps import get_db, get_current_active_superuser

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def create_order_view(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_active_superuser)
):
    order = await create_order(db, order_in, user.id)
    return order