import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select, func

from app.api.deps import SessionDep, CurrentUser, get_current_active_superuser
from app.models import User, UserPublic, UsersPublic, UserUpdate, Message

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=UsersPublic)
def read_users(session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    count = session.exec(select(func.count()).select_from(User)).one()
    data = [UserPublic.model_validate(u) for u in users]
    return UsersPublic(data=data, count=count)

@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return UserPublic.model_validate(current_user)

@router.put("/me", response_model=UserPublic)
def update_user_me(session: SessionDep, current_user: CurrentUser, user_in: UserUpdate) -> Any:
    # users service can update profile fields (not password)
    if user_in.email is not None:
        current_user.email = user_in.email
    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return UserPublic.model_validate(current_user)

@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID) -> Any:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if (not current_user.is_superuser) and (user.id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough privileges")
    return UserPublic.model_validate(user)

@router.delete("/{user_id}", response_model=Message)
def delete_user(session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID) -> Any:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
