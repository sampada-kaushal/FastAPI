import time
import os
import requests
from bs4 import BeautifulSoup
from app.models.product import Product
from app.utils.hashing import generate_image_filename
from typing import List, Optional
from fastapi import HTTPException
from pydantic import ValidationError
import logging

class DataExtractionService:
    def __init__(self, base_url: str, proxy: Optional[str] = None, retries: int = 3, delay: int = 2):
        self.base_url = base_url
        self.proxy = proxy
        self.retries = retries
        self.delay = delay

    # Function to retry in case of failures
    def retry_request(self, url):
        for attempt in range(self.retries):
            logging.info(f"Retrying attempt: {attempt + 1}"
            try:
                proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
                response = requests.get(url, proxies=proxies, timeout=10)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                if attempt < self.retries - 1:
                    time.sleep(self.delay)
                else:
                    raise HTTPException(status_code=500, detail=f"Failed to fetch data from {url}: {e}")

    # Function to extract details from HTML
    def scrape_page(self, page_url: str):
        response = self.retry_request(page_url)
        soup = BeautifulSoup(response.text, "html.parser")

        product_list = soup.select_one("ul.products.columns-4")
        if not product_list:
            raise HTTPException(status_code=500, detail="Product list not found on the page.")

        products = []
        # Iterate over all product items within the container of list("li")
        for product in product_list.select("li.product"):
            
            try: 
                img_tag = product.select_one("img")
                title = img_tag.get("alt", "").strip()
                logging.info(f"Scrapping for product : {title}")   
                price_str = float(product.select_one(".woocommerce-Price-amount").get_text(strip=True).replace("₹", ""))
                # Check for lazy-loaded image URL
                image_url = product.select_one("img")["data-lazy-src"] if product.select_one("img") else None
                # Fallback to the regular src attribute if lazy-loaded URL doesn't exist
                if not image_url:
                    image_url = product.select_one("img")["src"]
                try:
                    price = float(price_str)
                    if price < 0:
                        raise ValueError("Price cannot be negative.")
                except ValueError:
                    raise HTTPException(status_code=422, detail=f"Invalid price format: {price_str}")

                # Validate image URL type
                if not image_url.startswith(("http://", "https://")):
                    raise HTTPException(status_code=422, detail=f"Invalid image URL: {image_url}")

                # Download and validate image path
                image_filename = generate_image_filename(image_url)   
                if not os.path.exists(image_filename):
                    image_response = self.retry_request(image_url)
                    with open(image_filename, "wb") as img_file:
                        img_file.write(image_response.content)

                # Create and validate Product object
                product_data = Product(
                    product_title=title,
                    product_price=price,
                    path_to_image=image_filename
                )
                products.append(product_data)

            except (KeyError, AttributeError, ValidationError) as e:
                print(f"Skipping product due to error: {str(e)}")
                continue       
        return products