from docx import Document
from PyPDF2 import PdfReader


def read_txt(file):
    return file.read().decode("utf-8", errors="ignore")


def read_pdf(file):
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def read_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def read_uploaded_resume(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return read_txt(uploaded_file)
    elif file_name.endswith(".pdf"):
        return read_pdf(uploaded_file)
    elif file_name.endswith(".docx"):
        return read_docx(uploaded_file)
    else:
        return ""


def extract_resume_sections(resume_text):
    sections = {
        "summary": "",
        "education": "",
        "skills": "",
        "projects": "",
        "experience": "",
        "certifications": "",
        "achievements": ""
    }

    section_map = {
        "summary": ["summary", "professional summary", "profile", "objective", "career objective"],
        "education": ["education", "academic background", "qualification", "academic qualifications"],
        "skills": ["skills", "technical skills", "core skills", "key skills"],
        "projects": ["projects", "project"],
        "experience": ["experience", "work experience", "internship", "employment", "professional experience"],
        "certifications": ["certifications", "certificate", "licenses", "certificates"],
        "achievements": ["achievements", "accomplishments", "awards"]
    }

    lines = resume_text.splitlines()
    current_section = None

    for line in lines:
        stripped = line.strip()
        low = stripped.lower()

        detected_section = None
        for section, titles in section_map.items():
            if low in titles:
                detected_section = section
                break

        if detected_section:
            current_section = detected_section
            continue

        if current_section and stripped:
            sections[current_section] += stripped + "\n"

    return {k: v.strip() for k, v in sections.items()}
