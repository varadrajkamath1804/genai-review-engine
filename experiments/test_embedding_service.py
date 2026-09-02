import asyncio

from app.services.embedding_service import EmbeddingService


async def main():

    embedding_service = EmbeddingService()

    texts = [
        "Employees can apply for leave after six months.",
        "Annual leave must be approved by the manager.",
        "The company cafeteria is open from 9 AM to 6 PM.",
    ]

    embeddings = await embedding_service.generate_embeddings(texts)

    print("Number of texts:", len(texts))
    print("Number of embeddings:", len(embeddings))

    for index, embedding in enumerate(embeddings):
        print(
            f"Embedding {index + 1} dimension:",
            len(embedding),
        )


if __name__ == "__main__":
    asyncio.run(main())
