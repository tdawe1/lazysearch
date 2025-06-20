import requests
import time

def fetch_reed_jobs(api_key, query, location, limit=None, retries=2, delay=3, logger=None):
    url = "https://www.reed.co.uk/api/1.0/search"
    headers = {"Authorization": f"Basic {api_key}"}
    params = {
        "keywords": query,
        "locationName": location,
        "resultsToTake": limit or 50
    }

    for attempt in range(retries + 1):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            jobs = response.json().get("results", [])
            return jobs[:limit] if limit else jobs
        except Exception as e:
            msg = f"[ERROR] Reed fetch failed (attempt {attempt + 1}/{retries + 1}): {e}"
            print(msg)
            if logger:
                logger.write(msg + "\n")
            if attempt < retries:
                time.sleep(delay)

    return []
