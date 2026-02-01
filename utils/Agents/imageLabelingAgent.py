from turtle import heading
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
from utils.Templates.schemas import ImageState
import random

def random_rgb_color():
    """Generates a random RGB color tuple normalized to 0-1 range."""
    return (random.random(), random.random(), random.random())


class imageLabelingAgent:
    def __init__(self):
        pass
    def run(self, imageState: ImageState) -> dict:
        img = imageState.img
        img_width, img_height = img.size
        draw = ImageDraw.Draw(img)
        font_size = max(12, img_height // 40)   # tweak divisor as needed
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)

        for i in range(len(imageState.products)):
            box = imageState.boxes[i]
    
            label = imageState.products[i].productDisplayName

            x1, y1, x2, y2 = box
            color = tuple(int(c * 255) for c in random_rgb_color())
            line_width = max(2, img_height // 200)
            draw.rectangle([x1, y1, x2, y2], outline=color, width=line_width)

            bbox = draw.textbbox((0, 0), label, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            pad = max(2, img_height // 300)

            draw.rectangle(
                [x1, y1 - text_h - 2 * pad, x1 + text_w + 2 * pad, y1],
                fill=color
            )

            draw.text(
                (x1 + pad, y1 - text_h - pad),
                label,
                fill=(255, 255, 255),
                font=font
            )
        

        return {
            'img' : img
        }



# def plot_bbox(
#     img_height,
#     img_width,
#     box,
#     box_format="XYXY",
#     relative_coords=True,
#     color="r",
#     linestyle="solid",
#     text=None,
#     ax=None,
# ):
#     if box_format == "XYXY":
#         x, y, x2, y2 = box
#         w = x2 - x
#         h = y2 - y
#     elif box_format == "XYWH":
#         x, y, w, h = box
#     elif box_format == "CxCyWH":
#         cx, cy, w, h = box
#         x = cx - w / 2
#         y = cy - h / 2
#     else:
#         raise RuntimeError(f"Invalid box_format {box_format}")

#     if relative_coords:
#         x *= img_width
#         w *= img_width
#         y *= img_height
#         h *= img_height

#     if ax is None:
#         ax = plt.gca()
#     rect = patches.Rectangle(
#         (x, y),
#         w,
#         h,
#         linewidth=1.5,
#         edgecolor=color,
#         facecolor="none",
#         linestyle=linestyle,
#     )
#     ax.add_patch(rect)
#     if text is not None:
#         facecolor = "w"
#         ax.text(
#             x,
#             y - 5,
#             text,
#             color=color,
#             weight="bold",
#             fontsize=8,
#             bbox={"facecolor": facecolor, "pad": 2},
#         )