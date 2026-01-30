from typing import List, Optional
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
    img : Image.Image
    boxes : Optional[List[List[int]]] = Field(default_factory=list)
    products : Optional[List[ProductInfo]] = Field(default_factory=list)
    segmented_imgs : Optional[List[Image.Image]] = Field(default_factory=list)
    errors : Optional[List[str]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
