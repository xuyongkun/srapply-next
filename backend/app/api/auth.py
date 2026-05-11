from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt

from app.api.deps import get_current_user
from app.schemas.auth import CurrentUser, LoginRequest, LoginResponse
from app.services.auth import AuthService
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()
auth_service = AuthService()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    user = user_service.get_user(payload.username)
    if not user or not bcrypt.verify(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="invalid username or password")
    token = auth_service.encode_token(
        user_id=int(user["id"]),
        username=str(user["username"]),
        role=str(user["role"]),
    )
    return LoginResponse(
        access_token=token,
        username=str(user["username"]),
        role=str(user["role"]),
    )


@router.get("/me", response_model=CurrentUser)
def me(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    return current_user
