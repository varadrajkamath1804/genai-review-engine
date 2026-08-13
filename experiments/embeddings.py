import asyncio

from app.services.embedding_service import EmbeddingService


async def main() -> None:
    embedding_service = EmbeddingService()

    texts = [
        "I love this phone",
        "This smartphone is excellent",
        "The delivery was extremely late",
    ]

    embeddings = []

    for text in texts:
        embedding = await embedding_service.generate_embedding(text)
        embeddings.append(embedding)

    print("\nEmbedding Dimensions: ")
    for text, embedding in zip(texts, embeddings):
        print(f"{text}:{len(embedding)}")

    similarity_1_2 = embedding_service.calculate_similarity(
        embeddings[0],
        embeddings[1],
    )

    similarity_1_3 = embedding_service.calculate_similarity(
        embeddings[0],
        embeddings[2],
    )

    print("\nSemantic similarity:")
    print(f"Sentence 1 ↔ Sentence 2: {similarity_1_2:.4f}")
    print(f"Sentence 1 ↔ Sentence 3: {similarity_1_3:.4f}")


if __name__ == "__main__":
    asyncio.run(main())
