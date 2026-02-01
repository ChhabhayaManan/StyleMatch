#get the model
# 1. as we know that we need oto go one by one to all of the segments 
# and we'll ig take that enarest itesms as parameters and here generate a confirsed information the product
# and store that information into a state and. 

#code the main file connecting our first workflow. and test it for some testcase.
#see if it works fine.

import json
from utils.models.geminiModel import GeminiClient
from utils.models.clipModel import clip_model
from utils.Templates.schemas import ProductInfo, ImageState
from utils.Templates.promptTemplate import prompt_template
from PIL import Image



class ProductRecognizerAgent:
    def __init__(self):
        self.gemini_client = GeminiClient
        
    def run(self, ImageState: ImageState) -> ImageState:
        identified_products = []
        segmentated_imgs = ImageState.segmented_imgs
        nearest_items = ImageState.nearest_items

        

        print("Performing product recognition...")
        for idx, img in enumerate(segmentated_imgs):
            print(
                f"[Gemini] starting segment {idx+1}/{len(segmentated_imgs)}",
                flush=True
            )
            nearest_items_segment = nearest_items.get(f'segment_{idx}', [])
            prompt = prompt_template(
                nearest_items=nearest_items_segment,
                img=img
            )
            try:
                response = self.gemini_client.models.generate_content(
                    model="models/gemini-3-flash-preview",
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_json_schema": ProductInfo.model_json_schema(),
                    }
                )
            except Exception as e:
                err = ImageState.errors
                err.append(f"Gemini API error for segment {idx+1}: {str(e)}")
                print(f"[Gemini] error in segment {idx+1}: {str(e)}", flush=True)
                return {
                    "errors": err,
                    "products": identified_products
                }
                                                                        

            print(
                f"[Gemini] finished segment {idx+1}",
                flush=True
            )
            raw_text = response.candidates[0].content.parts[0].text
            data = json.loads(raw_text)
            productInfoTemp = ProductInfo.model_validate(data)
            identified_products.append(productInfoTemp)

        print("Product recognition completed.")
        return {
            "products": identified_products
        }
    


