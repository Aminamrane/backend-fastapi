import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
class UserBase(SQLModel):
    email: EmailStr = Field(index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
class UserCreate(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)
class UserPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    is_superuser: bool
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
class TokenPayload(SQLModel):
    sub: str | None = None
class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
class Message(SQLModel):
    message: str
