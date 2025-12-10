import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.models import Item, ItemCreate, ItemUpdate, ItemPublic, ItemsPublic, Message

router = APIRouter(prefix="/items", tags=["items"])

@router.post("/", response_model=ItemPublic)
def create_item(session: SessionDep, current_user: CurrentUser, item_in: ItemCreate) -> Any:
    item = Item(**item_in.model_dump(), owner_id=current_user.id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return ItemPublic.model_validate(item)

@router.get("/", response_model=ItemsPublic)
def list_my_items(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    items = session.exec(
        select(Item).where(Item.owner_id == current_user.id).offset(skip).limit(limit)
    ).all()
    count = session.exec(
        select(func.count()).select_from(select(Item).where(Item.owner_id == current_user.id).subquery())
    ).one()
    data = [ItemPublic.model_validate(i) for i in items]
    return ItemsPublic(data=data, count=count)

@router.get("/{item_id}", response_model=ItemPublic)
def get_item(session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID) -> Any:
    item = session.get(Item, item_id)
    if not item or (not current_user.is_superuser and item.owner_id != current_user.id):
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemPublic.model_validate(item)

@router.put("/{item_id}", response_model=ItemPublic)
def update_item(session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID, item_in: ItemUpdate) -> Any:
    item = session.get(Item, item_id)
    if not item or item.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(item, k, v)
    session.add(item)
    session.commit()
    session.refresh(item)
    return ItemPublic.model_validate(item)

@router.delete("/{item_id}", response_model=Message)
def delete_item(session: SessionDep, current_user: CurrentUser, item_id: uuid.UUID) -> Any:
    item = session.get(Item, item_id)
    if not item or (not current_user.is_superuser and item.owner_id != current_user.id):
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return Message(message="Item deleted successfully")
