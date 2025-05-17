import streamlit as st
from scraper import get_carreiras, get_detalhes_carreira, get_contexto_completo
from gemini_api import perguntar_gemini, MODELO

st.set_page_config(page_title="Chatbot de Carreiras TechGuide", layout="wide")
st.title("🤖 Chatbot de Carreiras TechGuide")

st.markdown("""
Este chatbot responde dúvidas sobre perfis profissionais e habilidades necessárias para atuar em áreas de tecnologia, com base no [TechGuide.sh](https://techguide.sh/).

Fonte dos dados: [https://techguide.sh/](https://techguide.sh/)
""")


@st.cache_data(show_spinner=True)
def carregar_carreiras():
    return get_carreiras()


@st.cache_data(show_spinner=True)
def carregar_contexto_completo():
    return get_contexto_completo()


carreiras = carregar_carreiras()
carreira_nomes = [c['nome'] for c in carreiras]

# Estado da carreira selecionada
if 'carreira_selecionada' not in st.session_state:
    st.session_state.carreira_selecionada = carreira_nomes[0]

# Sidebar: modelo Gemini e fontes
st.sidebar.markdown("🤖 Chatbot de Carreiras TechGuide")
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Modelo Gemini em uso:** `{MODELO}`")
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
        contexto_completo = carregar_contexto_completo()
        prompt = f"Você é um especialista em carreiras de tecnologia. Responda tudo sobre a área '{carreira_selecionada}' com base nas informações abaixo extraídas do site TechGuide.sh. Seja detalhado e cite as habilidades, tópicos, níveis e recomendações relevantes.\n\n{contexto_completo}"
        st.session_state.resposta_automatica = perguntar_gemini(prompt)

st.markdown(f"### Resumo da carreira selecionada: {carreira_selecionada}")
st.markdown(st.session_state.resposta_automatica)

# Chatbot opcional
st.subheader("Pergunte ao bot sobre a carreira ou aprofunde sua dúvida:")
pergunta = st.text_input("Digite sua pergunta (opcional):")

if pergunta:
    contexto_completo = carregar_contexto_completo()
    prompt = f"Você é um especialista em carreiras de tecnologia. Responda tudo sobre a área '{carreira_selecionada}' com base nas informações abaixo extraídas do site TechGuide.sh.\n\n{contexto_completo}\n\nPergunta do usuário: {pergunta}"
    resposta = perguntar_gemini(prompt)
    st.markdown(f"**Resposta:** {resposta}")
