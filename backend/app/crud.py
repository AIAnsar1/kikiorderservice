import uuid
from typing import Any

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate
from app.models import Order, OrderCreate


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item



async def create_order(session: Session, data: OrderCreate, user_id: uuid.UUID):
    # 1. Tariffni tekshirish (mock)
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.TARIFFS_URL}/tariffs/{data.tariff_id}")
        if resp.status_code != 200 or not resp.json().get("active", True):
            raise HTTPException(status_code=404, detail="Tariff not found or inactive")
        tariff = resp.json()
    # 2. Order yaratish
    order = Order(
        passenger_id=user_id,
        pickup_address=data.pickup.address,
        pickup_lat=data.pickup.lat,
        pickup_lon=data.pickup.lon,
        dropoff_address=data.dropoff.address,
        dropoff_lat=data.dropoff.lat,
        dropoff_lon=data.dropoff.lon,
        payment_method=data.payment_method,
        status="pending",
        estimated_price=tariff.get("base_price", 100.0),
    )
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_order(session: Session, order_id: uuid.UUID):
    return session.get(Order, order_id)

def accept_order(session: Session, order_id: uuid.UUID, driver_id: uuid.UUID):
    order = session.get(Order, order_id)
    if not order or order.status != "pending":
        raise HTTPException(status_code=400, detail="Order not pending")
    order.driver_id = driver_id
    order.status = "accepted"
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def arrive_order(session: Session, order_id: uuid.UUID):
    order = session.get(Order, order_id)
    if not order or order.status != "accepted":
        raise HTTPException(status_code=400, detail="Order not accepted")
    from datetime import datetime
    order.status = "arrived"
    order.arrived_at = datetime.utcnow()
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
