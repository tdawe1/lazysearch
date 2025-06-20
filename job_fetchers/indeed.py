from apify_client import ApifyClient

def fetch_indeed_jobs(apify_token, query, location):
    client = ApifyClient(apify_token)
    run_input = {
        "position": query,
        "country": "GB",  # Use 'GB' for the United Kingdom
        "location": location,
        "maxItems": 10
    }
    run = client.actor("misceres/indeed-scraper").call(run_input=run_input)
    dataset_id = run["defaultDatasetId"]
    return list(client.dataset(dataset_id).iterate_items())
