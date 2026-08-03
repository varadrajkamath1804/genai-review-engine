from app.services.job_services import JobService


def get_job_service() -> JobService:
    return JobService()
