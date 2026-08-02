# Assignment - Web Scraping using Python
# This program extracts product details (title, price, image) from a website,
# downloads the image, and compares the price with a target price.
# Website used: https://books.toscrape.com (a site made for practicing scraping)

import os
import requests
from bs4 import BeautifulSoup

# folder to save downloaded images
IMAGE_FOLDER = "product_images"

# price we want to compare with
TARGET_PRICE = 30.00

# list of product urls (can add more)
PRODUCT_URLS = [
    "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "https://books.toscrape.com/catalogue/soumission_998/index.html",
    "https://books.toscrape.com/catalogue/sharp-objects_997/index.html",
]

headers = {"User-Agent": "Mozilla/5.0"}


# function to fetch the html of a page
def fetch_page(url):
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"   # fix for weird symbols like £ showing wrong
    if res.status_code == 200:
        return res.text
    else:
        print("Failed to fetch page:", url)
        return None


# function to get title, price and image url from the page
def get_product_details(html, url):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1").text

    price_text = soup.find("p", class_="price_color").text
    price_text = price_text.replace("£", "").replace("Â", "")
    price = float(price_text)

    img_tag = soup.find("div", class_="item active").find("img")
    img_url = requests.compat.urljoin(url, img_tag["src"])

    return title, price, img_url


# function to download the product image
def download_image(img_url, title):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    file_name = title.replace(" ", "_") + ".jpg"
    file_path = os.path.join(IMAGE_FOLDER, file_name)

    img_data = requests.get(img_url, headers=headers).content
    with open(file_path, "wb") as f:
        f.write(img_data)

    print("Image saved:", file_path)


# function to compare price with target price
def compare_price(price):
    if price < TARGET_PRICE:
        print("Price is LESS than target price. Good deal!")
    elif price > TARGET_PRICE:
        print("Price is MORE than target price.")
    else:
        print("Price is SAME as target price.")


# main program - loop through all product urls
for url in PRODUCT_URLS:
    print("\n----------------------------------------")
    print("URL:", url)

    html = fetch_page(url)
    if html is None:
        continue

    title, price, img_url = get_product_details(html, url)

    print("Title:", title)
    print("Price: £", price)
    print("Image URL:", img_url)

    download_image(img_url, title)
    compare_price(price)

print("\n----------------------------------------")
print("Scraping finished for all products.")