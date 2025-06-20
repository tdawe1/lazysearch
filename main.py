from job_fetchers.reed import fetch_reed_jobs
from llm.generator import generate_cover_letter
from email_sender.smtp_sender import send_application
import json, csv, os

with open("config/settings.json") as f:
    config = json.load(f)

jobs = fetch_reed_jobs(config["reed_api_key"], config["search_query"])
applied_jobs = set()
if os.path.exists("logs/applied_jobs.csv"):
    with open("logs/applied_jobs.csv") as f:
        applied_jobs = set(row[0] for row in csv.reader(f))

for job in jobs:
    if job["jobId"] in applied_jobs:
        continue

    letter = generate_cover_letter(job, config["resume_text"], config["openai_api_key"])
    send_application(job["contactEmail"], f"Application: {job['title']}", letter, "resume.pdf",
                     config["email"], config["email_password"])

    with open("logs/applied_jobs.csv", "a", newline="") as f:
        csv.writer(f).writerow([job["jobId"]])
