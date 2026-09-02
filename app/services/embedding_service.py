import asyncio

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:
    """
    Service responsible for converting text into numerical vectors.

    The model used here produces 384-dimensional embeddings.
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384

    async def generate_embedding(
        self,
        text: str,
    ) -> list[float]:  # useful when a user sends a search query.
        embedding = self.model.encode(text)
        return embedding.tolist()

    def calculate_similarity(
        self,
        embedding_a: list[float],
        embedding_b: list[float],
    ) -> float:
        similarity = cosine_similarity(
            [embedding_a],
            [embedding_b],
        )
        return float(similarity[0][0])

    async def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:  # useful when ingesting 163 document chunks.
        embeddings = await asyncio.to_thread(
            self.model.encode,
            texts,
        )
        return embeddings.tolist()
