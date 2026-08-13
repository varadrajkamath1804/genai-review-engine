import asyncio

from app.services.embedding_service import EmbeddingService

REVIEWS = [
    "The battery lasts all day and is excellent.",
    "The delivery was extremely late.",
    "The phone camera takes amazing photos.",
    "Battery performance is really good.",
    "The product packaging was damaged.",
    "The phone battery dies very quickly.",
    "The screen quality is excellent.",
]


async def main() -> None:
    embedding_service = EmbeddingService()

    review_embeddings = []

    for review in REVIEWS:
        embedding = await embedding_service.generate_embedding(review)
        review_embeddings.append(embedding)

    query = "Which reviews talk about good battery life?"

    query_embedding = await embedding_service.generate_embedding(query)

    results = []

    for review, embedding in zip(REVIEWS, review_embeddings):
        similarity = embedding_service.calculate_similarity(
            query_embedding,
            embedding,
        )
        results.append((review, similarity))

    results.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    print("\nSearch Results\n")

    for review, similarity in results:
        print(f"{similarity:.4f} → {review}")


if __name__ == "__main__":
    asyncio.run(main())
