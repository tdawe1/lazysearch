import json, csv, os
from llm.generator import read_resume_docx, generate_cover_letter
from email_sender.smtp_sender import send_application
from job_fetchers.reed import fetch_reed_jobs
from job_fetchers.indeed import fetch_indeed_jobs
from resume_loader import load_combined_resumes

def test_mode(cfg):
    print("=== Running test mode ===")
    resume_text = load_combined_resumes(cfg["resume_docx_path"], cfg["resume_pdf_path"])
    print(f"Loaded combined resume text length: {len(resume_text)}")

    query = cfg["search_queries"][0]
    location = cfg["locations"][0]
    print(f"Fetching jobs for query='{query}', location='{location}'...")
    jobs = fetch_reed_jobs(cfg["reed_api_key"], query, location) + \
           fetch_indeed_jobs(cfg["apify_token"], query, location)
    print(f"Jobs fetched: {len(jobs)}")

    if not jobs:
        print("No jobs found, stopping test.")
        return

    job = jobs[0]
    print(f"Generating cover letter for first job: {job.get('title') or job.get('jobTitle')}")
    cover = generate_cover_letter(job, resume_text, cfg["openai_api_key"], mock=True)
    print("Cover letter:\n", cover)

    print("Skipping sending email in test mode.")

def main():
    with open("config/settings.json") as f:
        cfg = json.load(f)

    resume_text = load_combined_resumes(cfg["resume_docx_path"], cfg["resume_pdf_path"])
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

if __name__ == "__main__":
    TEST = True  # Change to False to run full job application process

    with open("config/settings.json") as f:
        cfg = json.load(f)

    if TEST:
        test_mode(cfg)
    else:
        main()
