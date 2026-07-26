from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine

router = APIRouter(
    prefix="/db",
    tags=["Health"],
)


@router.get("/db/health")
async def database_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"status": "connected"}
