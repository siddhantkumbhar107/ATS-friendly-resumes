from jinja2 import Template


def generate_resume_text(data):
    return f"""
{data.get('full_name', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
LinkedIn: {data.get('linkedin', '')}
GitHub: {data.get('github', '')}
Address: {data.get('address', '')}

PROFESSIONAL SUMMARY
{data.get('summary', '')}

EDUCATION
{data.get('education', '')}

SKILLS
{data.get('skills', '')}

PROJECTS
{data.get('projects', '')}

EXPERIENCE
{data.get('experience', '')}

CERTIFICATIONS
{data.get('certifications', '')}

ACHIEVEMENTS
{data.get('achievements', '')}
""".strip()


def load_template(template_id):
    with open(f"html_templates/template_{template_id}.html", "r", encoding="utf-8") as f:
        html = f.read()

    with open(f"assets/css/template_{template_id}.css", "r", encoding="utf-8") as f:
        css = f.read()

    html = html.replace("</head>", f"<style>{css}</style></head>")
    return html


def get_template_html(template_id, data):
    html = load_template(template_id)
    template = Template(html)
    return template.render(**data)
