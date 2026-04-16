import streamlit as st
from templates_data import TEMPLATE_LIST
from ats_logic import calculate_ats_score
from resume_engine import generate_resume_text, get_template_html
from pdf_export import convert_html_to_pdf

st.set_page_config(page_title="Resume Builder Pro", layout="wide")

st.title("Resume Builder Pro with ATS Optimizer")
st.write("Create ATS-friendly resumes and choose from 100+ resume designs.")

st.sidebar.header("Choose Resume Design")
template_names = [f"{item['id']} - {item['name']}" for item in TEMPLATE_LIST]
selected_template = st.sidebar.selectbox("Select Template", template_names)

st.sidebar.write(f"Total Templates Available: {len(TEMPLATE_LIST)}")

col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    linkedin = st.text_input("LinkedIn")
    github = st.text_input("GitHub")
    address = st.text_input("Address")
    summary = st.text_area("Professional Summary", height=120)
    education = st.text_area("Education", height=120)
    skills = st.text_area("Skills", height=120)

with col2:
    projects = st.text_area("Projects", height=150)
    experience = st.text_area("Experience", height=150)
    certifications = st.text_area("Certifications", height=100)
    achievements = st.text_area("Achievements", height=100)
    job_desc = st.text_area("Paste Job Description", height=180)

data = {
    "full_name": full_name,
    "email": email,
    "phone": phone,
    "linkedin": linkedin,
    "github": github,
    "address": address,
    "summary": summary,
    "education": education,
    "skills": skills,
    "projects": projects,
    "experience": experience,
    "certifications": certifications,
    "achievements": achievements,
}

if st.button("Generate Resume"):
    resume_text = generate_resume_text(data)
    score, matched_keywords, missing_keywords = calculate_ats_score(resume_text, job_desc)

    # project scoring logic
    if score >= 90 and len(missing_keywords) <= 2:
        score = 100

    st.success("Resume generated successfully.")
    st.metric("ATS Score", f"{score}/100")

    st.subheader("Matched Keywords")
    st.write(", ".join(matched_keywords) if matched_keywords else "No strong match found.")

    st.subheader("Missing Keywords")
    st.write(", ".join(missing_keywords[:20]) if missing_keywords else "No important keyword missing.")

    st.subheader("Resume Preview")
    html_preview = get_template_html(selected_template, data)
    st.components.v1.html(html_preview, height=900, scrolling=True)

    st.download_button(
        label="Download Resume as TXT",
        data=resume_text,
        file_name="resume.txt",
        mime="text/plain"
    )

    pdf_bytes = convert_html_to_pdf(html_preview)
    if pdf_bytes:
        st.download_button(
            label="Download Resume as PDF",
            data=pdf_bytes,
            file_name="resume.pdf",
            mime="application/pdf"
        )
