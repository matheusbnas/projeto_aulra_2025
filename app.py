import streamlit as st
from scraper import get_carreiras, get_detalhes_carreira
from gemini_api import perguntar_gemini, MODELO, configurar_gemini_api_key
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from google.auth.transport.requests import Request
from datetime import datetime, timedelta
import re
from google.oauth2 import service_account
import json
from googleapiclient.errors import HttpError

# Cria o arquivo credentials.json a partir da variável de ambiente GOOGLE_CREDENTIALS_JSON, se existir
if os.getenv('GOOGLE_CREDENTIALS_JSON'):
    with open('credentials.json', 'w') as f:
        f.write(os.getenv('GOOGLE_CREDENTIALS_JSON'))

st.set_page_config(page_title="Chatbot de Carreiras TechGuide", layout="wide")
st.title("🤖 Chatbot de Carreiras TechGuide")

st.markdown("""
Este chatbot responde dúvidas sobre perfis profissionais e habilidades necessárias para atuar em áreas de tecnologia, com base no [TechGuide.sh](https://techguide.sh/).

Fonte dos dados: [https://techguide.sh/](https://techguide.sh/)
""")


@st.cache_data(show_spinner=True)
def carregar_carreiras():
    return get_carreiras()


carreiras = carregar_carreiras()
carreira_nomes = [c['nome'] for c in carreiras]

# Estado da carreira selecionada
if 'carreira_selecionada' not in st.session_state:
    st.session_state.carreira_selecionada = carreira_nomes[0]

# Sidebar: opção de chave Gemini
st.sidebar.markdown("🤖 Chatbot de Carreiras TechGuide")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Modelo Gemini em uso:** `{MODELO}`")
user_api_key = st.sidebar.text_input(
    "Chave Gemini API (opcional, sobrescreve a do .env)", type="password")
if user_api_key:
    configurar_gemini_api_key(user_api_key)
    st.sidebar.success("Usando chave Gemini fornecida pelo usuário.")
else:
    st.sidebar.info("Usando chave Gemini do .env.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Fontes e Portfólio:**")
st.sidebar.markdown(
    "- Matheus Bernardes - [Portfólio](https://portfolio-matheusbernardes.netlify.app/)")
st.sidebar.markdown("- Matech - [Site da empresa](https://matechai.com/)")
st.sidebar.markdown("---")

# Selectbox no sidebar para seleção de carreira
carreira_sidebar = st.sidebar.selectbox(
    "Selecione a carreira de interesse:", carreira_nomes, index=carreira_nomes.index(st.session_state.carreira_selecionada))
if carreira_sidebar != st.session_state.carreira_selecionada:
    st.session_state.carreira_selecionada = carreira_sidebar
    st.session_state.resposta_automatica = None  # Limpa resposta anterior

# Mostrar cards não clicáveis, apenas visual, destacando o selecionado
cards_por_linha = 4
linhas = [carreira_nomes[i:i+cards_por_linha]
          for i in range(0, len(carreira_nomes), cards_por_linha)]
for linha in linhas:
    cols = st.columns(len(linha))
    for idx, nome in enumerate(linha):
        is_selected = (nome == st.session_state.carreira_selecionada)
        card_color = "#00e6e6" if is_selected else "#222"
        text_color = "#222" if is_selected else "#fff"
        border = "4px solid #00b8b8" if is_selected else "2px solid #444"
        shadow = "0 0 12px #00e6e6" if is_selected else "none"
        style = f"background-color: {card_color}; color: {text_color}; border-radius: 12px; border: {border}; font-weight: bold; height: 60px; width: 100%; margin-bottom: 8px; box-shadow: {shadow}; display:flex;align-items:center;justify-content:center; transition: box-shadow 0.2s;"
        cols[idx].markdown(
            f"<div style='{style}'>{nome}</div>", unsafe_allow_html=True)

carreira_selecionada = st.session_state.carreira_selecionada
carreira_url = next(
    (c['url'] for c in carreiras if c['nome'] == carreira_selecionada), None)

detalhes = []
if carreira_url:
    detalhes = get_detalhes_carreira(carreira_url)

# Sidebar formatado
st.sidebar.markdown(f"### {carreira_selecionada}")
if carreira_url:
    st.sidebar.markdown(
        f"[Ver guia completo]({carreira_url})", unsafe_allow_html=True)
st.sidebar.markdown("---")
for d in detalhes:
    if d['tipo'] == 'titulo':
        st.sidebar.markdown(f"**{d['conteudo']}**")
    elif d['tipo'] == 'lista':
        st.sidebar.markdown("<ul style='margin-top:0;margin-bottom:0'>" + ''.join(
            [f"<li>{item}</li>" for item in d['conteudo']]) + "</ul>", unsafe_allow_html=True)

# Geração automática da resposta sobre a carreira selecionada
if 'resposta_automatica' not in st.session_state or st.session_state.resposta_automatica is None:
    with st.spinner(f"Gerando resumo sobre a carreira '{carreira_selecionada}'..."):
        contexto = "\n".join([
            d['conteudo'] if d['tipo'] == 'titulo' else ", ".join(d['conteudo']) for d in detalhes
        ])
        prompt = f"Você é um especialista em carreiras de tecnologia. Responda tudo sobre a área '{carreira_selecionada}' com base nas informações abaixo extraídas do site TechGuide.sh. Seja detalhado e cite as habilidades, tópicos, níveis e recomendações relevantes.\n\n{contexto}"
        st.session_state.resposta_automatica = perguntar_gemini(prompt)

st.markdown(f"### Resumo da carreira selecionada: {carreira_selecionada}")
st.markdown(st.session_state.resposta_automatica)

# Chatbot sempre visível
st.subheader(
    "Pergunte ao bot sobre a carreira, ou use comandos especiais com @ para Google Agenda, Keep, etc:")
st.info("Exemplo: @agenda criar evento para reunião amanhã às 10h. | @keep criar anotação sobre carreira de dados.")
pergunta = st.text_input("Digite sua pergunta ou comando:")

# Escopos necessários
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/spreadsheets']

# Função para extrair dados do comando @agenda (simples, pode ser melhorada)


def extrair_evento_agenda(comando):
    # Exemplo: @agenda criar evento para reunião amanhã às 10h
    # Extrai título e data/hora simples
    match = re.search(
        r'evento para (.+) (amanhã|hoje|[0-9]{1,2}/[0-9]{1,2}|segunda|terça|quarta|quinta|sexta|sábado|domingo)? ?(às|as)? ?([0-9]{1,2}h)?', comando, re.I)
    titulo = "Evento do Chatbot"
    data_inicio = None
    data_fim = None
    if match:
        titulo = match.group(1).strip().capitalize()
        hora = match.group(4)
        if match.group(2):
            dia = match.group(2).lower()
            if dia == 'amanhã':
                data = datetime.now() + timedelta(days=1)
            elif dia == 'hoje':
                data = datetime.now()
            else:
                data = datetime.now()  # fallback
        else:
            data = datetime.now()
        if hora:
            hora_num = int(hora.replace('h', ''))
            data = data.replace(hour=hora_num, minute=0,
                                second=0, microsecond=0)
        data_inicio = data.isoformat()
        data_fim = (data + timedelta(hours=1)).isoformat()
    return titulo, data_inicio, data_fim

# Função para autenticação OAuth web


@st.cache_resource(show_spinner=True)
def get_calendar_flow():
    SERVICE_ACCOUNT_FILE_PATH = os.environ.get('SERVICE_ACCOUNT_FILE_PATH')
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE_PATH,
        scopes=SCOPES
    )
    return build('calendar', 'v3', credentials=creds)


def criar_evento_google_agenda(titulo, data_inicio, data_fim, code=None):
    calendar_service = get_calendar_flow()
    if not calendar_service:
        return {
            "status": "error",
            "error_message": "Serviço do Google Calendar não configurado."
        }
    if code:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        flow.fetch_token(code=code)
        creds = flow.credentials
        service = build('calendar', 'v3', credentials=creds)
        evento = {
            'summary': titulo,
            'start': {'dateTime': data_inicio, 'timeZone': 'America/Sao_Paulo'},
            'end': {'dateTime': data_fim, 'timeZone': 'America/Sao_Paulo'},
        }
        try:
            evento = service.events().insert(calendarId='primary', body=evento).execute()
            return evento.get('htmlLink')
        except HttpError as e:
            error_details = json.loads(e.content).get('error', {})
            reason = error_details.get('errors', [{}])[0].get('reason')
            message = error_details.get('message')

            if e.resp.status == 403 and reason == 'forbiddenForServiceAccounts':
                error_msg = (
                    "Erro: Falha ao criar evento. A conta de serviço pode não ter permissão "
                    f"para adicionar convidados ('{email_convidado}') ou enviar notificações. "
                    "Tente criar o evento sem um email de convidado, ou verifique as configurações de delegação de domínio do Google Workspace."
                )
                return {
                    "status": "error",
                    "error_message": error_msg
                }
    else:
        auth_url, _ = flow.authorization_url(prompt='consent')
        return auth_url


if pergunta:
    contexto = "\n".join([
        d['conteudo'] if d['tipo'] == 'titulo' else ", ".join(d['conteudo']) for d in detalhes
    ])
    # Detecta comandos especiais com @
    if pergunta.strip().startswith("@agenda"):
        st.markdown(f"**Comando detectado:** {pergunta}")
        # Extrai dados do evento
        titulo, data_inicio, data_fim = extrair_evento_agenda(pergunta)
        # Passo 1: Se não há code, gera link de autorização
        code = st.text_input(
            "Cole aqui o código de autorização do Google (após clicar no link abaixo):", key="code_input")
        if not code:
            auth_url = criar_evento_google_agenda(
                titulo, data_inicio, data_fim, code=None)
            st.markdown(
                f"[Clique aqui para autorizar o Google Agenda]({auth_url})")
            st.info("Após autorizar, copie o código do Google e cole acima.")
        else:
            try:
                link_evento = criar_evento_google_agenda(
                    titulo, data_inicio, data_fim, code=code)
                st.success(
                    f"Evento criado com sucesso! [Ver no Google Agenda]({link_evento})")
            except Exception as e:
                st.error(f"Erro ao criar evento: {e}")
    elif pergunta.strip().startswith("@keep"):
        st.warning(
            "Integração com Google Keep: (futuro) Aqui o sistema criaria uma anotação no Keep usando a API do Google.")
        st.markdown(f"**Comando detectado:** {pergunta}")
    else:
        prompt = f"Você é um especialista em carreiras de tecnologia. Responda tudo sobre a área '{carreira_selecionada}' com base nas informações abaixo extraídas do site TechGuide.sh.\n\n{contexto}\n\nPergunta do usuário: {pergunta}"
        resposta = perguntar_gemini(prompt)
        st.markdown(f"**Resposta:** {resposta}")
