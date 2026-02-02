import html
from typing import List, Optional, Dict
from utils.Templates.schemas import shoppingProductInfo, ShoppingProductList, ImageState, ProductInfo


class htmlblockGeneratorNode:
    def __init__(self):
        pass

    def run(self, image_state: ImageState):
        html_list = [
            self.getBlock(item)
            for item in image_state.productShoppingInfos.items
        ]
        return {
            "html_shopping": html_list
        }
    
    def getBlock(self, item: shoppingProductInfo) -> str:
        """Generate an HTML block for a shopping product item."""
        return f"""<div class="product-card">
        <a href="{item.product_url}" target="_blank">
            <div class="product-box">

            <div class="product-image">
                <img src="{item.product_image_url or 'https://via.placeholder.com/150'}" alt="{html.escape(item.product_name)}">
            </div>

            <div class="product-content">
                <div class="product-title">{item.product_name}</div>

                <div class="product-rating">
                <span class="product-stars">★{item.product_rating}</span>
                <span>({item.product_ratings_count})</span>
                </div>

                <div class="product-footer">
                <img class="product-seller" src="{item.seller_logo_url or 'https://via.placeholder.com/100x24?text=No+Logo'}" alt="{html.escape(item.seller_name or 'Unknown Seller')}">
                <div class="product-price">{item.product_price}</div>
                </div>
            </div>

            </div>
        </a>
        </div>
        """

