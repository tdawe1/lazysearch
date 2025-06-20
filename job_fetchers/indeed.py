from apify_client import ApifyClient

def fetch_indeed_jobs(apify_token, query, location):
    client = ApifyClient(apify_token)
    run = client.actor("drobnikj/indeed-scraper").call({
        "query": query,
        "location": location,
        "maxItems": 10
    })
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())
