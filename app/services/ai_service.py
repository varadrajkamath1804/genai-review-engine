from groq import AsyncGroq

from app.core.config import Settings
from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse


class AIService:
    """
    Service responsible for AI-powered review analysis.
    """

    def __init__(
        self,
        client: AsyncGroq,
        settings: Settings,
    ):
        self.client = client
        self.settings = settings

    async def analyze_review(self, review: ReviewInput) -> SentimentResponse:
        print(review)
        print(review.review)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a sentiment analysis assistant.\n"
                    "Analyze customer reviews.\n"
                    "Return the sentiment of the review."
                ),
            },
            {
                "role": "user",
                "content": review.review,
            },
        ]
        try:
            response = await self.client.chat.completions.create(
                model=self.settings.GROQ_MODEL, messages=messages, temperature=0
            )

            print(response.choices[0].message.content)

            return SentimentResponse(
                sentiment=response.choices[0].message.content,
                confidence=1.0,
            )

        except Exception as error:
            raise RuntimeError("Failed to analyze review") from error
