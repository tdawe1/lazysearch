def generate_cover_letter(job, resume_text, api_key, mock=False):
    if mock:
        # Return a fixed dummy cover letter for testing
        return f"Dear Hiring Manager,\n\nI am very interested in the position of {job.get('title', 'the job')} at your company.\n\nBest regards,\nYour Name"

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
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
