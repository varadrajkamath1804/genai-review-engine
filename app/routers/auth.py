from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.dependencies.auth import get_auth_service
from app.models.user.user_create import UserCreate
from app.models.user.user_response import UserResponse
from app.services.auth_service import AuthService
from app.models.user.user_login import UserLogin
from app.models.user.token_response import TokenResponse
from app.models.user.refresh_token import RefreshTokenRequest

router = APIRouter(
    prefix="",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
)
async def signup(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.signup(
        user,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=HTTPStatus.OK,
)
async def login(
    user_login: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """
    Authenticate user and return JWT.
    """
    return await auth_service.login(
        user_login,
    )


@router.post("/refresh")
async def refresh_token(request:RefreshTokenRequest,
auth_service:AuthService=Depends(get_auth_service),)
