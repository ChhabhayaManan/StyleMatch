import os
import http.client
import json
from dotenv import load_dotenv
import requests
from urllib.parse import quote
from utils.Templates.schemas import shoppingProductInfo, ShoppingProductList
load_dotenv()

def shoppingDatafromWeb(query: str, limit: int = 10, region: str = 'in'):
    """Find shopping data for a product from the web. 
    Returns image link, price, rating, reviews count, product URL, and store name. 
    Input must be a plain product search query string."""
    conn = http.client.HTTPSConnection("real-time-product-search.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': os.getenv("X_API_KEY"),
        'x-rapidapi-host': "real-time-product-search.p.rapidapi.com"
    }
    query += " Best Sellers"
    encoded_query = quote(query)
    url = f"/search-v2?q={encoded_query}&country={region}&language=en&page=1&limit={limit}&sort_by=BEST_MATCH&product_condition=ANY&return_filters=true"
    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    
    json_data = json.loads(data.decode("utf-8"))

    

    # Extract specific elements from JSON
    if "data" in json_data and "products" in json_data["data"]:
        products = json_data["data"]["products"]
        extracted_data = ShoppingProductList(
            items = [
            shoppingProductInfo( 
                product_name=product.get("product_title"),
                product_image_url=product.get("product_photos") and product["product_photos"][0] if product.get("product_photos") else None,
                product_rating=product.get("product_rating"),
                product_ratings_count=product.get("product_num_reviews"),
                product_price=product.get("offer") and product["offer"]["price"] if product.get("offer") else None,
                product_url = product.get("offer") and product["offer"]["offer_page_url"] if product.get("offer") else None,
                seller_name=product.get("offer") and product["offer"]["store_name"] if product.get("offer") else None
            )
            for product in products
            ]
        )
        
        return extracted_data
    
    return json_data

    

if __name__ == "__main__":
    print(type(shoppingDatafromWeb("Dior Dress", 1, 'in')))
    
