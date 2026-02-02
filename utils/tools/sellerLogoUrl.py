from dotenv import load_dotenv
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
import requests
import os

load_dotenv()


def sellerLogoUrl(url: str = "amazon.com") -> str:
    """Get the logo URL of a seller site.
    Input must be a seller domain only, e.g. amazon.com"""
    
    

    key = os.getenv("LOGO_DEV_PUBLISHABLE_KEY")
    if not key:
        raise ValueError("LOGO_DEV_PUBLISHABLE_KEY environment variable is not set.")
    
    seller_site = urlparse(url)
    seller_site = seller_site.netloc.replace("www.", "") if seller_site.netloc else seller_site.path

    try :
        logo_url = f"https://img.logo.dev/{seller_site}?token={key}&retina=true"
    except Exception as e:
        print("Error in forming logo URL:", e)
        logo_url = ""
    return logo_url





if __name__ == "__main__":
    url = "https://www.apple.com/in/shop/go/product/MFYP4HN/A"
    logo_url = sellerLogoUrl(url)

    response = requests.get(logo_url)
    response.raise_for_status()  # optional but good

    img = Image.open(BytesIO(response.content))
    img.show()

    