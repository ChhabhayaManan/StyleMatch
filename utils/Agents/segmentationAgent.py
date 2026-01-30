import torch
import numpy as np
from PIL import Image
from Project.StyleMatch.utils.models.samLoader import Processor, model
from Project.StyleMatch.utils.Templates.schemas import ImageState


class SegmentationAgent:
    def __init__(self):
        pass
    
    def segment_image(self, imageState: ImageState, prompt: str) -> dict:
        img = imageState.img

        
        
        
        #converting the final img into Image.image formate if it's in np.ndarray
        if type(img) == np.ndarray:
            f_Img = Image.fromarray(img)
        else:
            f_Img = img

        #inference states for processing the img
        inf_state = Processor.set_image(f_Img)
        inf_state1 = Processor.set_text_prompt(prompt=prompt ,state=inf_state)


        img_boxes = inf_state1['boxes']
        if len(img_boxes) == 0:
            return {**ImageState , "error" : ["No objects detected in the image"]}

        imgWithMask = draw_boxes_on_image(f_Img, img_boxes)
        cropped_imgs = getCroppedImgs(f_Img, img_boxes)
        
        
        return {**imageState,
                "boxes" : img_boxes,
                "segmented_imgs" : cropped_imgs,
                "img" : imgWithMask,
                "error" : None
                }
        

def draw_boxes_on_image(image, boxes):
    """
    Draws a rectangle on a given PIL image using the provided box coordinates in xywh format.
    :param image: PIL.Image - The image on which to draw the rectangle.
    :param box: tuple - A tuple (x, y, w, h) representing the top-left corner, width, and height of the rectangle.
    :param color: tuple - A tuple (R, G, B) representing the color of the rectangle. Default is red.
    :return: PIL.Image - The image with the rectangle drawn on it.
    """
    # Ensure the image is in RGB mode
    try:
        image = image.convert("RGB")
    except Exception as e:
        print("Img conversion failed")
        return image
    
    color=(0, 255, 0)
    width, height = image.size
    # Unpack the box coordinates and draw a line on all of them
    for box in boxes:
        x1, y1, x2, y2 = box
        x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))
        x1 = max(0, min(x1, width - 1))
        y1 = max(0, min(y1, height - 1))
        x2 = max(0, min(x2, width - 1))
        y2 = max(0, min(y2, height - 1))

        # Get the pixel data
        pixels = image.load()
        # Draw the top and bottom edges
        for i in range(x1, x2 + 1):
            pixels[i, y1] = color
            pixels[i, y2] = color

        for j in range(y1, y2 + 1):
            pixels[x1, j] = color
            pixels[x2, j] = color

    return image

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