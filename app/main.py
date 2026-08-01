from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.clients.groq import create_groq_client
from app.core.logging_config import configure_logging
from app.exceptions.handlers import register_exception_handlers
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.reviews import router as review_router
from app.middleware.request_logging import RequestLoggingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware

configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.groq = create_groq_client()

    logger.info("Groq client initialized")

    yield

    await app.state.groq.close()

    logger.info("Groq client closed")


app = FastAPI(
    lifespan=lifespan,
)

register_exception_handlers(app)

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(review_router)
app.include_router(health_router)
