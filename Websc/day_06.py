import os
import requests
import textwrap
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_DIR = "quotes"

def fetch_quotes():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = soup.select("div.quote")

    quotes_data = []

    for q in quotes[:5]:
        quote_text = q.find("span", class_="text").text.strip()
        author = q.find("small", class_="author").text.strip()
        quotes_data.append((quote_text, author))

    return quotes_data  # outside loop

def create_image(text, author, index):
    width, height = 800, 400
    background_color = "#f8d77f"
    text_color = "#262626"

    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default()
    author_font = ImageFont.load_default()

    wrapped = textwrap.fill(text, width=60)
    author_text = f"- {author}"

    y_text = 60
    draw.text((40, y_text), wrapped, font=font, fill=text_color)

    y_text += wrapped.count("\n") * 15 + 40
    draw.text((500, y_text), author_text, font=author_font, fill=text_color)

    # save image
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    filename = os.path.join(OUTPUT_DIR, f"quote_{index + 1}.png")
    image.save(filename)
    print(f"✅ saved: {filename}")

def main():
    quotes = fetch_quotes()
    for idx, (text, author) in enumerate(quotes):
        create_image(text, author, idx)

if __name__ == "__main__":
    main()
