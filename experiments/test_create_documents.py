from app.services.chunking_service import ChunkingService

chunking_service = ChunkingService(
    chunk_size=80,
    chunk_overlap=20,
)


texts = [
    """
    The product quality is excellent and the battery lasts all day.
    The sound quality is also very good and provides a great listening experience.
    However, some users reported problems after using the product for several days.
    """,
    """
    The mobile application crashes whenever users try to make a payment.
    Customer support responded quickly but was unable to solve every issue.
    Some customers were disappointed with the overall experience.
    """,
]


metadatas = [
    {
        "review_id": 1,
        "sentiment": "Positive",
    },
    {
        "review_id": 19,
        "sentiment": "Negative",
    },
]


documents = chunking_service.create_chunk_documents(
    texts=texts,
    metadatas=metadatas,
)


for index, document in enumerate(documents, start=1):

    print(f"\n--- DOCUMENT CHUNK {index} ---")

    print("\nPAGE CONTENT:")
    print(document.page_content)

    print("\nMETADATA:")
    print(document.metadata)
