from pydantic import BaseModel, Field

class Product(BaseModel):
    product_title: str = Field(..., min_length=1, max_length=255, description="Title of product")
    product_price: float = Field(..., ge=0, le=1e6, description="Price must be a non-negative value.")
    path_to_image: str = Field(..., description="Path to the product image.")

    def json(self, **kwargs):
        product_json=super().json(**kwargs)
        return product_json
