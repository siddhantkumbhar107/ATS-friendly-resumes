from jinja2 import Template


def generate_resume_text(data):
    return f"""
{data['full_name']}
Email: {data['email']}
Phone: {data['phone']}
LinkedIn: {data['linkedin']}
GitHub: {data['github']}
Address: {data['address']}

SUMMARY
{data['summary']}

EDUCATION
{data['education']}

SKILLS
{data['skills']}

PROJECTS
{data['projects']}

EXPERIENCE
{data['experience']}

CERTIFICATIONS
{data['certifications']}

ACHIEVEMENTS
{data['achievements']}
""".strip()


def get_template_html(template_name, data):
    base_html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; }
            h1 { text-align: center; margin-bottom: 5px; }
            .contact { text-align: center; font-size: 12px; margin-bottom: 20px; }
            h2 { border-bottom: 1px solid #333; padding-bottom: 4px; margin-top: 20px; }
            p { font-size: 13px; line-height: 1.5; }
        </style>
    </head>
    <body>
        <h1>{{ full_name }}</h1>
        <div class="contact">
            {{ email }} | {{ phone }} | {{ linkedin }} | {{ github }} | {{ address }}
        </div>

        <h2>Professional Summary</h2>
        <p>{{ summary }}</p>

        <h2>Education</h2>
        <p>{{ education }}</p>

        <h2>Skills</h2>
        <p>{{ skills }}</p>

        <h2>Projects</h2>
        <p>{{ projects }}</p>

        <h2>Experience</h2>
        <p>{{ experience }}</p>

        <h2>Certifications</h2>
        <p>{{ certifications }}</p>

        <h2>Achievements</h2>
        <p>{{ achievements }}</p>
    </body>
    </html>
    """
    template = Template(base_html)
    return template.render(**data)
