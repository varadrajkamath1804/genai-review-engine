from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine
from app.core.redis import get_redis

router = APIRouter(
    prefix="/connection",
    tags=["Health"],
)


@router.get("/db/health")
async def database_health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {"status": "connected"}


@router.get("/redis/health")
async def redis_health():
    try:
        redis = await get_redis()
        await redis.ping()
        return {"status": "connected"}
    except Exception as e:
        return {"status": "disconnected", "error": str(e)}
