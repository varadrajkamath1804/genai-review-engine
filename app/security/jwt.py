from datetime import UTC, datetime, timedelta
from jose import jwt

from app.core.config import get_settings


class JWTManager:
    """
    Handles JWT token generation and verification.
    """

    @staticmethod
    def create_access_token(
        data: dict,
    ) -> str:
        settings = get_settings()

        payload = data.copy()

        expire = datetime.now(
            UTC,
        ) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        payload["exp"] = expire

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
        )
