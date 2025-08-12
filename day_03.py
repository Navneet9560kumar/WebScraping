import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/catalogue/"
START_PAGE = "page-1.html"

OUTPUT_PAGE = "books_data.json"
TARGET_COUNT = 70

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Failed to fetch url:", e)
        return [], None
    
    soup = BeautifulSoup(response.text, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 > a")
        title = title_tag.get("title")
        price = article.select_one("p.price_color").text.strip()
        print(f"{title} - {price}")
        books.append({"title": title, "price": price})
    
    # Find next page if available
    next_button = soup.select_one("li.next > a")
    next_url = urljoin(url, next_button["href"]) if next_button else None

    return books, next_url

# Example: Call the function
if __name__ == "__main__":
    url = urljoin(BASE_URL, START_PAGE)

    books_scraped = 0
    all_books = []

    while url and books_scraped < TARGET_COUNT:
        books, url = scrape_page(url)
        all_books.extend(books)
        books_scraped = len(all_books)
        print(f"Scraped {books_scraped} books so far...")

    # Save to JSON
    with open(OUTPUT_PAGE, "w", encoding="utf-8") as f:
        json.dump(all_books[:TARGET_COUNT], f, ensure_ascii=False, indent=2)

    print(f"Saved {min(TARGET_COUNT, len(all_books))} books to {OUTPUT_PAGE}")
