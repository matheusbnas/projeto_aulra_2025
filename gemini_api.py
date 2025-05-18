import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Permite configurar a chave Gemini em tempo de execução


def configurar_gemini_api_key(api_key=None):
    if api_key:
        genai.configure(api_key=api_key)
    else:
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Inicializa com a chave do .env por padrão
configurar_gemini_api_key()

MODELO = "gemini-2.0-flash-lite"

# Função principal para geração de texto


def perguntar_gemini(pergunta, contexto=None):
    client = genai.GenerativeModel(MODELO)
    prompt = pergunta
    if contexto:
        prompt = f"{contexto}\n\nPergunta: {pergunta}"
    resposta = client.generate_content(prompt)
    return resposta.text.strip()
