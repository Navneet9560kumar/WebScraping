import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import wget

BASE_URL = "https://books.toscrape.com/"
IMAGE_DIR = "images"

def sanitize_filename(title):
    return re.sub(r'[^\w\-_.]', '', title).replace(" ", "_")

def downlode_image(img_url, filename):
    try:
        response = requests.get(img_url, stream=True, timeout=10)
        with open(filename, 'wb') as f:  # FIX: binary mode
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        print(f"Failed to download {filename} - {e}")

def scrape_and_download_images():
    url = BASE_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # FIX: CSS selector inside quotes
    books = soup.select("article.product_pod")[:20]

    if not os.path.exists(IMAGE_DIR):
        os.makedirs(IMAGE_DIR)

    for book in books:
        title = book.h3.a['title']
        relative_img = book.find("img")["src"]
        image_url = urljoin(BASE_URL, relative_img)  # FIX: join URL

        filename = sanitize_filename(title) + ".jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

    print(f"Downloading: {title}")
    #   downlode_image(image_url, filepath)  # FIX: correct vars
    wget.download(image_url, filepath)

    print("All 10 book covers downloaded to 'images' folder.")

if __name__ == "__main__":
    scrape_and_download_images()
