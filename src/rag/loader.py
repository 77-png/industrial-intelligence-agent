from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str) -> list[dict]:
    """
    Read a PDF page by page and keep source metadata.
    """

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append(
                {
                    "text": text.strip(),
                    "source": Path(pdf_path).name,
                    "page": page_number,
                }
            )

    return documents


def load_all_pdfs(directory: str) -> list[dict]:
    """
    Load all PDF files from a directory.
    """

    directory_path = Path(directory)

    all_documents = []

    pdf_files = list(directory_path.glob("*.pdf"))

    for pdf_path in pdf_files:
        print(f"正在读取：{pdf_path.name}")

        documents = load_pdf(str(pdf_path))

        print(f"  → 读取 {len(documents)} 页")

        all_documents.extend(documents)

    return all_documents