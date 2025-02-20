import os
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import time


load_dotenv()
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")


client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_KEY))

def extract_text_from_image(image_url):
    """Usa Azure OCR para extraer texto de un ticket desde una URL con mejor procesamiento."""
    result = client.read(url=image_url, raw=True)
    operation_id = result.headers["Operation-Location"].split("/")[-1]

    while True:
        read_result = client.get_read_result(operation_id)
        if read_result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)  

    if read_result.status == "succeeded":
        text_lines = []
        for result in read_result.analyze_result.read_results:
            for line in result.lines:
                text_lines.append(line.text)
        
 
        return "\n".join(text_lines)

    return None  
