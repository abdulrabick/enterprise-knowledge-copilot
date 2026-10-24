from pypdf import PdfReader
from docx import Document


def extract_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        text += f"\n[Page {page_number}]\n{page_text}"

    return text


def extract_docx(file):
    document = Document(file)
    text = "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )

    return text


def extract_txt(file):
    content = file.getvalue()
    return content.decode("utf-8", errors="replace")