from typing import List
from PIL import Image
from utils.Templates.schemas import ProductInfo
from langchain_core.output_parsers import JsonOutputParser
from google.genai import types
from io import BytesIO
def prompt_template(nearest_items: List, img: Image.Image) -> List:
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

