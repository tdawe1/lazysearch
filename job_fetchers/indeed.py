from apify_client import ApifyClient
import time

def fetch_indeed_jobs(apify_token, query, location, limit=None, retries=2, delay=3, logger=None):
    client = ApifyClient(apify_token)
    run_input = {
        "position": query,
        "country": "GB",
        "location": location,
        "maxItems": limit or 10
    }

    for attempt in range(retries + 1):
        try:
            run = client.actor("misceres/indeed-scraper").call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]
            jobs = list(client.dataset(dataset_id).iterate_items())
            return jobs[:limit] if limit else jobs
        except Exception as e:
            msg = f"[ERROR] Indeed fetch failed (attempt {attempt + 1}/{retries + 1}): {e}"
            print(msg)
            if logger:
                logger.write(msg + "\n")
            if attempt < retries:
                time.sleep(delay)

    return []
