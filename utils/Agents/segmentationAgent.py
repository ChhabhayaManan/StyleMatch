import torch
import numpy as np
from PIL import Image
from utils.models.samLoader import model
from utils.Templates.schemas import ImageState
from sam3.model.sam3_image_processor import Sam3Processor

class SegmentationAgent:
    def __init__(self):
        pass
    
    def run(self, imageState: ImageState) -> dict:
        img = imageState.img
        prompt = imageState.prompt
        #converting the final img into Image.image formate if it's in np.ndarray
        if type(img) == np.ndarray:
            f_Img = Image.fromarray(img)
        else:
            f_Img = img

        if f_Img.mode != "RGB": #if the dimentions of img are more than 3 convert to RGB
            f_Img = f_Img.convert("RGB")
        print("Performing segmentation...")
        Processor = Sam3Processor(model, confidence_threshold=0.7)

        #inference states for processing the img
        inf_state = Processor.set_image(f_Img)
        inf_state1 = Processor.set_text_prompt(prompt=prompt ,state=inf_state)

        print("Segmentation completed.")
        img_boxes = inf_state1['boxes']
        boxes = (#because boxes are in tensor formate we need to convert them to list
            img_boxes
            .detach()
            .cpu()
            .round()
            .int()
            .tolist()
        )
        if len(boxes) == 0:
            errors = imageState.errors
            errors.append("No objects detected in the image")
            return {**imageState.model_dump() , "errors" : errors}

        cropped_imgs = getCroppedImgs(f_Img, boxes)
        

        return {**imageState.model_dump(),
                "boxes" : boxes,
                "segmented_imgs" : cropped_imgs,
                }
        


def getCroppedImgs(image, boxes):
    try:
        image = image.convert("RGB")
    except Exception as e:
        print("Img conversion failed")
        return image
    
    imgs = []

    if len(boxes) == 0:
        print("No object found!!")
        return imgs

    image_w, image_h = image.size

    for box in boxes:
        if torch.is_tensor(box):
            box = box.tolist()

        x1, y1, x2, y2 = map(int, box)

        # Clamp to image bounds (important)
        x1 = max(0, min(x1, image_w))
        x2 = max(0, min(x2, image_w))
        y1 = max(0, min(y1, image_h))
        y2 = max(0, min(y2, image_h))

        imgs.append(image.crop((x1, y1, x2, y2)))

    return imgs

    
if __name__ == "__main__":
    pass