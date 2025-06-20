import requests

def fetch_reed_jobs(api_key, query, location):
    url = "https://www.reed.co.uk/api/1.0/search"
    headers = {"Authorization": f"Basic {api_key}"}
    params = {"keywords": query, "locationName": location, "resultsToTake": 10}
    return requests.get(url, headers=headers, params=params).json().get("results", [])
