import os
from utils.Templates.schemas import ImageState, ShoppingProductList, shoppingProductInfo, ProductInfo
from utils.tools.sellerLogoUrl import sellerLogoUrl
from utils.tools.webScraper import shoppingDatafromWeb



class shoppingInfoAgent:
    def __init__(self, limit: int = 5, region: str = 'in'):
        self.limit = limit
        self.region = region

    def run(self, image_state: ImageState):
        all_product_infos = image_state.products
        all_products_shopping_lists = []
        print("Fetching shopping information...")

        for ind, product in enumerate(all_product_infos):
            print(f"Searching for shopping info for product: {ind} / {len(all_product_infos)}")
            search_query = product.productDisplayName + " " + product.Brand if product.Brand else " " + product.Color
            shopping_data = shoppingDatafromWeb(search_query, self.limit, self.region)
            for item in shopping_data.items:
                if item.seller_name and not item.seller_logo_url:
                    item.seller_logo_url = sellerLogoUrl(item.product_url)
                all_products_shopping_lists.append(item)

        print("Shopping information fetching completed.")
        shoppingList = ShoppingProductList(items=all_products_shopping_lists)

        return {
            "productShoppingInfos": shoppingList
        }
    
if __name__ == "__main__":
    agent = shoppingInfoAgent(limit=3, region='in')
    dummy_image_state = ImageState(
        products=[
            ProductInfo(
                productDisplayName="Nike Air Max 270",
                Brand="Nike",
                Color="Black",
                gender="Unisex",
                masterCategory="Footwear",
                subCategory="Shoes",
                usage="Casual"
            ),
            ProductInfo(
                productDisplayName="Adidas Ultraboost 21",
                Brand="Adidas",
                Color="White",
                gender="Unisex",
                masterCategory="Footwear",
                subCategory="Shoes",
                usage="Sports"
            )
        ]
    )
    result = agent.run(dummy_image_state)
    for item in result["productShoppingInfos"].items:
        print(item)
    

        
        

        
