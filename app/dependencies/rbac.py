from fastapi import Depends

from app.exceptions.user import ForbiddenException
from app.db.models.user import User
from app.dependencies.current_user import get_current_user
from app.models.user.enums import Role


class RoleChecker:

    def __init__(self, required_role: Role):
        self.required_role = required_role

    async def __call__(
        self,
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in self.required_role:
            raise ForbiddenException()

        return current_user
