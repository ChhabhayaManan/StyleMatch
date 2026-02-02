from html import parser
from typing import List
from PIL import Image
from utils.Templates.schemas import ProductInfo, shoppingProductInfo
from langchain_core.output_parsers import JsonOutputParser
from google.genai import types
from io import BytesIO


def prompt_template_Recognization(nearest_items: List, img: Image.Image) -> List:
    if img.mode != "RGB":
        img = img.convert("RGB")

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=95)

    System_message = """Analyze the fashion product image and extract the required details. 
You may use provided similar-product context as a hint, but it may be inaccurate, or unrelated as shortage of data. 
If a field is unclear, return `none` and do not guess."""
    Human_message = "Examine the main fashion product type, brand, model, and color."
    instructions = JsonOutputParser(pydantic_object=ProductInfo).get_format_instructions()
    img_bytes = types.Part.from_bytes(
        data=buf.getvalue(),
        mime_type="image/jpeg"
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


def shoppingInfoPrompt(products: ProductInfo):
    parser = JsonOutputParser(pydantic_object=shoppingProductInfo)
    instructions = parser.get_format_instructions()
    prompt = {
        "SystemMessage" : """You are a helpful assistant that provides shopping information for fashion products. Given a product information, make a search query to find relevant shopping data including product price, URL, rating, reviews count, image link, seller name, and seller logo URL
                      it is not necessary to make query with all the information just use product name and brand. use tools for getting data from web and seller logo URL. Provide at max 5 results of shopping data in JSON format.
                      you have 2 tools available: 1. shoppingDatafromWeb 2. sellerLogoUrl use them sequencially to get the required information.""",
        "HumanMessage" : f"""Product Information: {products}
                      instuctions for output format for one: {instructions}
                    you need to provide list of these objects"""
    }
    return prompt
