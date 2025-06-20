import json
import csv
import os
import sys
import logging
from llm.generator import read_resume_docx, generate_cover_letter
from email_sender.smtp_sender import send_application
from job_fetchers.reed import fetch_reed_jobs
from job_fetchers.indeed import fetch_indeed_jobs
from resume_loader import load_combined_resumes

# Setup logging for test mode
logging.basicConfig(
    filename="logs/test_mode.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def test_mode(cfg):
    print("=== Running test mode ===")
    resume_text = load_combined_resumes(cfg["resume_docx_path"], cfg["resume_pdf_path"])
    logging.info(f"Loaded combined resume text length: {len(resume_text)}")
    print(f"Loaded combined resume text length: {len(resume_text)}")

    query = cfg["search_queries"][0]
    location = cfg["locations"][0]
    print(f"Fetching 1 job each from Reed and Indeed for query='{query}', location='{location}'...")
    logging.info(f"Fetching 1 job each from Reed and Indeed for query='{query}', location='{location}'...")

    # Note: fetch functions must support 'limit' param (you might need to add this)
    jobs = fetch_reed_jobs(cfg["reed_api_key"], query, location, limit=1) + \
           fetch_indeed_jobs(cfg["apify_token"], query, location, limit=1)
    print(f"Jobs fetched: {len(jobs)}")
    logging.info(f"Jobs fetched: {len(jobs)}")

    if not jobs:
        print("No jobs found, stopping test.")
        logging.info("No jobs found, stopping test.")
        return

    job = jobs[0]
    job_title = job.get('title') or job.get('jobTitle') or "Unknown Title"
    print(f"Generating cover letter for job: {job_title}")
    logging.info(f"Generating cover letter for job: {job_title}")

    cover = generate_cover_letter(job, resume_text, cfg["openai_api_key"], mock=True)
    print("Cover letter snippet:\n", cover[:300], "...\n")
    logging.info(f"Cover letter generated:\n{cover}")

    print("Skipping sending email in test mode.")
    logging.info("Skipped sending email in test mode.")

def main():
    with open("config/settings.json") as f:
        cfg = json.load(f)

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_mode(cfg)
        return

    resume_text = load_combined_resumes(cfg["resume_docx_path"], cfg["resume_pdf_path"])
    applied = set()
    if os.path.exists("logs/applied_jobs.csv"):
        with open("logs/applied_jobs.csv") as f:
            applied = {row[0] for row in csv.reader(f)}

    for query in cfg["search_queries"]:
        for location in cfg["locations"]:
            jobs = fetch_reed_jobs(cfg["reed_api_key"], query, location, limit=1, logger=logfile) + \
            fetch_indeed_jobs(cfg["apify_token"], query, location, limit=1, logger=logfile)


            for job in jobs:
                job_id = job.get("jobId") or job.get("id") or job.get("jobKey")
                if job_id in applied:
                    continue

                cover = generate_cover_letter(job, resume_text, cfg["openai_api_key"])
                contact_email = job.get("contactEmail") or "applications@example.com"
                send_application(
                    contact_email,
                    f"Application: {job.get('title') or job.get('jobTitle')}",
                    cover,
                    cfg["resume_pdf_path"],
                    cfg["email"],
                    cfg["email_password"]
                )
                with open("logs/applied_jobs.csv", "a", newline="") as f:
                    csv.writer(f).writerow([job_id])
                applied.add(job_id)

if __name__ == "__main__":
    main()
