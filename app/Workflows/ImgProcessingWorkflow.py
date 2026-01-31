from langgraph.graph import START, END, StateGraph
import sys
import os
from utils.Templates.schemas import ImageState, ProductInfo
from utils.Agents.stopWorkflow1 import StopWorkflowAgent
from utils.Agents.segmentationAgent import SegmentationAgent
from utils.Agents.infoRetrievalAgent import InfoRetrievalAgent
from utils.Agents.productRecognizerAgent import ProductRecognizerAgent
from PIL import Image

def ImgProcessing(uploadedImg: Image.Image, Prompt: str = "Fashion"):
    
    graph = StateGraph(ImageState)
    
    index_path = "G:\Coding\GenAi\Pro\StyleMatch\data\fashion_product_images.index"
    json_path = "G:\Coding\GenAi\Pro\StyleMatch\data\fashion_product_info.json"
    print(index_path)

    segmentationAgent = SegmentationAgent()
    stopWorkflowAgent = StopWorkflowAgent()
    productRecognizerAgent = ProductRecognizerAgent()
    infoRetrievalAgent = InfoRetrievalAgent(index_path=index_path, metadata_path=json_path)

    graph.set_entry_point("Segmentation")
    graph.add_node("Segmentation", segmentationAgent.run)
    graph.add_node("InfoRetrieval", infoRetrievalAgent.run)
    graph.add_node("ProductRecognition", productRecognizerAgent.run)
    graph.add_node("StopWorkflow", stopWorkflowAgent.run)

    graph.add_edge(START, "Segmentation")
    graph.add_edge("Segmentation", "InfoRetrieval")
    graph.add_edge("InfoRetrieval", "ProductRecognition")
    graph.add_edge("ProductRecognition", "StopWorkflow")
    graph.add_edge("StopWorkflow", END)

    compiled = graph.compile()
    print(compiled.get_graph().draw_mermaid())

    initial_state = ImageState(
        img=uploadedImg,
        prompt=Prompt
    )

    result = compiled.invoke(initial_state)

    print(result)


if __name__ == "__main__":
    test_img_path = os.path.join(os.getcwd(), "data/demo.webp")
    test_img = Image.open(test_img_path)
    ImgProcessing(test_img)