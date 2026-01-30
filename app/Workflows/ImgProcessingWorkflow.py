from langgraph.graph import START, END, StateGraph
from utils.Agents.segmentationAgent import SegmentationAgent
from utils.Templates.schemas import ImageState
from utils.Agents.stopWorkflow1 import StopWorkflowAgent
from utils.Agents.imageClassificationAgent import ImageClassificationAgent
from utils.Agents.productInfoExtractionAgent import ProductInfoExtractionAgent


def Img