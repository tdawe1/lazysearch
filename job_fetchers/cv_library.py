import requests

def fetch_cv_jobs(query, location):
    url = "https://www.cv-library.co.uk/search-jobs-json"
    params = {"keywords": query, "location": location, "resultsToTake": 10}
    return requests.get(url, params=params).json().get("jobs", [])
