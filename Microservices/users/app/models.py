import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

# DB-mapped model mirrors the shared 'user' table (owned by AUTH).
# Keeping hashed_password column for ORM completeness; never expose it in API.
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

# API schemas (never include hashed_password)
class UserPublic(SQLModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    is_superuser: bool

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    full_name: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None   # superuser only
    is_superuser: bool | None = None  # superuser only

class Message(SQLModel):
    message: str

# Minimal token payload to decode JWT
class TokenPayload(SQLModel):
    sub: str | None = None
