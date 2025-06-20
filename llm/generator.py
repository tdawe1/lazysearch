import openai
from docx import Document

def read_resume_docx(docx_path):
    """
    Read text content from a DOCX file and return as a single string.
    """
    try:
        doc = Document(docx_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

def generate_cover_letter(job, resume_text, api_key, mock=False):
    if mock:
        return (
            f"Dear Hiring Manager,\n\n"
            f"I am very interested in the position of {job.get('title', 'the job')} at your company.\n\n"
            "Best regards,\nYour Name"
        )

    openai.api_key = api_key

    # Limit resume summary length to avoid token overflow
    resume_snippet = resume_text[:1000] if resume_text else "No resume summary provided."

    prompt = f"""
You are applying for this role in the UK:

Title: {job.get('title') or job.get('jobTitle', 'Unknown')}
Company: {job.get('employerName') or job.get('companyName', 'Unknown')}
Description: {job.get('description') or job.get('jobDescription', 'No description provided.')}

Your resume summary:
{resume_snippet}

Write a concise, professional UK-style cover letter tailored to this role.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "Could not generate cover letter due to API error."
