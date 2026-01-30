from google import genai
from dotenv import load_dotenv
load_dotenv()

print("Gemini model is loading......")
try:
    GeminiClient = genai.Client()
    print("Successfully Loaded")
except Exception as e:
    print("Model loading failed")
    print(e)

