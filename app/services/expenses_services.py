import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # Guarda tu API Key en .env


CLAUDE_API_URL = ""

def parse_ticket_text_with_claude(text):
    """Usa Claude 3 Sonnet para extraer productos del ticket y devolver JSON."""

    prompt = f"""
    Extrae los productos de este ticket y devuélvelos en formato JSON con las claves: 'cantidad', 'producto' y 'precio'.

    Ticket:
    {text}

    Responde únicamente con un JSON, sin texto adicional, con este formato:
    [
        {{"cantidad": 1.0, "producto": "Hierbas medicinales suquia variedad", "precio": 499.00}},
        {{"cantidad": 1.0, "producto": "Crema UAT LS Culinaria TetraTop330ml", "precio": 1113.75}},
        {{"cantidad": 1.0, "producto": "Portobellos PORTO", "precio": 1499.00}},
        {{"cantidad": 0.194, "producto": "Queso reggianito C&Co x kilo", "precio": 1163.81}}
    ]
    """

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 1024, 
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(CLAUDE_API_URL, headers=headers, json=data)
        response.raise_for_status()  
        result = response.json()

        generated_text = result["content"][0]["text"].strip()
      
        return json.loads(generated_text)

    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP en la API de Claude: {http_err}")
        print("Respuesta completa de la API:", response.text)  
        return None
    except Exception as e:
        print(f"Error general al procesar el ticket con Claude 3: {e}")
        return None
