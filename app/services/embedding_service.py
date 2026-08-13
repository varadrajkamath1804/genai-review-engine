from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingService:
    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    async def generate_embedding(
        self,
        text: str,
    ) -> list[float]:
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
