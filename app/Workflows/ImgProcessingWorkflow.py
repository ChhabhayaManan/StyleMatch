import time
start = time.perf_counter()
from langgraph.graph import START, END, StateGraph
import sys
import os
from utils.Templates.schemas import ImageState, ProductInfo
from utils.Agents.stopWorkflow1 import StopWorkflowAgent
from utils.Agents.segmentationAgent import SegmentationAgent
from utils.Agents.infoRetrievalAgent import InfoRetrievalAgent
from utils.Agents.productRecognizerAgent import ProductRecognizerAgent
from utils.Agents.imageLabelingAgent import imageLabelingAgent
from utils.Agents.htmlblockGeneratorNode import htmlblockGeneratorNode
from utils.Agents.shoppingInfoAgent import shoppingInfoAgent
from PIL import Image
import numpy as np




def ImgProcessing(uploadedImg: Image.Image or np.ndarray, Prompt: str = "Fashion"):
    
    if isinstance(uploadedImg, np.ndarray):
        uploadedImg = Image.fromarray(uploadedImg)
    
    graph = StateGraph(ImageState)
    


    
    index_path = "/teamspace/studios/this_studio/StyleMatch/data/fashion_product_images.index"
    json_path = "/teamspace/studios/this_studio/StyleMatch/data/fashion_product_info.json"
    print(index_path)

    print("Initializing agents...")
    segmentationAgent = SegmentationAgent()
    stopWorkflowAgent = StopWorkflowAgent()
    productRecognizerAgent = ProductRecognizerAgent()
    infoRetrievalAgent = InfoRetrievalAgent(index_path=index_path, metadata_path=json_path)
    imgLabelAgent = imageLabelingAgent()
    shoppingInfoAgentNode = shoppingInfoAgent(limit=5, region='in')
    htmlBlockGeneratorNode = htmlblockGeneratorNode()


    print("Building workflow graph...")
    graph.set_entry_point("Segmentation")
    graph.add_node("Segmentation", segmentationAgent.run)
    graph.add_node("InfoRetrieval", infoRetrievalAgent.run)
    graph.add_node("ProductRecognition", productRecognizerAgent.run)
    graph.add_node("StopWorkflow", stopWorkflowAgent.run)
    graph.add_node("ImageLabeling", imgLabelAgent.run)
    graph.add_node("ShoppingInfo", shoppingInfoAgentNode.run)
    graph.add_node("HTMLBlockGenerator", htmlBlockGeneratorNode.run)

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
    compiled = graph.compile()
    print(compiled.get_graph().draw_mermaid())


    print("Running workflow...")
    initial_state = ImageState(
        img=uploadedImg,
        prompt=Prompt
    )

    result = compiled.invoke(initial_state)
    resultImg = result['img']
    resultImg.show()
    resultHTMLS = result['html_shopping']
    print("Generated HTML Blocks: ", resultHTMLS)
    save_path = os.path.join(os.getcwd(), "data/result.jpg")
    resultImg.save(save_path, "JPEG")

    return resultHTMLS, resultImg

if __name__ == "__main__":
    
    test_img_path = os.path.join(os.getcwd(), "data/77909915.webp")
    test_img = Image.open(test_img_path)
    ImgProcessing(test_img,"Skirt")
    end = time.perf_counter()
    print(f"Total processing time: {end - start:.4f} seconds")