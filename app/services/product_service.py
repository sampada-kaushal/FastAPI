from app.services.data_extraction_service import DataExtractionService
from app.services.cache_service import CacheService
from app.services.notification_service import NotificationStrategy
from app.models.product import Product
from fastapi import HTTPException
import logging

class ProductService:
    def __init__(self, scraper: DataExtractionService, cache_manager: CacheService, notification: NotificationStrategy):
        self.scraper=scraper
        self.cache_manager=cache_manager
        self.notification= notification

    # Function to scrape products page-wise
    def scrape_products(self, pages: int):
        if not isinstance(pages, int) or pages <=0:
            raise ValueError("Pages must be a positive integer.")
        all_products=[]
        for page_num in range (1, pages+1):
            logging.info(f"Retrieving from page {page_num}")
            page_url=f"{self.scraper.base_url}{page_num}/"
            try:
                scraped_products=self.scraper.scrape_page(page_url)
                
                for product in scraped_products:
                    if not self.cache_manager.is_product_cached(product):
                        self.cache_manager.cache_product(product)
                        all_products.append(product) 
            except HTTPException as e:
                logging.error("Skipping page")
                print(f"Skipping page {page_num} due to error: {e.detail}")
        self.notification.notify(f"Scraping session completed. {len(all_products)} products were scraped.")        
        return all_products        