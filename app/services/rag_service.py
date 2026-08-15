from groq import AsyncGroq

from app.core.config import Settings
from app.services.semantic_search_service import SemanticSearchService
from app.models.review.rag_response import RAGResponse, RAGSource


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

        context = "\n\n".join(
            f"Review {index + 1}: {review.review}"
            for index, review in enumerate(reviews)
        )

        # ---------------------------------------------------------
        # STEP 3: SEND QUESTION + CONTEXT TO THE LLM
        # ---------------------------------------------------------

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a customer review analysis assistant.\n\n"
                    "Your task is to answer the user's question "
                    "using ONLY the information contained in the "
                    "provided review context.\n\n"
                    "Rules:\n"
                    "1. Do not use outside knowledge.\n"
                    "2. Do not invent or assume information.\n"
                    "3. If the context does not contain enough "
                    "information to answer the question, clearly say "
                    "that the available reviews do not contain enough "
                    "information.\n"
                    "4. Base your answer only on the retrieved reviews.\n"
                    "5. Keep the answer concise and directly answer "
                    "the user's question."
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

        sources = [
            RAGSource(
                id=review.id,
                review=review.review,
            )
            for review in reviews
        ]

        # Extract the generated answer from the Groq response.
        return RAGResponse(
            answer=response.choices[0].message.content,
            sources=sources,
        )
