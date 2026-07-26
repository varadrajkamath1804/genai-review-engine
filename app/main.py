from contextlib import asynccontextmanager
from sqlalchemy import text
from http import HTTPStatus
from fastapi import FastAPI, Depends, Query
from groq import AsyncGroq
from typing import Annotated
import logging
from app.core.logging_config import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware
from app.exceptions.handlers import register_exception_handlers
from app.clients.groq import create_groq_client
from app.models.review.query import SortField, SortOrder
from app.models.review.review import ReviewInput
from app.models.review.review_response import ReviewResponse
from app.models.review.update_review import UpdateReview
from app.models.review.sentiment import SentimentResponse
from app.services.ai_service import AIService
from app.dependencies.ai import get_ai_service
from app.dependencies.current_user import get_current_user
from app.core.database import engine
from app.dependencies.auth import get_auth_service
from app.models.user.user_create import UserCreate
from app.models.user.user_response import UserResponse
from app.services.auth_service import AuthService
from app.models.user.user_login import UserLogin
from app.models.user.token_response import TokenResponse
from app.db.models.user import User

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    app.state.groq = create_groq_client()
    logger.info("Groq client initialized")
    yield
    await app.state.groq.close()
    logger.info("Groq client closed")


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.add_middleware(RequestLoggingMiddleware)


@app.post("/analyze")
async def analyze_review(
    review: ReviewInput,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
) -> SentimentResponse:

    return await ai_service.analyze_review(
        review,
    )


@app.get(
    "/reviews",
    response_model=list[ReviewResponse],
    status_code=HTTPStatus.OK,
)
async def get_all_reviews(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    sentiment: str | None = None,
    review: str | None = None,
    sort_by: SortField = SortField.id,
    order: SortOrder = SortOrder.asc,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
):
    return await ai_service.get_all_reviews(
        page,
        size,
        sentiment,
        review,
        sort_by,
        order,
    )


@app.get(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
    status_code=HTTPStatus.OK,
)
async def get_review(
    review_id: int,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
):
    return await ai_service.get_review(
        review_id,
    )


@app.get("/db/health")
async def database_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"status": "connected"}


@app.put(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
)
async def update_review(
    review_id: int,
    review: UpdateReview,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
):
    return await ai_service.update_review(
        review_id,
        review,
    )


@app.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
):
    await ai_service.delete_review(review_id)


@app.post(
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


@app.post(
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
