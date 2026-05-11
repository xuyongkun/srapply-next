import os
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import JWTError, jwt


class AuthService:
    def __init__(self) -> None:
        self.secret = os.getenv("JWT_SECRET", "srapply-dev-secret")
        self.expire_seconds = int(os.getenv("JWT_EXPIRE_SECONDS", "28800"))

    def encode_token(self, user_id: int, username: str, role: str) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "iat": now,
            "exp": now + timedelta(seconds=self.expire_seconds),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
        except JWTError as exc:
            raise HTTPException(status_code=401, detail="invalid token") from exc
        return payload
