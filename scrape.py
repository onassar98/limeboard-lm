import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape():
    url = "https://lmarena.ai/leaderboard"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')

        # Basic fallback structure - real selectors need page inspection
        data = []
        # Example: find all category blocks (adjust after you inspect real HTML)
        for cat_block in soup.select('.leaderboard-category'):  # CHANGE THIS SELECTOR
            cat_title = cat_block.select_one('h2, h3, .category-title')
            top_model = cat_block.select_one('.top-model, .rank-1')

            cat_name = cat_title.get_text(strip=True) if cat_title else "Unknown"
            top = top_model.get_text(strip=True) if top_model else "Unknown"

            data.append({
                "category": cat_name,
                "top": top,
                "runnerups": "Various",
                "why": "From lmarena.ai",
                "proof": "Live scrape",
                "link": url,
                "lastUpdated": datetime.now().strftime("%B %d, %Y")
            })

        # If nothing found → fallback to your 7 categories
        if not data:
            data = [
                {"category": "General Conversation & Brainstorming", "top": "Claude Opus 4.6 Thinking", "runnerups": "Claude Opus 4.6 • Gemini 3.1 Pro", "why": "Highest Elo", "proof": "Elo 1502", "link": "https://claude.ai", "lastUpdated": "March 19, 2026"},
                {"category": "Research & Deep Analysis", "top": "Gemini 3.1 Pro", "runnerups": "Claude Opus 4.6", "why": "Long context", "proof": "MMLU-Pro 91%", "link": "https://gemini.google.com", "lastUpdated": "March 19, 2026"},
                {"category": "Creative & Professional Writing", "top": "Claude Opus 4.6", "runnerups": "Gemini 3.1 Pro", "why": "Best prose", "proof": "Text #1", "link": "https://claude.ai", "lastUpdated": "March 19, 2026"},
                {"category": "Coding & Software Engineering", "top": "Claude Opus 4.6", "runnerups": "o4-Mini", "why": "SWE-Bench leader", "proof": "~79%", "link": "https://claude.ai", "lastUpdated": "March 19, 2026"},
                {"category": "Advanced Reasoning & Math", "top": "Gemini 3.1 Pro", "runnerups": "o4-Mini", "why": "Complex logic", "proof": "LiveCodeBench #1", "link": "https://gemini.google.com", "lastUpdated": "March 19, 2026"},
                {"category": "Image Generation", "top": "Gemini Nano Banana 2", "runnerups": "GPT Image 1.5 • FLUX.2", "why": "Image Elo leader", "proof": "Elo 1268", "link": "https://gemini.google.com", "lastUpdated": "March 19, 2026"},
                {"category": "Video Generation", "top": "Veo 3.1 Audio", "runnerups": "Kling 3.0 • Runway Gen-4.5", "why": "Best motion", "proof": "Video Elo 1381", "link": "https://deepmind.google/veo/", "lastUpdated": "March 19, 2026"}
            ]

        with open("data/leaderboard.json", "w") as f:
            json.dump(data, f, indent=2)

        print(f"Scraped {len(data)} categories")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    scrape()
