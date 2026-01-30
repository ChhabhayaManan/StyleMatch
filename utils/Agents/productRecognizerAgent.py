#get the model
# 1. as we know that we need oto go one by one to all of the segments 
# and we'll ig take that enarest itesms as parameters and here generate a confirsed information the product
# and store that information into a state and. 

#code the main file connecting our first workflow. and test it for some testcase.
#see if it works fine.

from utils.models.geminiModel import GeminiClient
from utils.models.clipModel import clip_model
from utils.template.schemas import ProductInfo, ImageState
from utils.template.promptTemplate import prompt_template
from PIL import Image



class ProductRecognizerAgent:
    def __init__(self):
        self.gemini_client = GeminiClient
        
    def recognize_product(self, ImageState: ImageState, nearest_items: dict) -> ImageState:
        identified_products = []
        segmentated_imgs = ImageState.segmented_imgs

        for idx, img in enumerate(segmentated_imgs):
            segment_nearest_items = nearest_items.get(f'segment_{idx}', [])
            prompt = prompt_template(segment_nearest_items, img)
            response = self.gemini_client.model.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": ProductInfo.model_json_schema(),
                }
            )
            productInfoTemp = ProductInfo.model_validate(response.candidates[0].content.parts[0].text)
            identified_products.append(productInfoTemp)
        
        return {
            **ImageState,
            "identified_products": identified_products
        }
    
    