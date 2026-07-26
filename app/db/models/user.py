from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.user.enums import Role
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True)

    # User's full name
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Email used for login (must be unique)
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    # Store HASHED password (never plain text)
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # User role (will later become an Enum)
    role: Mapped[Role] = mapped_column(
        Enum(Role),
        nullable=False,
        default=Role.USER,
    )

    # Automatically set when the row is created
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Automatically updated whenever the row changes
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
