from http import HTTPStatus
from fastapi import APIRouter, Depends
from app.dependencies.job import get_job_service
from app.dependencies.current_user import get_current_user
from app.services.job_services import JobService
from app.models.review.review import ReviewInput
from app.models.user.enums import Role
from app.dependencies.rbac import RoleChecker
from app.exceptions import JobNotCompletedException

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post(
    "/analyze",
    status_code=HTTPStatus.ACCEPTED,
)
async def submit_analysis_job(
    review: ReviewInput,
    job_service: JobService = Depends(get_job_service),
    current_user=Depends(get_current_user),
):
    """
    Submit a sentiment analysis job for background processing.
    """
    job_id = await job_service.analyze_review_async(review)

    return {
        "job_id": job_id,
        "status": "pending",
        "message": "Job submitted. Check /jobs/{job_id}/status",
    }


@router.get(
    "/{job_id}/status",
    status_code=HTTPStatus.OK,
)
async def get_job_status(
    job_id: str,
    job_service: JobService = Depends(get_job_service),
    # ❌ current_user NOT required - anyone can check status
):
    """
    Get the status of a background job.
    """
    return await job_service.get_job_status(job_id)


@router.get(
    "/{job_id}/result",
    status_code=HTTPStatus.OK,
)
async def get_job_result(
    job_id: str,
    job_service: JobService = Depends(get_job_service),
    # ❌ current_user NOT required - anyone can get result
):
    """
    Get the result of a completed job.
    """
    status = await job_service.get_job_status(job_id)

    if status.get("status") != "completed":
        raise JobNotCompletedException(job_id, status.get("status"))

    return status.get("result")


@router.delete(
    "/{job_id}",
    status_code=HTTPStatus.OK,
)
async def delete_job(
    job_id: str,
    job_service: JobService = Depends(get_job_service),
    current_user=Depends(RoleChecker(Role.ADMIN)),
):
    """
    Delete a job (Admin only).
    """
    await job_service.get_job_status(job_id)

    return {"message": f"Job {job_id} deleted successfully"}
