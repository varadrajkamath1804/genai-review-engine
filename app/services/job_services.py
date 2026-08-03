import json
import uuid
import logging
from typing import Dict, Optional
from datetime import datetime
from app.core.redis import get_redis
from app.exceptions import JobNotFoundException

logger = logging.getLogger(__name__)


class JobService:

    def __init__(self):
        self.prefix = "job:"
        self.result_prefix = "job:result:"
        self.default_ttl = 3600

    async def _get_redis(self):
        return await get_redis()

    async def create_job(self, job_type: str, data: Dict) -> str:
        job_id = str(uuid.uuid4())
        redis = await self._get_redis()

        key = f"{self.prefix}{job_id}"
        job_data = {
            "job_id": job_id,
            "job_type": job_type,
            "data": json.dumps(data),
            "status": "pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        await redis.hset(key, mapping=job_data)
        await redis.expire(key, self.default_ttl)

        queue_key = f"queue:{job_type}"
        await redis.rpush(queue_key, job_id)

        logger.info(f"✅ Job created: {job_id} ({job_type})")

        return job_id

    async def get_job_status(self, job_id: str) -> Dict:
        redis = await self._get_redis()
        key = f"{self.prefix}{job_id}"

        job_data = await redis.hgetall(key)
        if not job_data:
            raise JobNotFoundException

        if "data" in job_data:
            job_data["data"] = json.loads(job_data["data"])

        if job_data.get("status") == "completed":
            result_key = f"{self.result_prefix}{job_id}"
            result = await redis.get(result_key)
            if result:
                job_data["result"] = json.loads(result)
        return job_data

    async def update_job_status(self, job_id: str, status: str) -> None:
        redis = await self._get_redis()
        key = f"{self.prefix}{job_id}"

        exists = await self._get_redis(key)
        if not exists:
            raise JobNotFoundException

        await redis.hset(key, "status", status)
        await redis.hset(key, "updated_time", datetime.utcnow().isoformat())

        logger.info(f"Job Updated:{job_id} -> {status}")

    async def save_job_result(self, job_id: str, result: Dict) -> None:
        redis = await self._get_redis()

        result_key = f"{self.result_prefix}{job_id}"
        await redis.setex(result_key, self.default_ttl, json.dumps(result))
        await self.update_job_status(job_id, "completed")
        logger.info(f"Job result saved {job_id}")
