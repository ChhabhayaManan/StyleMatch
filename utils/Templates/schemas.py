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



class ImageState(BaseModel):
    img: Optional[Image.Image] = None
    prompt: str = "Fashion"

    boxes: List[List[int]] = Field(default_factory=list)
    products: List[ProductInfo] = Field(default_factory=list)
    segmented_imgs: List[Image.Image] = Field(default_factory=list)

    nearest_items: Optional[Dict] = None
    errors: List[str] = Field(default_factory=list)

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )