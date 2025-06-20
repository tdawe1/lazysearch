import docx
import pdfplumber

def load_docx_resume(path):
    doc = docx.Document(path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def load_pdf_resume(path):
    full_text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            full_text.append(page.extract_text())
    return "\n".join(full_text)

def load_combined_resumes(docx_path, pdf_path):
    docx_text = load_docx_resume(docx_path)
    pdf_text = load_pdf_resume(pdf_path)
    return docx_text + "\n\n" + pdf_text
