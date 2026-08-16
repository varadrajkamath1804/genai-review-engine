from http import HTTPStatus
from fastapi import APIRouter, Depends, Query

from typing import Annotated
from app.models.user.enums import Role
from app.dependencies.rbac import RoleChecker
from app.models.review.query import SortField, SortOrder
from app.models.review.review import ReviewInput
from app.models.review.review_response import ReviewResponse
from app.models.review.update_review import UpdateReview
from app.models.review.sentiment import SentimentResponse
from app.services.ai_service import AIService
from app.dependencies.ai import get_ai_service
from app.dependencies.current_user import get_current_user
from app.dependencies.rate_limit import rate_limit
from app.models.review.semantic_search import SemanticSearchRequest
from app.services.semantic_search_service import SemanticSearchService
from app.dependencies.repository import get_semantic_search_service
from app.dependencies.rag import get_rag_service
from app.services.rag_service import RAGService
from app.models.review.rag_response import RAGResponse

router = APIRouter(
    prefix="/ai",
    tags=["Reviews"],
)


@router.post("/analyze")
async def analyze_review(
    review: ReviewInput,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
    _: None = Depends(rate_limit),
) -> SentimentResponse:

    return await ai_service.analyze_review(
        review,
    )


@router.get(
    "/reviews",
    response_model=list[ReviewResponse],
    status_code=HTTPStatus.OK,
)
async def get_all_reviews(
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    sentiment: str | None = None,
    review: str | None = None,
    sort_by: SortField = SortField.id,
    order: SortOrder = SortOrder.asc,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
    _: None = Depends(rate_limit),
):
    return await ai_service.get_all_reviews(
        page,
        size,
        sentiment,
        review,
        sort_by,
        order,
    )


@router.get(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
    status_code=HTTPStatus.OK,
)
async def get_review(
    review_id: int,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
):
    return await ai_service.get_review(
        review_id,
    )


@router.put(
    "/reviews/{review_id}",
    response_model=ReviewResponse,
)
async def update_review(
    review_id: int,
    review: UpdateReview,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(get_current_user),
):
    return await ai_service.update_review(
        review_id,
        review,
    )


@router.delete("/reviews/{review_id}")
async def delete_review(
    review_id: int,
    ai_service: AIService = Depends(get_ai_service),
    current_user: Users = Depends(RoleChecker(Role.ADMIN)),
):
    return await ai_service.delete_review(review_id)


@router.post(
    "/reviews/semantic-search",
    response_model=list[ReviewResponse],
)
async def semantic_search(
    request: SemanticSearchRequest,
    semantic_search_service: SemanticSearchService = Depends(
        get_semantic_search_service
    ),
) -> list[ReviewResponse]:
    reviews = await semantic_search_service.semantic_search(
        query=request.query,
        limit=request.limit,
    )

    return [ReviewResponse.model_validate(review) for review in reviews]


@router.post("/rag")
async def rag_answer(
    request: SemanticSearchRequest, rag_service: RAGService = Depends(get_rag_service)
) -> RAGResponse:
    return await rag_service.generate_answer(
        query=request.query,
        limit=request.limit,
    )
