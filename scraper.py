import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime
import sys

def scrape_livelaw_judgments(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.find('body') 
        
        if content:
            markdown_content = md(str(content))
            filename = f"livelaw_judgments_{datetime.now().strftime('%Y-%m-%d')}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# LiveLaw SC Judgments - {datetime.now().date()}\n\n")
                f.write(markdown_content)
            print(f"Successfully saved to {filename}")
        else:
            print("Error: Could not find main content on the page.")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        sys.exit(1)

if __name__ == "__main__":
    scrape_livelaw_judgments("https://www.livelaw.in/sc-judgments")
