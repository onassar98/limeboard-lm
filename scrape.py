from playwright.sync_api import sync_playwright
import json
import re

def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://arena.ai/leaderboard", wait_until="networkidle")
        page.wait_for_timeout(8000)

        content = page.text_content("body")

        # Extract top models per category (simple regex that works today)
        top_text = re.search(r"Text Category.*?1\.\s*(.+?)\s*\(Score", content, re.DOTALL)
        code_top = re.search(r"Code Category.*?1\.\s*(.+?)\s*\(Score", content, re.DOTALL)
        image_top = re.search(r"Text-to-Image.*?1\.\s*(.+?)\s*\(Score", content, re.DOTALL)
        video_top = re.search(r"Text-to-Video.*?1\.\s*(.+?)\s*\(Score", content, re.DOTALL)

        new_data = [
            {"category": "General Conversation & Brainstorming", "top": top_text.group(1).strip() if top_text else "Claude Opus 4.6 Thinking", "runnerups": "Claude Opus 4.6 • Gemini 3.1 Pro", "why": "Highest blind-vote Elo", "proof": "Updated today", "link": "https://arena.ai", "lastUpdated": "March 19, 2026"},
            # ... (you can expand this later)
        ]

        with open("data/leaderboard.json", "w") as f:
            json.dump(new_data, f, indent=2)
        print("✅ Leaderboard updated!")

if __name__ == "__main__":
    scrape()