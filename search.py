import json
import requests
from parallel import Parallel

# API Keys
PARALLEL_API_KEY = "ly8rXA18Oe9z0HroJZCwG6sWVCbfyWT98RZB_8QW"
SERPER_API_KEY = "a0c0d88e010033e189bfe9b12a978865479a1e26"  # TODO: Replace with your Serper API key

def scrape_url_to_markdown(url: str) -> str | None:
    """Scrape a URL using Serper and return markdown content."""
    try:
        response = requests.post(
            "https://scrape.serper.dev",
            headers={
                "X-API-KEY": SERPER_API_KEY,
                "Content-Type": "application/json"
            },
            json={"url": url}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("markdown") or data.get("text")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

# Step 1: Search using Parallel API
client = Parallel(api_key=PARALLEL_API_KEY)
response = client.beta.search(
  objective="Find official press releases announcing clinical trial results, development milestones, or strategic decisions related to the investigational drug litifilimab (BIIB059).",
  search_queries=[
    "BIIB059 press release",
    "litifilimab press release",
    "Biogen litifilimab announcement",
    "BIIB059 Phase 2 press release",
    "BIIB059 Phase 3 update press release"
  ],
  max_results=20
)

# Step 2: Convert response to dict
results_data = response.model_dump()

# Step 3: Scrape each URL and replace excerpts with markdown
if results_data.get("results"):
    for result in results_data["results"]:
        url = result.get("url")
        if url:
            print(f"Scraping: {url}")
            markdown_content = scrape_url_to_markdown(url)
            if markdown_content:
                result["markdown"] = markdown_content
            # Keep original excerpts as fallback (they remain in the result)

# Step 4: Save to JSON file
with open("search_results.json", "w", encoding="utf-8") as f:
    json.dump(results_data, f, indent=2, ensure_ascii=False)

print(f"Saved {len(results_data.get('results', []))} results to search_results.json")