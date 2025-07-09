import fitz  # PyMuPDF
import re
from utils.skills_bank import skills_list

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join([page.get_text() for page in doc])

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if len(line.split()) <= 4 and len(line) > 2:
            return line.title()
    return "Candidate"

def extract_skills_from_resume(text):
    found = []
    for skill in skills_list:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append(skill)
    return list(set(found))