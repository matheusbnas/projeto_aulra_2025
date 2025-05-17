import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODELO = "gemini-2.0-flash-lite"


def perguntar_gemini(pergunta, contexto=None):
    client = genai.GenerativeModel(MODELO)
    prompt = pergunta
    if contexto:
        prompt = f"{contexto}\n\nPergunta: {pergunta}"
    resposta = client.generate_content(prompt)
    return resposta.text.strip()
