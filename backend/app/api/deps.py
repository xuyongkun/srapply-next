from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth import CurrentUser
from app.services.auth import AuthService

security = HTTPBearer(auto_error=False)
auth_service = AuthService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> CurrentUser:
    if not credentials:
        raise HTTPException(status_code=401, detail="missing authorization header")
    payload = auth_service.decode_token(credentials.credentials)
    return CurrentUser(
        id=int(payload["sub"]),
        username=str(payload["username"]),
        role=str(payload["role"]),
    )


def require_roles(*roles: str):
    def checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="permission denied")
        return current_user

    return checker
