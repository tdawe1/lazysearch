# test_run.py
from llm.generator import generate_cover_letter

def main():
    print("Running simple test...")

    # Dummy job and resume data
    job = {"title": "Software Engineer"}
    resume_text = "Experienced software developer with Python skills."

    # Call generate_cover_letter with mock=True to avoid API calls
    cover_letter = generate_cover_letter(job, resume_text, "fake-key", mock=True)

    print("Cover letter generated:")
    print(cover_letter)

if __name__ == "__main__":
    main()
