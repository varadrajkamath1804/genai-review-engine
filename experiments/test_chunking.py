from app.services.chunking_service import ChunkingService

chunking_service = ChunkingService()

text = """
The product quality is excellent and the battery lasts all day.
The sound quality is also very good.

However, the mobile application sometimes crashes when making payments.
Customer support responded quickly and solved the issue.
"""

chunks = chunking_service.chunk_text(
    text=text,
    chunk_size=80,
    chunk_overlap=20,
)

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {index} ---")
    print(chunk)
    print(f"Length: {len(chunk)}")
