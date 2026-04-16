import re
from collections import Counter


def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_keywords(job_desc, limit=30):
    stop_words = {
        "the", "and", "for", "with", "you", "your", "are", "this", "that", "will",
        "have", "has", "our", "from", "but", "not", "all", "can", "their", "who",
        "how", "why", "into", "about", "them", "they", "his", "her", "she", "him",
        "was", "were", "been", "being", "job", "role", "work", "must", "should",
        "good", "strong", "ability", "experience", "years", "year", "team", "using",
        "use", "used", "required", "preferred", "candidate", "position", "skills"
    }

    text = clean_text(job_desc)
    words = text.split()
    filtered = [w for w in words if len(w) > 2 and w not in stop_words]

    freq = Counter(filtered)
    return [word for word, _ in freq.most_common(limit)]


def calculate_ats_score(resume_text, job_desc):
    resume_clean = clean_text(resume_text)
    jd_keywords = extract_keywords(job_desc)

    matched_keywords = [kw for kw in jd_keywords if kw in resume_clean]
    missing_keywords = [kw for kw in jd_keywords if kw not in resume_clean]

    score = 0

    if jd_keywords:
        score += min(int((len(matched_keywords) / len(jd_keywords)) * 60), 60)

    required_sections = ["summary", "education", "skills", "projects", "experience"]
    found_sections = sum(1 for sec in required_sections if sec in resume_clean)
    score += min(found_sections * 5, 25)

    if any(x in resume_clean for x in ["email", "phone", "linkedin", "github"]):
        score += 5

    if score > 100:
        score = 100

    return score, matched_keywords, missing_keywords
