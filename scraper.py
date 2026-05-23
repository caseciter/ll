import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime
import re
import sys

def scrape_livelaw_judgments(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all articles/cards (common tag for LiveLaw listing)
        articles = soup.find_all('article') 
        
        filtered_content = []
        for article in articles:
            # Check if "LiveLaw (SC)" is in the text of the article
            if re.search(r'LiveLaw\s*\(SC\)', article.get_text(), re.IGNORECASE):
                filtered_content.append(str(article))
        
        if filtered_content:
            filename = f"livelaw_sc_judgments_{datetime.now().strftime('%Y-%m-%d')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# LiveLaw (SC) Judgments - {datetime.now().date()}\n\n")
                for item in filtered_content:
                    f.write(md(item) + "\n---\n")
            print(f"Successfully saved filtered content to {filename}")
        else:
            print("No articles with 'LiveLaw (SC)' citation found.")
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        sys.exit(1)

if __name__ == "__main__":
    scrape_livelaw_judgments("https://www.livelaw.in/sc-judgments")
