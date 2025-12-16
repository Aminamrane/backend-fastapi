from datetime import timedelta
import jwt

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    ALGORITHM
)
from app.core.config import settings


def test_password_hash_and_verify():
    password = "SuperSecret123!"
    hashed = get_password_hash(password)

    assert hashed != password

    assert verify_password(password, hashed) is True

    assert verify_password("wrong-password", hashed) is False


def test_create_access_token():
    subject = "test-user"
    token = create_access_token(
        subject=subject,
        expires_delta=timedelta(minutes=5)
    )

    assert isinstance(token, str)

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    assert payload["sub"] == subject
    assert "exp" in payload
