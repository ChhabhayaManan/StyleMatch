from typing import List
from PIL import Image
from schemas import ProductInfo
from langchain_core.output_parsers import JsonOutputParser
from google.genai import types

def prompt_template(nearest_items: List, img: Image.Image) -> List:
    System_message = """You are an AI assistant whose job is to inspect an image of Fashion Related Product and provide the desired information from the image.
                        There is some additional context provided about similar products found in a database. Use this information to help identify the product in the image.
                        Don't take the additional context as absolute truth, it may have inaccuracies, as some products in the database might be mislabeled or outdated or not in the database.
                        If the desired field is not clear or not well detected, return none for this field. Do not try to guess."""
    Human_message = "Examine the main fashion product type, brand, model, and color."
    instructions = JsonOutputParser(pydantic_object=ProductInfo).get_format_instructions()
    img_bytes = types.Part.from_bytes(
        data=img.tobytes(),
        mime_type=f"image/{img.format.lower()}"
    )
    nearest_items_info = f"""Here is some additional context about similar products found in a database:
    {nearest_items}
    Use this information to help identify the product in the image."""

    return [
        System_message,
        Human_message,
        instructions,
        img_bytes,
        nearest_items_info
    ]

