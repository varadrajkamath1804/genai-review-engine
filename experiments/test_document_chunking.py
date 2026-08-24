from langchain_core.documents import Document

from app.services.chunking_service import ChunkingService

chunking_service = ChunkingService(
    chunk_size=80,
    chunk_overlap=20,
)


document = Document(
    page_content="""
The product quality is excellent and the battery lasts all day.
The sound quality is also very good and provides a great listening experience.
However, after using the product for several days, some users reported issues.
The mobile application sometimes crashes when making payments or updating information.
Customer support responded quickly and solved some issues, but other customers were disappointed.
""",
    metadata={
        "review_id": 19,
        "sentiment": "Negative",
        "confidence": 0.95,
    },
)


chunks = chunking_service.chunk_documents(
    documents=[document],
)


for index, chunk in enumerate(chunks, start=1):

    print(f"\n--- CHUNK {index} ---")

    print("\nPAGE CONTENT:")
    print(chunk.page_content)

    print("\nMETADATA:")
    print(chunk.metadata)
