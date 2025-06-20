import json, csv, os
from llm.generator import read_resume_docx, generate_cover_letter
from email_sender.smtp_sender import send_application
from job_fetchers.reed import fetch_reed_jobs
from job_fetchers.indeed import fetch_indeed_jobs
from resume_loader import load_combined_resumes

docx_path = "path/to/your_resume.docx"
pdf_path = "path/to/your_resume.pdf"

resume_text = load_combined_resumes(docx_path, pdf_path)


mock_mode = True  # Set False when ready to use real API

for job in jobs:
    job_id = job.get("jobId") or job.get("id") or job.get("jobKey")
    if job_id in applied:
        continue
    cover = generate_cover_letter(job, resume_text, cfg["openai_api_key"], mock=mock_mode)

with open("config/settings.json") as f:
    cfg = json.load(f)

resume_text = read_resume_docx(cfg["resume_docx_path"])
applied = set()
if os.path.exists("logs/applied_jobs.csv"):
    with open("logs/applied_jobs.csv") as f:
        applied = {row[0] for row in csv.reader(f)}

for query in cfg["search_queries"]:
    for location in cfg["locations"]:
        jobs = fetch_reed_jobs(cfg["reed_api_key"], query, location) + \
               fetch_indeed_jobs(cfg["apify_token"], query, location)

        for job in jobs:
            job_id = job.get("jobId") or job.get("id") or job.get("jobKey")
            if job_id in applied:
                continue
            cover = generate_cover_letter(job, resume_text, cfg["openai_api_key"])
            contact_email = job.get("contactEmail") or "applications@example.com"
            send_application(contact_email,
                             f"Application: {job.get('title') or job.get('jobTitle')}",
                             cover,
                             cfg["resume_pdf_path"],
                             cfg["email"],
                             cfg["email_password"])
            with open("logs/applied_jobs.csv", "a", newline="") as f:
                csv.writer(f).writerow([job_id])
