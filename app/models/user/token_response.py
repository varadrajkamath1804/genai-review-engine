from pydantic import BaseModel


class TokenResponse(BaseModel):

    # JWT Access Token
    access_token: str

    # JWT Refresh Token
    refresh_token: str

    # Authentication scheme
    token_type: str = "Bearer"
