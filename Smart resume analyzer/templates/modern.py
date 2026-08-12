# Modern Resume Template Module
from utils.pdf_export import generate_resume_pdf

def render_modern_pdf(data: dict) -> bytes:
    return generate_resume_pdf(data, theme="Modern")
