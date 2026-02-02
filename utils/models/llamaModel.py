from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv()
googleModel = None

try :
    print("Loading Llama-3 model...")
    googleModel = ChatGoogleGenerativeAI(model='gemini-3.5-pro', api_key=os.getenv("GOOGLE_API_KEY2")) 
    print("Llama-3 model loaded successfully.")
except Exception as e:
    print(f"Error loading Llama-3 model: {e}")