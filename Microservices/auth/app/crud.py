import uuid
from typing import Optional
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate
def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User(email=user_create.email, full_name=user_create.full_name or None,
                  hashed_password=get_password_hash(user_create.password))
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
def get_user_by_email(*, session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()
def authenticate(*, session: Session, email: str, password: str) -> Optional[User]:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
