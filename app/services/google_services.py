import os
import json
import urllib.parse
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)


def generar_blog(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        # Instrucciones + prompt de usuario en un solo texto
        real_prompt = (
            "Genera un artículo de blog basado en este prompt del usuario.\n\n"
            "DEVUELVE ÚNICAMENTE un JSON válido. NO incluyas texto adicional, "
            "NO uses markdown, NO pongas ```json.\n\n"
            "Formato EXACTO:\n"
            "{\n"
            "  \"id\": \"string\",\n"
            "  \"title\": \"string corta (que no supere los 100 caracteres)\",\n"
            "  \"description\": \"string corta (que no supere las 120 caracteres)\",\n"
            "  \"datecreation\": \"YYYY-MM-DD\",\n"
            "  \"imageurl\": \"string\"\n"
            "}\n\n"
            f"Prompt del usuario: {prompt}"
        )

        response = model.generate_content(real_prompt)

        raw = response.text.strip()
        print("IA RAW:", raw)

        # Intentar parsear JSON
        data = json.loads(raw)

        # Crear imagen Pollinations segura
        encoded = urllib.parse.quote(prompt.strip())
        data["imageurl"] = f"https://image.pollinations.ai/prompt/{encoded}"

        return data

    except Exception as e:
        raise Exception(f"Error al generar IA -> {e}")
