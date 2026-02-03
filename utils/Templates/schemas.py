from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from PIL import Image

class ProductInfo(BaseModel):
    gender: str = Field(
        ...,
        examples=["male", "female", "unisex", "kids"],
        description="Gender catagory of the product."
    )
    masterCategory: str = Field(
        ...,
        examples=["Apparel", "Footwear", "Accessories"],
        description="Master category of the product."
    )
    subCategory: str = Field(
        ...,
        examples=["Oversized Shirts", "Sneakers", "Bags", "glasses", "Watch", "Cargo Pants"],
        description="Specific Sub category of the product."
    )
    Color: str = Field(
        ...,
        examples=["Dark Red", "Navy Blue", "Olive Green", "Light Black", "Off White", "Charcoal Grey"],
        description="Color of the product."
    )
    usage: str = Field(
        ...,
        examples=["Casual", "Formal", "Sports", "Party", "Beach"],
        description="Intended usage of the product."
    )
    productDisplayName: str = Field(
        ...,
        examples=["Turtle Check Men Navy Blue Shirt", "Peter England Men Party Blue Jeans", "Fastrack Unisex Black Sunglasses"],
        description="Display name of the product."
    )
    Brand: str = Field(
        ...,
        examples=["Nike", "Adidas", "Levi's", "Zara", "H&M", "Gucci"],
        description="Brand of the product."
    )

class shoppingProductInfo(BaseModel):
    product_name: str = Field(
        ...,
        examples=["Nike Air Max 270", "Adidas Ultraboost 21"],
        description="Name of the shopping product."
    )
    product_price: str = Field(
        ...,
        examples=["$150", "₹200"],
        description="Price of the shopping product with the currency."
    )
    product_url: str = Field(
        ...,
        examples=["https://www.nike.com/air-max-270", "https://www.adidas.com/ultraboost-21"],
        description="URL link to the shopping product."
    )
    product_rating: Optional[float] = Field(
        None,
        examples=[4.5, 4.0, 3.8],
        description="Customer rating of the shopping product."
    )
    product_ratings_count: Optional[int] = Field(
        None,
        examples=[150, 2000, 350],
        description="Number of ratings for the shopping product."
    )
    product_image_url: Optional[str] = Field(
        None,
        examples=["https://images.nike.com/air-max-270.jpg", "https://images.adidas.com/ultraboost-21.jpg"],
        description="Image URL of the shopping product."
    )
    seller_name: Optional[str] = Field(
        None,
        examples=["Nike Official Store", "Adidas Online Shop", "Amazon", "Flipkart"],
        description="Name of the seller or store."
    )
    seller_logo_url: Optional[str] = Field(
        None,
        examples=["https://logos.nike.com/logo.png", "https://logos.adidas.com/logo.png"],
        description="Logo URL of the seller or store."
    )
    

class ShoppingProductList(BaseModel):
    items: Optional[List[shoppingProductInfo]] = Field(default_factory=list)

class ImageState(BaseModel):
    img: Optional[Image.Image] = None
    prompt: str = "Fashion"

    boxes: Optional[List[List[int]]] = Field(default_factory=list)
    products: Optional[List[ProductInfo]] = Field(default_factory=list)
    segmented_imgs: Optional[List[Image.Image]] = Field(default_factory=list)

    nearest_items: Optional[Dict] = None
    errors: Optional[List[str]] = Field(default_factory=list)
    html_shopping: Optional[str] = Field(default_factory=str)
    productShoppingInfos: Optional[ShoppingProductList] = Field(default_factory=ShoppingProductList)

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )