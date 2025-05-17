import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

modelo = "gemini-2.0-flash-lite"
client = genai.GenerativeModel(modelo)
resposta = client.generate_content(
    "Quem é a empresa por trás dos modelos Gemini?")
print(resposta.text)
