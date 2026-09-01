from pathlib import Path

from app.services.pdf_extraction_service import PDFExtractionService


async def main():
    pdf_path = Path("pdf/employee_handbook.pdf")

    service = PDFExtractionService()

    documents = await service.extract(str(pdf_path))

    print(f"Total pages extracted: {len(documents)}")

    for index, document in enumerate(documents, start=1):
        print(f"\n--- PAGE {index} ---")
        print("CONTENT:")
        print(document.page_content)
        print("METADATA:")
        print(document.metadata)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
