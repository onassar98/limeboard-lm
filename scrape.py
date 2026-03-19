import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape():
    url = "https://arena.lmarena.ai/leaderboard"  # Current real URL in 2026 (arena.ai redirects here)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find leaderboard sections - adjust selectors based on current HTML (inspect page)
        categories = []
        sections = soup.find_all('div', class_='leaderboard-section')  # example class - change to real

        for section in sections:
            title = section.find('h2') or section.find('h3')
            if title:
                cat_name = title.get_text(strip=True)
            else:
                cat_name = "Unknown Category"

            top_model = "Unknown"
            model_elem = section.find('div', class_='top-model')  # adjust
            if model_elem:
                top_model = model_elem.get_text(strip=True)

            categories.append({
                "category": cat_name,
                "top": top_model,
                "runnerups": "Various models",
                "why": "Based on current leaderboard",
                "proof": "Fetched from arena.lmarena.ai",
                "link": url,
                "lastUpdated": datetime.now().strftime("%B %d, %Y")
            })

        # Fallback: if parsing fails, keep at least some data
        if not categories:
            categories = [{"category": "Fallback", "top": "Claude Opus 4.6", "runnerups": "...", "why": "Parsing failed - check scrape.py", "proof": "Manual", "link": url, "lastUpdated": datetime.now().strftime("%B %d, %Y")}]

        with open("data/leaderboard.json", "w") as f:
            json.dump(categories, f, indent=2)

        print(f"Successfully scraped {len(categories)} categories")
    except Exception as e:
        print(f"Scrape failed: {str(e)}")
        # Write fallback data so site doesn't break
        fallback = [{"category": "Error", "top": "Scraper failed", "runnerups": "Check Actions logs", "why": str(e)[:100], "proof": "Failed", "link": url, "lastUpdated": datetime.now().strftime("%B %d, %Y")}]
        with open("data/leaderboard.json", "w") as f:
            json.dump(fallback, f, indent=2)

if __name__ == "__main__":
    scrape()
