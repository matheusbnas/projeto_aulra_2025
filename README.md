# 🤖 Chatbot de Carreiras TechGuide

Este projeto é um chatbot interativo construído com [Streamlit](https://streamlit.io/) que responde dúvidas sobre perfis profissionais e habilidades necessárias para atuar em áreas de tecnologia, utilizando inteligência artificial generativa (Google Gemini) e dados raspados do site [TechGuide.sh](https://techguide.sh/).

## Funcionalidades

- Chatbot com IA Gemini (modelo `gemini-2.0-flash-lite`)
- Raspagem automática das profissões e habilidades do [TechGuide.sh](https://techguide.sh/)
- Interface web simples e intuitiva
- Respostas contextualizadas sobre carreiras em tecnologia

## Fonte dos Dados

Os dados de profissões e habilidades são coletados automaticamente do site:

- [https://techguide.sh/](https://techguide.sh/)

## Como rodar o projeto

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

5. **Execute o app:**

   ```bash
   streamlit run app.py
   ```

6. **Acesse no navegador:**
   - O Streamlit irá mostrar o link local (geralmente http://localhost:8501)

## Como usar

- Digite sua pergunta sobre carreiras, profissões ou habilidades em tecnologia no campo de texto e pressione Enter.
- O bot irá responder automaticamente com base nos dados do [TechGuide.sh](https://techguide.sh/) e na IA Gemini.
- No menu lateral, você pode ver a lista de profissões disponíveis.

## Exemplo de perguntas

- "Quais habilidades preciso para ser cientista de dados?"
- "O que faz um analista de segurança?"
- "Quais áreas existem em dados?"

## Licença

Este projeto é apenas para fins educacionais e de demonstração.

---

**Fonte dos dados:** [https://techguide.sh/](https://techguide.sh/)
