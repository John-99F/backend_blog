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

        instrucciones = (
            "Genera un artículo de blog basado en el prompt del usuario.\n"
            "Devuelve EXCLUSIVAMENTE un JSON válido. Sin explicaciones, sin texto extra, "
            "sin backticks, sin markdown, sin ```json.\n\n"
            "Formato EXACTO:\n"
            "{\n"
            "  \"id\": \"string\",\n"
            "  \"title\": \"string\",\n"
            "  \"description\": \"string corta (máximo 2–3 líneas)\",\n"
            "  \"datecreation\": \"YYYY-MM-DD\",\n"
            "  \"imageurl\": \"string\"\n"
            "}\n\n"
            "IMPORTANTE:\n"
            "- No incluyas nada fuera del JSON.\n"
            "- 'imageurl' debe ser una URL válida generada con Pollinations.\n"
            "- Usa el prompt original para generar la imagen.\n"
        )

        response = model.generate_content([
            {"role": "system", "content": instrucciones},
            {"role": "user", "content": prompt}
        ])

        raw = response.text.strip()
        print("IA RAW:", raw)

        # Convertir respuesta a JSON
        data = json.loads(raw)

        # Crear URL segura de pollinations
        encoded_prompt = urllib.parse.quote(prompt)
        data["imageurl"] = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        return data

    except Exception as e:
        raise Exception(f"Error al generar IA -> {e}")
