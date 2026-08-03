from app.services.token_blacklist import TokenBlacklistService


def get_blacklist_service() -> TokenBlacklistService:
    return TokenBlacklistService()
