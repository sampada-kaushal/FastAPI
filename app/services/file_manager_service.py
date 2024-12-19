import json
from typing import List
from app.models.product import Product
import logging

class FileManagerService:
    @staticmethod
    def save_to_json(data: List[Product], filename="products.json"):
        # Loads existing data
        existing_data = []
        try:
            logging.info("Saving to file")
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # if file does not exist or is invalid, start with an empty list
            existing_data = []

        # Convert existing data into a set of unique tuples for comparison
        existing_set = {
            (item["product_title"], item["product_price"], item["path_to_image"])
            for item in existing_data
        }

        # Filter incoming data to include only unique products
        unique_data = [
            product.dict()
            for product in data
            if (product.product_title, product.product_price, product.path_to_image)
            not in existing_set
        ]

        # Merge the new unique data with the existing data
        merged_data = existing_data + unique_data

        # Save the updated data back to the file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)

        # Log the results
        logging.info(f"{len(unique_data)} new products added to {filename}.")
