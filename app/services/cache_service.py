import redis
from app.models.product import Product
from app.utils.hashing import generate_product_hash
from app.utils.hashing import generate_product_dict_hash
from typing import Union

class CacheService:
    def __init__(self, redis_host="localhost", redis_port="6379"):
        self.redis_client=redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    # Checking is product is already added in the cache
    def is_product_cached(self, product: Union[Product, dict]):
        if isinstance(product, Product):
            product_hash=generate_product_hash(product)
        elif isinstance(product, dict):
            product_hash=generate_product_dict_hash
        else:
            raise TypeError("Product must of type Product or dict")
        return self.redis_client.exists(product_hash)          
        
    # If not already in cache, adding it to cache
    def cache_product(self, product: Product):       
        if not isinstance(product, Product):
            raise TypeError("Product must of type Product")
        product_hash = generate_product_hash(product)
        self.redis_client.set(product_hash, 1)  