import html
from typing import List, Optional, Dict
from utils.Templates.schemas import shoppingProductInfo, ShoppingProductList, ImageState, ProductInfo

class htmlblockGeneratorNode:
    # Embedded CSS with unique class names to ensure horizontal layout and styling
    _STYLES = """
    <style>
    /* 1. Container: Forces 3 Columns */
    .custom-gallery-container {
        display: grid;
        /* This forces exactly 3 columns of equal width */
        grid-template-columns: repeat(3, 1fr); 
        gap: 20px;       
        padding: 20px;
        width: 100%;
        box-sizing: border-box;
        border: 2px solid white;
        border-radius: 12px;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* 2. The Card: Horizontal Layout */
    .custom-product-card {
       background: rgba(255, 255, 255, 0.2); 
  
   3. Apply the backdrop blur effect 
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);  For Safari support 
  
  /* 4. Optional: Add a light border and shadow for depth */
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        display: flex;          
        flex-direction: row;
        overflow: hidden;
        text-decoration: none !important;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 140px; /* Fixed height ensures alignment */
    }

    .custom-product-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2) !important;
    }

    /* 3. Image Box */
    .custom-card-img-box {
        width: 120px;       /* Fixed width for image */
        flex-shrink: 0;     /* Prevents image from squishing */
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 8px;
        border-right: 1px solid #f0f0f0;
    }

    .custom-card-img {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }

    /* 4. Details Section */
    .custom-card-details {
        flex: 1;
        padding: 12px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-width: 0;
    }

    /* Typography */
    .custom-product-title {
        font-size: 15px;
        font-weight: 600;
        color: #F8EEEC !important;
        line-height: 1.3;
        margin-bottom: 4px;
        display: -webkit-box;
        -webkit-line-clamp: 2; /* Limits title to 2 lines */
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .custom-meta-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: auto; 
    }

    .custom-product-price {
        font-size: 18px;
        font-weight: 700;
        color: #8bca84 !important;
    }

    /* RATING FIX: High Contrast Colors */
    .custom-rating-badge {
        display: inline-flex;
        align-items: center;
        background-color: #f0f0f0; /* Slightly darker grey background */
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 12px;
        border: 1px solid #ddd;
        color: #000000 !important; /* Force TEXT BLACK */
        font-weight: 500;
    }

    .custom-stars {
        color: #ffc107; /* Gold stars */
        margin-right: 4px;
        font-size: 14px;
    }
    
    .custom-rating-count {
        color: #333 !important; /* Dark grey for count */
        margin-left: 4px;
        opacity: 0.8;
    }

    /* Seller Info */
    .custom-seller-row {
        display: flex;
        align-items: center;
        gap: 6px;
        padding-top: 8px;
        margin-top: 8px;
        border-top: 1px solid #f0f0f0;
        font-size: 11px;
        color: #fbfcf8 !important;
    }

    .custom-seller-logo {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        object-fit: cover;
        border: 1px solid #ddd;
    }

    /* RESPONSIVENESS: Important so it doesn't break on phones */
    @media (max-width: 1024px) {
        .custom-gallery-container {
            grid-template-columns: repeat(2, 1fr); /* 2 per row on tablets */
        }
    }

    @media (max-width: 600px) {
        .custom-gallery-container {
            grid-template-columns: 1fr; /* 1 per row on mobile */
        }
        .custom-product-card {
            height: auto; /* Let height grow on mobile */
        }
    }
</style>
    """

    def __init__(self):
        pass

    def run(self, image_state: ImageState):
        # 1. Generate HTML for all individual cards
        cards_html = "".join([
            self.getBlock(item)
            for item in image_state.productShoppingInfos.items
        ])

        # 2. Wrap them in the container and prepend styles
        # This is necessary for the flexbox/horizontal layout to work in Gradio
        final_html = f"{self._STYLES}<div class=\"custom-gallery-container\">{cards_html}</div>"

        return {
            "html_shopping": final_html
        }
    
    def getBlock(self, item: shoppingProductInfo) -> str:
        """Generate a styled HTML block for a shopping product item."""
        
        # Calculate stars visual
        try:
            rating_val = float(item.product_rating) if item.product_rating else 0.0
        except (ValueError, TypeError):
            rating_val = 0.0
            
        full_stars = int(rating_val)

        return f"""
       <a href="{item.product_url}" target="_blank" class="custom-product-card">
    
    <div class="custom-card-img-box">
        <img src="{item.product_image_url}" alt="{item.product_name}" class="custom-card-img" loading="lazy">
    </div>

    <div class="custom-card-details">
        
        <div class="custom-product-title">{item.product_name}</div>
        
        <div class="custom-meta-row">
            <div class="custom-product-price">{item.product_price}</div>
            
            <div class="custom-rating-badge">
                <span class="custom-stars">★</span> 
                <span style="color: #000;">{rating_val}</span>
                <span class="custom-rating-count">({item.product_ratings_count})</span>
            </div>
        </div>

        <div class="custom-seller-row">
            <img src="{item.seller_logo_url}" alt="Seller" class="custom-seller-logo">
            <span>{item.seller_name}</span>
        </div>
        
    </div>
</a>
        """



 