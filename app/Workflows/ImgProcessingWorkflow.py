import time
from pathlib import Path
from typing import Any, Dict, Iterator, List

import numpy as np
from PIL import Image
from langgraph.graph import END, START, StateGraph

from utils.Agents.htmlblockGeneratorNode import htmlblockGeneratorNode
from utils.Agents.imageLabelingAgent import imageLabelingAgent
from utils.Agents.infoRetrievalAgent import InfoRetrievalAgent
from utils.Agents.productRecognizerAgent import ProductRecognizerAgent
from utils.Agents.segmentationAgent import SegmentationAgent
from utils.Agents.shoppingInfoAgent import shoppingInfoAgent
from utils.Agents.stopWorkflow import StopWorkflowAgent
from utils.Templates.schemas import ImageState

start = time.perf_counter()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
INDEX_PATH = DATA_DIR / "fashion_product_images.index"
METADATA_PATH = DATA_DIR / "fashion_product_info.json"

WORKFLOW_ACTIVITY_STEPS = (
    {
        "id": "Segmentation",
        "title": "Segmenter",
        "description": "Detects the clothing regions that match your prompt.",
    },
    {
        "id": "InfoRetrieval",
        "title": "Catalog Search",
        "description": "Pulls nearby fashion matches from the vector index.",
    },
    {
        "id": "ProductRecognition",
        "title": "Recognizer",
        "description": "Names each detected piece and fills the product fields.",
    },
    {
        "id": "ImageLabeling",
        "title": "Labeler",
        "description": "Draws the annotations on top of the uploaded image.",
    },
    {
        "id": "ShoppingInfo",
        "title": "Shopping Scout",
        "description": "Fetches shopping results, prices, sellers, and ratings.",
    },
    {
        "id": "HTMLBlockGenerator",
        "title": "Card Builder",
        "description": "Builds the product gallery that Gradio renders below.",
    },
)

_VISIBLE_STEP_IDS = [step["id"] for step in WORKFLOW_ACTIVITY_STEPS]


def _normalize_image(uploaded_img: Image.Image | np.ndarray) -> Image.Image:
    if isinstance(uploaded_img, np.ndarray):
        return Image.fromarray(uploaded_img)
    return uploaded_img


def _build_workflow(limit: int, region: str):
    graph = StateGraph(ImageState)

    print("Initializing agents...")
    segmentation_agent = SegmentationAgent()
    info_retrieval_agent = InfoRetrievalAgent(
        index_path=str(INDEX_PATH),
        metadata_path=str(METADATA_PATH),
    )
    product_recognizer_agent = ProductRecognizerAgent()
    image_label_agent = imageLabelingAgent()
    shopping_info_agent = shoppingInfoAgent(limit=limit, region=region)
    html_block_generator = htmlblockGeneratorNode()
    stop_workflow_agent = StopWorkflowAgent()

    print("Building workflow graph...")
    graph.set_entry_point("Segmentation")
    graph.add_node("Segmentation", segmentation_agent.run)
    graph.add_node("InfoRetrieval", info_retrieval_agent.run)
    graph.add_node("ProductRecognition", product_recognizer_agent.run)
    graph.add_node("ImageLabeling", image_label_agent.run)
    graph.add_node("ShoppingInfo", shopping_info_agent.run)
    graph.add_node("HTMLBlockGenerator", html_block_generator.run)
    graph.add_node("StopWorkflow", stop_workflow_agent.run)

    print("Connecting workflow nodes...")
    graph.add_edge(START, "Segmentation")
    graph.add_edge("Segmentation", "InfoRetrieval")
    graph.add_edge("InfoRetrieval", "ProductRecognition")
    graph.add_edge("ProductRecognition", "ImageLabeling")
    graph.add_edge("ImageLabeling", "ShoppingInfo")
    graph.add_edge("ShoppingInfo", "HTMLBlockGenerator")
    graph.add_edge("HTMLBlockGenerator", "StopWorkflow")
    graph.add_edge("StopWorkflow", END)

    print("Compiling workflow graph...")
    return graph.compile()


def _merge_state(state: Dict[str, Any], update: Dict[str, Any] | None) -> Dict[str, Any]:
    if update:
        state.update(update)
    return state


def _result_from_state(state: Dict[str, Any]):
    return (
        state.get("html_shopping", ""),
        state.get("img"),
        state.get("products", []),
        state.get("errors", []),
    )


def stream_img_processing(
    uploadedImg: Image.Image | np.ndarray,
    Prompt: str = "Fashion",
    Limit: int = 5,
    Region: str = "in",
) -> Iterator[Dict[str, Any]]:
    uploaded_img = _normalize_image(uploadedImg)
    compiled = _build_workflow(limit=Limit, region=Region)
    initial_state = ImageState(img=uploaded_img, prompt=Prompt)
    merged_state = initial_state.model_dump()
    completed_nodes: List[str] = []

    yield {
        "event": "start",
        "active_node": _VISIBLE_STEP_IDS[0] if _VISIBLE_STEP_IDS else None,
        "completed_nodes": [],
        "state": dict(merged_state),
    }

    for node_event in compiled.stream(initial_state, stream_mode="updates"):
        if not node_event:
            continue

        node_name, node_update = next(iter(node_event.items()))
        _merge_state(merged_state, node_update)

        if node_name in _VISIBLE_STEP_IDS and node_name not in completed_nodes:
            completed_nodes.append(node_name)
            next_index = len(completed_nodes)
            next_active = _VISIBLE_STEP_IDS[next_index] if next_index < len(_VISIBLE_STEP_IDS) else None
            yield {
                "event": "progress",
                "active_node": next_active,
                "completed_nodes": completed_nodes.copy(),
                "state": dict(merged_state),
            }

    yield {
        "event": "done",
        "active_node": None,
        "completed_nodes": completed_nodes.copy(),
        "state": dict(merged_state),
    }


def ImgProcessing(
    uploadedImg: Image.Image | np.ndarray,
    Prompt: str = "Fashion",
    Limit: int = 5,
    Region: str = "in",
):
    final_update = None
    for workflow_update in stream_img_processing(
        uploadedImg=uploadedImg,
        Prompt=Prompt,
        Limit=Limit,
        Region=Region,
    ):
        final_update = workflow_update

    if final_update is None:
        raise RuntimeError("StyleMatch workflow did not return a final state.")

    return _result_from_state(final_update["state"])


if __name__ == "__main__":
    test_img_path = PROJECT_ROOT / "data" / "77909915.webp"
    test_img = Image.open(test_img_path)
    ImgProcessing(test_img, "Skirt")
    end = time.perf_counter()
    print(f"Total processing time: {end - start:.4f} seconds")
