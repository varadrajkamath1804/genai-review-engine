"""add user role

Revision ID: c08ad54a6a3a
Revises: 5d0a6368f14f
Create Date: 2026-07-26 21:29:57.650625

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "c08ad54a6a3a"
down_revision: Union[str, Sequence[str], None] = "5d0a6368f14f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    role_enum = sa.Enum("USER", "ADMIN", name="role")

    role_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(length=20),
        type_=role_enum,
        existing_nullable=False,
        postgresql_using="role::role",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("USER", "ADMIN", name="role"),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
        postgresql_using="role::text",
    )

    role_enum = sa.Enum("USER", "ADMIN", name="role")
    role_enum.drop(op.get_bind(), checkfirst=True)
