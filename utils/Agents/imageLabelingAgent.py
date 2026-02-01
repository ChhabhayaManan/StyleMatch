from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def random_rgb_color():
    """Generates a random RGB color tuple."""
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


class imageLabelingAgent:
    def __init__(self):
        pass
    def run(self, imageState: ImageState) -> dict:
        img = imageState.img
        img_width, img_height = img.size
        for i in range(len(imageState.boxes)):
            box = imageState.boxes[i]
    
            product_label = imageState.products[i]['productDisplayName']
            color = random_rgb_color()
            fig, ax = plt.subplots(1)
            plot_bbox(
                img_height,
                img_width,
                box,
                box_format="XYXY",
                relative_coords=False,
                color=color,
                linestyle="solid",
                text=product_label,
                ax=ax,
            )
        

        return {
            'img' : img
        }



def plot_bbox(
    img_height,
    img_width,
    box,
    box_format="XYXY",
    relative_coords=True,
    color="r",
    linestyle="solid",
    text=None,
    ax=None,
):
    if box_format == "XYXY":
        x, y, x2, y2 = box
        w = x2 - x
        h = y2 - y
    elif box_format == "XYWH":
        x, y, w, h = box
    elif box_format == "CxCyWH":
        cx, cy, w, h = box
        x = cx - w / 2
        y = cy - h / 2
    else:
        raise RuntimeError(f"Invalid box_format {box_format}")

    if relative_coords:
        x *= img_width
        w *= img_width
        y *= img_height
        h *= img_height

    if ax is None:
        ax = plt.gca()
    rect = patches.Rectangle(
        (x, y),
        w,
        h,
        linewidth=1.5,
        edgecolor=color,
        facecolor="none",
        linestyle=linestyle,
    )
    ax.add_patch(rect)
    if text is not None:
        facecolor = "w"
        ax.text(
            x,
            y - 5,
            text,
            color=color,
            weight="bold",
            fontsize=8,
            bbox={"facecolor": facecolor, "alpha": 0.75, "pad": 2},
        )