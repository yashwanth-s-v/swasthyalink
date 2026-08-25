from datetime import datetime, timedelta, timezone

import bcrypt

from jose import JWTError, jwt

from config import settings


# ==========================================
# PASSWORD HASHING
# ==========================================

def hash_password(password: str) -> str:
    """
    Hash a user's password using bcrypt.
    """

    password_bytes = password.encode("utf-8")

    # bcrypt has a 72-byte password limitation.
    if len(password_bytes) > 72:

        raise ValueError(
            "Password must be 72 bytes or less."
        )

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password_bytes,
        salt
    )

    return hashed.decode("utf-8")


# ==========================================
# PASSWORD VERIFICATION
# ==========================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain password against a bcrypt hash.
    """

    password_bytes = plain_password.encode(
        "utf-8"
    )

    hashed_bytes = hashed_password.encode(
        "utf-8"
    )

    return bcrypt.checkpw(
        password_bytes,
        hashed_bytes
    )


# ==========================================
# CREATE JWT
# ==========================================

def create_access_token(
    user_id: int,
    role: str
) -> str:
    """
    Create JWT access token.
    """

    expire = (
        datetime.now(timezone.utc)
        + timedelta(minutes=60)
    )

    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


# ==========================================
# DECODE JWT
# ==========================================

def decode_access_token(
    token: str
) -> dict | None:
    """
    Decode and validate JWT access token.
    """

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ]
        )

        return payload

    except JWTError:

        return None