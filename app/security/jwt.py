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
        return JWTManager._create_token(
            data,
            timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
        )

    @staticmethod
    def create_refresh_token(
        data: dict,
    ) -> str:
        settings = get_settings()

        return JWTManager._create_token(
            data,
            timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
            ),
        )

    @staticmethod
    def decode_token(
        token: str,
    ) -> dict:
        """
        Verify signature and decode a JWT.
        """

        settings = get_settings()

        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

    @staticmethod
    def _create_token(
        data: dict,
        expires_delta: timedelta,
    ) -> str:
        settings = get_settings()

        payload = data.copy()

        payload["exp"] = datetime.now(UTC) + expires_delta

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
