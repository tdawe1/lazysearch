import requests

def fetch_cv_jobs(query, location):
    url = f"https://www.cv-library.co.uk/search-jobs-json"
    params = {"keywords": query, "location": location, "resultsToTake": 10}
    r = requests.get(url, params=params)
    return r.json().get("jobs", [])
