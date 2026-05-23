import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup


def fetch_livelaw_headings():
    url = "https://www.livelaw.in/sc-judgments"
    # LiveLaw blocks default python-requests user-agents, so we must mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching LiveLaw: {e}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    headings = []
    # LiveLaw typical heading containers for section feeds
    # If their layout shifts, these selectors can be adjusted
    articles = soup.find_all(["h1", "h2", "h3"], class_="heading") or soup.select(
        ".news-heading a, .heading a"
    )

    for item in articles:
        text = item.get_text(strip=True)
        if text and text not in headings:
            headings.append(text)

    # Fallback to general link scraping if tight classes match nothing
    if not headings:
        for link in soup.find_all("a", href=True):
            if "/top-stories/" in link["href"] or "/news-updates/" in link["href"]:
                text = link.get_text(strip=True)
                if len(text) > 30 and text not in headings:
                    headings.append(text)

    return headings[:15]  # Grab top 15 latest entries


def update_markdown_file(headings):
    if not headings:
        print("No new headings found to write.")
        return

    filename = "judgments.md"
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    # Generate the chunk of Markdown content
    new_content = f"\n## LiveLaw SC Judgments Updates — {current_time}\n"
    for heading in headings:
        new_content += f"* {heading}\n"

    # Read existing content to prepend/append or create a fresh file
    file_exists = os.path.exists(filename)

    if file_exists:
        with open(filename, "r", encoding="utf-8") as file:
            existing_data = file.read()
        # Prepending puts the newest updates right at the top of the file
        final_content = new_content + "\n---\n" + existing_data
    else:
        final_content = (
            "# Supreme Court Judgments Logs\n" + new_content
        )

    with open(filename, "w", encoding="utf-8") as file:
        file.write(final_content)

    print(f"Successfully updated {filename} with {len(headings)} items.")


if __name__ == "__main__":
    latest_headings = fetch_livelaw_headings()
    update_markdown_file(latest_headings)
