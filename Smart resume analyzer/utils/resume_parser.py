import re
import pdfplumber
import docx
import spacy

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    # If spaCy model isn't downloaded yet, load blank English or handle gracefully
    try:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None

# Comprehensive skill dictionary for keyword extraction fallback & categorization
COMMON_SKILLS = [
    "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "SQL", "R", "PHP",
    "React", "Angular", "Vue.js", "Next.js", "Node.js", "Express", "Django", "Flask", "FastAPI",
    "HTML", "CSS", "Tailwind CSS", "Bootstrap", "Streamlit", "GraphQL", "REST API",
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Scikit-Learn", "Pandas", "NumPy", "OpenCV", "SpaCy", "Gemini API",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Git", "GitHub", "CI/CD", "Linux", "Bash",
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Snowflake", "BigQuery",
    "Agile", "Scrum", "Project Management", "Leadership", "Communication", "Problem Solving",
    "Data Analysis", "Data Visualization", "Plotly", "Power BI", "Tableau"
]

def extract_text_from_pdf(pdf_file) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        text = f"Error reading PDF file: {str(e)}"
    return text.strip()

def extract_text_from_docx(docx_file) -> str:
    text = ""
    try:
        doc = docx.Document(docx_file)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text += paragraph.text + "\n"
    except Exception as e:
        text = f"Error reading DOCX file: {str(e)}"
    return text.strip()

def parse_resume(file_obj) -> dict:
    file_name = file_obj.name
    ext = file_name.split(".")[-1].lower()
    
    if ext == "pdf":
        raw_text = extract_text_from_pdf(file_obj)
    elif ext in ["doc", "docx"]:
        raw_text = extract_text_from_docx(file_obj)
    else:
        raw_text = file_obj.read().decode("utf-8", errors="ignore")

    email = extract_email(raw_text)
    phone = extract_phone(raw_text)
    skills = extract_skills(raw_text)
    entities = extract_entities(raw_text)

    return {
        "filename": file_name,
        "raw_text": raw_text,
        "email": email,
        "phone": phone,
        "skills": skills,
        "entities": entities,
        "word_count": len(raw_text.split())
    }

def extract_email(text: str) -> str:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else "Not Found"

def extract_phone(text: str) -> str:
    pattern = r'(\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{4}'
    matches = re.findall(pattern, text)
    if matches:
        return re.sub(r'[^\d+]', '', text[text.find(matches[0]):text.find(matches[0])+15])
    return "Not Found"

def extract_skills(text: str) -> list:
    extracted = []
    text_lower = text.lower()
    for skill in COMMON_SKILLS:
        # Match word boundary
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            extracted.append(skill)
    return list(set(extracted))

def extract_entities(text: str) -> dict:
    entities = {"organizations": [], "dates": [], "degrees": []}
    
    if nlp is not None:
        doc = nlp(text[:10000])  # limit length for spacy speed
        for ent in doc.ents:
            if ent.label_ == "ORG" and ent.text not in entities["organizations"]:
                entities["organizations"].append(ent.text)
            elif ent.label_ == "DATE" and ent.text not in entities["dates"]:
                entities["dates"].append(ent.text)

    # Regex heuristic for degrees
    degree_patterns = [r"B\.?S\.?", r"B\.?A\.?", r"M\.?S\.?", r"Ph\.?D", r"Bachelor", r"Master", r"Degree", r"B\.?Tech", r"M\.?Tech"]
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            if match not in entities["degrees"]:
                entities["degrees"].append(match)

    return entities
