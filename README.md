# 🤖 Chatbot de Carreiras TechGuide

Este projeto é um chatbot inteligente e multimodal, construído com [Streamlit](https://streamlit.io/), que responde dúvidas sobre perfis profissionais e habilidades necessárias para atuar em áreas de tecnologia, utilizando inteligência artificial generativa (Google Gemini) e dados raspados do site [TechGuide.sh](https://techguide.sh/).

Agora, o chatbot também permite criar eventos no Google Agenda usando comandos especiais, além de responder perguntas sobre carreiras!

## Deploy Online

Acesse o chatbot em produção:
👉 [https://chatbot-scraper.streamlit.app/](https://chatbot-scraper.streamlit.app/)

## Funcionalidades

- Chatbot com IA Gemini (modelo `gemini-2.0-flash-lite`)
- Raspagem automática das profissões e habilidades do [TechGuide.sh](https://techguide.sh/)
- Interface web moderna e responsiva
- Respostas contextualizadas sobre carreiras em tecnologia
- **Comando especial @agenda:** Crie eventos no Google Agenda diretamente pelo chat
- Pronto para integração futura com Google Keep e outros serviços Google
- Sidebar com seleção de carreira, fontes e portfólio

## Como rodar o projeto localmente

1. **Clone o repositório e acesse a pasta:**

   ```bash
   git clone <url-do-repo>
   cd projeto_aulra_2025
   ```

2. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # Ou
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure sua chave da API Gemini:**

   - Crie um arquivo `.env` na raiz do projeto com o conteúdo:
     ```
     GOOGLE_API_KEY=SUA_CHAVE_AQUI
     ```
   - Você pode obter uma chave em: [Google AI Studio](https://aistudio.google.com/app/apikey)

5. **Configure as credenciais do Google para Agenda:**

   - No [Google Cloud Console](https://console.cloud.google.com/), ative a API do Google Agenda e crie um ID OAuth 2.0.
   - Baixe o arquivo `credentials.json` e coloque na raiz do projeto.

6. **Execute o app:**

   ```bash
   streamlit run app.py
   ```

7. **Acesse no navegador:**
   - O Streamlit irá mostrar o link local (geralmente http://localhost:8501)

## Como usar

- Selecione uma carreira no menu lateral.
- Veja o resumo automático da carreira na tela principal.
- Use o campo de chat para perguntar sobre a carreira ou usar comandos especiais.
- **Para criar um evento no Google Agenda:**
  - Digite, por exemplo: `@agenda criar evento para reunião amanhã às 10h`
  - O app irá pedir autorização do Google e criar o evento na sua agenda.
- (Futuro) Use `@keep` para criar anotações no Google Keep.

## Exemplo de comandos

- "Quais habilidades preciso para ser cientista de dados?"
- `@agenda criar evento para entrevista de emprego segunda às 15h`
- `@keep criar anotação sobre dicas de carreira em dados`

## Fontes e Portfólio

- Matheus Bernardes - [Portfólio](https://portfolio-matheusbernardes.netlify.app/)
- Matech - [Site da empresa](https://matechai.com/)
- Dados de carreira: [https://techguide.sh/](https://techguide.sh/)

## Licença

Este projeto é apenas para fins educacionais e de demonstração.

---

**Deploy:** [https://chatbot-scraper.streamlit.app/](https://chatbot-scraper.streamlit.app/)
