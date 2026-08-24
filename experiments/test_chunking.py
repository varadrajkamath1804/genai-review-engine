from app.services.chunking_service import ChunkingService

chunking_service = ChunkingService(
    chunk_size=80,
    chunk_overlap=20,
)

text = """
The product quality is excellent and the battery lasts all day. 
The sound quality is also very good and provides a great listening experience.
However, after using the product for several days, some users reported issues.
The mobile application sometimes crashes when making payments or updating information.
Customer support responded quickly and solved some issues, but other customers were disappointed.
The delivery process was fast, and the package arrived earlier than expected.
"""

chunks = chunking_service.chunk_text(text)

for index, chunk in enumerate(chunks, start=1):
    print(f"\n--- CHUNK {index} ---")
    print(chunk)
    print(f"Length: {len(chunk)}")
