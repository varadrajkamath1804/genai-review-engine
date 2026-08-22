class ChunkingService:
    # fixed-size chunking with overlap
    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> list[str]:

        # Return an empty list when there is no text.
        if not text:
            return []

        # Prevent an invalid overlap that could cause
        # the chunking loop to never move forward.
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk must be smaller than chunk size")

        chunks = []

        start = 0
        text_length = len(text)

        while start < text_length:

            # Calculate where the current chunk should end.
            end = start + chunk_size

            # Extract the current chunk.
            chunk = text[start:end]

            # Store the chunk.
            chunks.append(chunk)

            # Stop when we have reached the end of the text.
            if end >= text_length:
                break

            # Move forward by:
            # chunk_size - chunk_overlap
            #
            # This preserves part of the previous chunk.
            start = end - chunk_overlap

        return chunks
