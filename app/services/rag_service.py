from groq import AsyncGroq

from app.core.config import Settings
from app.services.semantic_search_service import SemanticSearchService


class RAGService:
    def __init__(
        self,
        client: AsyncGroq,
        settings: Settings,
        semantic_search_service=SemanticSearchService,
    ):
        self.client = client
        self.settings = settings
        self.semantic_search_service = semantic_search_service

    async def generate_answer(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        # ---------------------------------------------------------
        # STEP 1: RETRIEVAL
        # ---------------------------------------------------------
        # Convert the user's question into an embedding and
        # retrieve the most semantically relevant reviews.

        reviews = await self.semantic_search_service.semantic_search(
            query=query,
            limit=limit,
        )

        # ---------------------------------------------------------
        # STEP 2: BUILD CONTEXT
        # ---------------------------------------------------------
        # Convert the retrieved reviews into plain text that
        # can be provided to the LLM as context.

        context = "\n\n".join(f"Review {review.review}" for review in reviews)

        # ---------------------------------------------------------
        # STEP 3: SEND QUESTION + CONTEXT TO THE LLM
        # ---------------------------------------------------------

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a customer review analysis assistant.\n\n"
                    "Answer the user's question using ONLY the "
                    "provided review context.\n"
                    "If the context does not contain enough "
                    "information, say so.\n"
                    "Do not invent information."
                ),
            },
            {
                "role": "user",
                "content": (f"Context:\n" f"{context}\n\n" f"Question:\n" f"{query}"),
            },
        ]

        # ---------------------------------------------------------
        # STEP 4: GENERATION
        # ---------------------------------------------------------
        response = await self.client.chat.completions.create(
            model=self.settings.GROQ_MODEL,
            messages=messages,
            temperature=0,
        )

        # Extract the generated answer from the Groq response.
        return response.choices[0].message.content
