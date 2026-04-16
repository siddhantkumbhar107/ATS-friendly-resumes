import streamlit as st
from templates_data import TEMPLATE_LIST
from ats_logic import calculate_ats_score
from resume_engine import generate_resume_text, get_template_html
from pdf_export import convert_html_to_pdf
from resume_parser import read_uploaded_resume, extract_resume_sections

st.set_page_config(page_title="Resume Builder Pro", page_icon="📄", layout="wide")

st.title("📄 Resume Builder Pro with ATS Optimizer")
st.write("Upload your old resume or fill details manually, then generate a new ATS-friendly resume.")

# -----------------------------
# Sidebar Template Selection
# -----------------------------
st.sidebar.header("Choose Resume Design")

template_options = {f"{item['id']} - {item['name']}": item["id"] for item in TEMPLATE_LIST}
selected_template_label = st.sidebar.selectbox("Select Template", list(template_options.keys()))
selected_template_id = template_options[selected_template_label]

st.sidebar.write(f"Total Templates Available: {len(TEMPLATE_LIST)}")

# -----------------------------
# Upload Resume
# -----------------------------
st.subheader("Upload Existing Resume")
uploaded_resume = st.file_uploader("Upload Resume (.txt, .pdf, .docx)", type=["txt", "pdf", "docx"])

uploaded_text = ""
sections = {
    "summary": "",
    "education": "",
    "skills": "",
    "projects": "",
    "experience": "",
    "certifications": "",
    "achievements": ""
}

if uploaded_resume is not None:
    try:
        uploaded_text = read_uploaded_resume(uploaded_resume)
        if uploaded_text.strip():
            sections = extract_resume_sections(uploaded_text)
            st.success("Resume uploaded and parsed successfully.")
        else:
            st.warning("Resume uploaded, but no text could be extracted.")
    except Exception as e:
        st.error(f"Error reading uploaded resume: {e}")

# -----------------------------
# Resume Input Form
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    linkedin = st.text_input("LinkedIn")
    github = st.text_input("GitHub")
    address = st.text_input("Address")
    summary = st.text_area("Professional Summary", value=sections["summary"], height=140)
    education = st.text_area("Education", value=sections["education"], height=140)
    skills = st.text_area("Skills", value=sections["skills"], height=140)

with col2:
    projects = st.text_area("Projects", value=sections["projects"], height=160)
    experience = st.text_area("Experience", value=sections["experience"], height=160)
    certifications = st.text_area("Certifications", value=sections["certifications"], height=110)
    achievements = st.text_area("Achievements", value=sections["achievements"], height=110)
    job_desc = st.text_area("Paste Job Description", height=220)

# -----------------------------
# Resume Data Dictionary
# -----------------------------
data = {
    "full_name": full_name if full_name else "Your Name",
    "email": email if email else "your@email.com",
    "phone": phone if phone else "Your Phone",
    "linkedin": linkedin if linkedin else "Your LinkedIn",
    "github": github if github else "Your GitHub",
    "address": address if address else "Your Address",
    "summary": summary if summary else "Write your professional summary here.",
    "education": education if education else "Write your education details here.",
    "skills": skills if skills else "Write your skills here.",
    "projects": projects if projects else "Write your projects here.",
    "experience": experience if experience else "Write your experience here.",
    "certifications": certifications if certifications else "Write your certifications here.",
    "achievements": achievements if achievements else "Write your achievements here."
}

# -----------------------------
# Buttons
# -----------------------------
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    generate_button = st.button("Generate Resume")

with col_btn2:
    preview_button = st.button("Preview Resume")

# -----------------------------
# Preview Resume
# -----------------------------
if preview_button:
    try:
        html_preview = get_template_html(selected_template_id, data)
        st.subheader("Resume Preview")
        st.components.v1.html(html_preview, height=900, scrolling=True)
    except FileNotFoundError:
        st.error(f"Template HTML or CSS file not found for template {selected_template_id}.")
    except Exception as e:
        st.error(f"Error while loading preview: {e}")

# -----------------------------
# Generate Resume + ATS
# -----------------------------
if generate_button:
    try:
        resume_text = generate_resume_text(data)

        if job_desc.strip():
            score, matched_keywords, missing_keywords = calculate_ats_score(resume_text, job_desc)

            if score >= 90 and len(missing_keywords) <= 2:
                score = 100
        else:
            score = 0
            matched_keywords = []
            missing_keywords = []

        html_preview = get_template_html(selected_template_id, data)

        st.success("Resume generated successfully.")

        if job_desc.strip():
            st.subheader("ATS Score")
            st.metric("ATS Score", f"{score}/100")

            st.subheader("Matched Keywords")
            st.write(", ".join(matched_keywords) if matched_keywords else "No strong keyword matches found.")

            st.subheader("Missing Keywords")
            st.write(", ".join(missing_keywords[:20]) if missing_keywords else "No important keywords missing.")
        else:
            st.info("No job description provided, so ATS score was not calculated.")

        st.subheader("Resume Preview")
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
        else:
            st.warning("PDF generation failed. Please check your HTML template structure.")

    except FileNotFoundError:
        st.error(f"Template HTML or CSS file not found for template {selected_template_id}.")
    except Exception as e:
        st.error(f"Error while generating resume: {e}")
