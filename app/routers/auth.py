from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.db.models.user import User
from app.dependencies.auth import get_auth_service
from app.dependencies.current_user import get_current_user
from app.models.user.user_create import UserCreate
from app.models.user.user_response import UserResponse
from app.services.auth_service import AuthService
from app.models.user.user_login import UserLogin
from app.models.user.logout_request import LogoutRequest
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
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.refresh_token(
        request.refresh_token,
    )


@router.post("/logout")
async def logout(
    request: LogoutRequest,
    current_user=Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout(
        request.refresh_token,
        user_id=current_user.id,
    )

    return {
        "message": "logged out successfully",
    }


@router.post("/logout-all")
async def logout_all(
    current_user: User = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    await auth_service.logout_all(
        current_user.id,
    )

    return {
        "message": "Logged out from all devices successfully.",
    }
