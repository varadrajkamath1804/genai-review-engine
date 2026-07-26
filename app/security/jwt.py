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

        # Copy payload
        payload = data.copy()

        # Add expiration claim
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        payload["exp"] = expire

        # Generate signed JWT
        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
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
