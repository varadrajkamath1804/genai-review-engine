from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import engine
from app.exceptions import DatabaseConnectionFailed

router = APIRouter(
    prefix="/connection",
    tags=["Health"],
)


@router.get("/db/health")
async def database_health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {"status": "connected"}
    except SQLAlchemyError as exc:
        raise DatabaseConnectionFailed() from exc
