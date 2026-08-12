# Professional Resume Template Module
from utils.pdf_export import generate_resume_pdf

def render_professional_pdf(data: dict) -> bytes:
    return generate_resume_pdf(data, theme="Professional")
