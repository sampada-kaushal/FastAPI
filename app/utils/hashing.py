import hashlib
from app.models.product import Product

def generate_image_filename(image_url: str) -> str:
    return f"images/{hashlib.md5(image_url.encode()).hexdigest()}.jpg"

def generate_product_hash(product: Product) -> str:
    return hashlib.md5(product.json().encode()).hexdigest()

def generate_product_dict_hash(product: Product) -> str:
    return hashlib.md5(product.encode()).hexdigest()