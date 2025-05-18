import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://techguide.sh"

# Função para coletar todas as carreiras disponíveis na página principal


def get_carreiras(url=BASE_URL):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    carreiras = []
    # Procura por links de carreiras (ex: /pt-BR/path/data-science/)
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/pt-BR/path/' in href and href.endswith('/'):
            nome = a.text.strip()
            if nome and {'nome': nome, 'url': BASE_URL + href} not in carreiras:
                carreiras.append({'nome': nome, 'url': BASE_URL + href})
    return carreiras

# Função para coletar dados detalhados de uma carreira específica (filtrando rodapés e institucionais)


def get_detalhes_carreira(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    detalhes = []
    # Coleta apenas seções principais (ignorando rodapé, redes sociais, etc)
    main = soup.find('main') or soup
    for section in main.find_all(['h2', 'h3', 'ul', 'ol'], recursive=True):
        if section.name in ['h2', 'h3']:
            titulo = section.text.strip()
            # Ignora títulos institucionais
            if not re.search(r'(youtube|facebook|twitter|instagram|playstore|appstore|tiktok|guia em formato|descubra o que dominar|desafie-se|dúvidas e respostas|logo|versão|alura|pm3|fiap)', titulo, re.I):
                detalhes.append({'tipo': 'titulo', 'conteudo': titulo})
        elif section.name in ['ul', 'ol']:
            itens = [li.text.strip() for li in section.find_all('li')]
            # Ignora listas institucionais
            if itens and not any(re.search(r'(youtube|facebook|twitter|instagram|playstore|appstore|tiktok)', item, re.I) for item in itens):
                detalhes.append({'tipo': 'lista', 'conteudo': itens})
    return detalhes

# Função para contexto geral (opcional, não scraping em massa)


def get_contexto_completo():
    return "Contexto geral do TechGuide.sh. Use get_detalhes_carreira para detalhes sob demanda."


if __name__ == "__main__":
    carreiras = get_carreiras()
    print("Carreiras disponíveis:")
    for c in carreiras:
        print(f"- {c['nome']}: {c['url']}")
    # Exemplo: coletar detalhes de Data Science
    ds = next(
        (c for c in carreiras if 'data science' in c['nome'].lower()), None)
    if ds:
        detalhes = get_detalhes_carreira(ds['url'])
        print(f"\nDetalhes de {ds['nome']}:")
        for d in detalhes:
            print(d)
