from fastapi import FastAPI, Depends, Query, HTTPException
from app.services.data_extraction_service import DataExtractionService
from app.services.cache_service import CacheService
from app.services.product_service import ProductService
from app.services.authentication_service import AuthService
from app.services.file_manager_service import FileManagerService
from app.services.notification_service import ConsoleNotificationStrategy
from typing import Optional
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app= FastAPI()

# Main controller endpoint logic
@app.get("/scrape/")

def scrape(
    pages: int = Query(..., description="Number of pages to scrape", ge=1),
    proxy: Optional[str] = Query(None, description="Proxy string for scraping"),
    token: str = Depends(AuthService.authenticate)
):
    logging.info("/scrape/ endpoint called")
    scraper = DataExtractionService(base_url="https://dentalstall.com/shop/page/", proxy=proxy)
    cache_manager = CacheService()
    notification = ConsoleNotificationStrategy()
    product_manager = ProductService(scraper, cache_manager, notification)

    all_products= product_manager.scrape_products(pages)

    FileManagerService.save_to_json(all_products)

    return {"message": f"Scraped {len(all_products)} products."}