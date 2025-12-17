import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    text_chunks = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text:
                text_chunks.append(page_text)

    return "\n".join(text_chunks)
