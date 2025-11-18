import google.generativeai as genai

API_KEY = "AIzaSyDEpsitZNnt9mFJyLbtB7irS_yo1530Bu0"

genai.configure(api_key=API_KEY)

def generar_blog(prompt: str):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        real_prompt = (
            f"Genera un artículo de blog basado en este prompt. "
            f"Devuélvelo en formato JSON con: id, title, description, datecreation, imageurl. "
            f"En 'imageurl' crea una imagen usando https://image.pollinations.ai/ "
            f"y devuelve solo la URL. Prompt original: {prompt}"
        )
        response = model.generate_content(real_prompt)
        return response.text
    except Exception as e:
        return f"Error al generar IA -> {e}"
    
