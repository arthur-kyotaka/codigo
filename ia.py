import streamlit as st
from openai import OpenAI

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="Guia Galático",
    page_icon="🛰️",
    layout="centered",
    initial_sidebar_state="expanded"
)


# ==========================================
# 2. ESTILIZAÇÃO ESPACIAL
# ==========================================

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0f19 !important;
        color: #e2e8f0 !important;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    .main, .block-container {
        background-color: #0b0f19 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1e3a8a !important;
    }

    /* Mensagens do chat */
    [data-testid="stChatMessage"] {
        background-color: #111827 !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] li {
        color: #f8fafc !important;
        font-size: 16px !important;
    }

    /* Campo de entrada */
    [data-testid="stChatInput"] {
        background-color: #111827 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.4) !important;
    }

    [data-testid="stChatInput"] div,
    [data-testid="stChatInput"] textarea {
        background-color: #111827 !important;
        color: #ffffff !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #94a3b8 !important;
    }

    [data-testid="stChatInput"] button {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }

    [data-testid="stChatInput"] button svg {
        fill: #60a5fa !important;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #60a5fa !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. MENU LATERAL
# ==========================================

st.sidebar.title("🚀 Navegação Galática")

pagina = st.sidebar.radio(
    "Escolha a seção:",
    [
        "Chat ExplorerBot",
        "Política de Privacidade & Termos"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Projeto acadêmico desenvolvido para exploração "
    "de dados espaciais da NASA."
)


# ==========================================
# 4. PÁGINA DO CHAT
# ==========================================

if pagina == "Chat ExplorerBot":

    st.title("🛰️ ExplorerBot - NASA & Satélites")

    st.caption(
        "Tire suas dúvidas sobre missões espaciais, "
        "satélites e astronomia."
    )

    st.divider()

    # ------------------------------------------
    # CONFIGURAÇÃO DA API
    # ------------------------------------------

    try:
        cliente = OpenAI(
            api_key=st.secrets["GEMINI_API_KEY"],
            base_url=(
                "https://generativelanguage.googleapis.com/"
                "v1beta/openai/"
            )
        )

    except Exception:
        st.error(
            "Não foi possível configurar a API do Gemini. "
            "Verifique se GEMINI_API_KEY está configurada "
            "corretamente nos Secrets do Streamlit."
        )
        st.stop()

    # ------------------------------------------
    # CONFIGURAÇÕES DE HISTÓRICO
    # ------------------------------------------

    # Quantidade máxima de mensagens enviadas à API.
    # Isso não apaga as mensagens exibidas no chat.
    LIMITE_HISTORICO_API = 10

    # Inicializa o histórico da conversa.
    if "historico" not in st.session_state:
        st.session_state["historico"] = []

    # ------------------------------------------
    # EXIBIR CONVERSA ANTERIOR
    # ------------------------------------------

    for mensagem in st.session_state["historico"]:

        with st.chat_message(mensagem["role"]):
            st.write(mensagem["content"])

    # ------------------------------------------
    # ENTRADA DO USUÁRIO
    # ------------------------------------------

    texto_usuario = st.chat_input(
        "Digite sua pergunta sobre o espaço..."
    )

    if texto_usuario:

        # Exibe a pergunta do usuário.
        with st.chat_message("user"):
            st.write(texto_usuario)

        # Adiciona a pergunta ao histórico da sessão.
        st.session_state["historico"].append({
            "role": "user",
            "content": texto_usuario
        })

        # ------------------------------------------
        # PREPARAR HISTÓRICO PARA A API
        # ------------------------------------------

        historico = st.session_state["historico"]

        # Seleciona somente as mensagens mais recentes.
        mensagens_api = historico[-LIMITE_HISTORICO_API:]

        # Evita começar o contexto com uma resposta antiga
        # do assistente, se isso ocorrer após o recorte.
        if (
            mensagens_api
            and mensagens_api[0]["role"] == "assistant"
        ):
            mensagens_api = mensagens_api[1:]

        # ------------------------------------------
        # SOLICITAR RESPOSTA À IA
        # ------------------------------------------

        with st.chat_message("assistant"):

            resposta_completa = ""
            holder = st.empty()

            try:
                with st.spinner(
                    "A consultar os arquivos orbitais..."
                ):

                    resposta_stream = (
                        cliente.chat.completions.create(
                            model="gemini-3.8-flash",
                            messages=mensagens_api,
                            reasoning_effort="low",
                            stream=True
                        )
                    )

                    # Recebe a resposta em partes.
                    for chunk in resposta_stream:

                        if not chunk.choices:
                            continue

                        conteudo = chunk.choices[0].delta.content

                        if conteudo:
                            resposta_completa += conteudo
                            holder.write(resposta_completa)

                # ----------------------------------
                # SALVAR RESPOSTA
                # ----------------------------------

                if resposta_completa.strip():

                    st.session_state["historico"].append({
                        "role": "assistant",
                        "content": resposta_completa
                    })

                else:
                    st.warning(
                        "A IA não retornou uma resposta. "
                        "Tente enviar a pergunta novamente."
                    )

            # --------------------------------------
            # TRATAMENTO DE ERROS
            # --------------------------------------

            except Exception as erro:

                erro_texto = str(erro).upper()

                if (
                    "429" in erro_texto
                    or "RESOURCE_EXHAUSTED" in erro_texto
                    or "RATE_LIMIT" in erro_texto
                    or "QUOTA" in erro_texto
                ):

                    st.warning(
                        "🚀 O limite de requisições da IA "
                        "foi atingido.\n\n"
                        "Aguarde a renovação da cota ou "
                        "verifique os limites do projeto "
                        "no Google AI Studio."
                    )

                elif (
                    "401" in erro_texto
                    or "403" in erro_texto
                    or "AUTHENTICATION" in erro_texto
                    or "PERMISSION_DENIED" in erro_texto
                ):

                    st.error(
                        "🔐 Não foi possível autenticar "
                        "a API. Verifique a chave, as "
                        "permissões e a configuração do projeto."
                    )

                else:

                    st.error(
                        "Não foi possível obter uma resposta. "
                        "Verifique sua conexão e tente novamente."
                    )

                # Não exibe detalhes técnicos nem a chave
                # da API diretamente para o visitante.


# ==========================================
# 5. POLÍTICA DE PRIVACIDADE E TERMOS
# ==========================================

elif pagina == "Política de Privacidade & Termos":

    st.title("📜 Política de Privacidade e Termos de Uso")

    st.caption("Última atualização: Outubro de 2026")

    st.divider()

    st.subheader("1. Sobre o Projeto")

    st.write("""
    O **ExplorerBot** é um assistente virtual interativo
    desenvolvido por Arthur R. Santos como parte de um
    trabalho acadêmico universitário da Universidade
    Paulista (UNIP).

    Seu objetivo é fornecer informações educativas e
    interativas sobre missões espaciais, satélites e
    astronomia.
    """)

    st.subheader("2. Privacidade e Dados dos Usuários")

    st.markdown("""
    - **Histórico da sessão:** as conversas são mantidas
      temporariamente no estado da sessão do Streamlit.
      O código não grava o histórico em um banco de dados
      permanente.

    - **Processamento por IA:** as mensagens selecionadas
      são enviadas à API do Google Gemini para gerar respostas.

    - **Dados pessoais:** não envie informações pessoais,
      confidenciais ou sensíveis durante a interação.
    """)

    st.subheader(
        "3. Direitos Autorais e Isenção de Responsabilidade"
    )

    st.markdown("""
    - As informações astronômicas podem se basear em dados
      públicos de agências espaciais, como a NASA.

    - O projeto tem finalidade educacional e acadêmica,
      sem fins comerciais.

    - As respostas geradas por inteligência artificial
      podem conter imprecisões. Verifique informações
      importantes em fontes confiáveis.
    """)

    st.divider()

    st.success(
        "Dúvidas sobre os termos? Entre em contato com "
        "a equipe de desenvolvimento acadêmico."
    )