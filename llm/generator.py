import openai
from docx import Document

def read_resume_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def generate_cover_letter(job, resume_text, api_key):
    openai.api_key = api_key
    prompt = f"""
You are applying for this role in the UK:

Title: {job.get('title') or job.get('jobTitle')}
Company: {job.get('employerName') or job.get('companyName')}
Description: {job.get('description') or job.get('jobDescription', '')}

Your resume summary:
{resume_text[:1000]}

Write a concise, UK-style cover letter tailored to this role.
"""
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
