import csv
import requests
from bs4 import BeautifulSoup

# ✅ Target Hacker News
HN_URL = "https://news.ycombinator.com/"
CSV_FILE = "hn_top20.csv"

def fetch_top_post():
    try:
        response = requests.get(HN_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Network error:\n{e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    post_links = soup.select("span.titleline > a")

    posts = []
    for link in post_links[:20]:  # Get top 20 posts
        title = link.text.strip()
        url = link.get("href", "").strip()
        print(f"{title}\n{url}\n")
        posts.append({"title": title, "url": url})

    return posts  # ✅ Move this outside the loop

def save_to_csv(posts):
    if not posts:
        print("Nothing to save")
        return

    # Save to CSV
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(posts)

    print(f"\n✅ Data saved to {CSV_FILE}")

def main():
    print("Scraping the HN portal....")
    posts = fetch_top_post()
    print("Collected all data...")
    save_to_csv(posts)

# ✅ Run only if this file is the main script
if __name__ == "__main__":
    main()
