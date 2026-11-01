import streamlit as st
from openai import OpenAI

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================

st.set_page_config(
    page_title="galactic guide",
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
    "Choose the section:",
    [
        "Chat ExplorerBot",
        "Privacy Policy & Terms"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Academic project developed for exploration "
    "from NASA spatial data."
)


# ==========================================
# 4. PÁGINA DO CHAT
# ==========================================

if pagina == "Chat ExplorerBot":

    st.title("🛰️ ExplorerBot - NASA & Satellites")

    st.caption(
        "Tire suas dúvidas sobre missões espaciais, "
        "satellites and astronomy."
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
            "It was not possible to configure the Gemini API."
            "Check if GEMINI_API_KEY is set "
            "correctly in Streamlit Secrets."
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
        "Type your question about space..."
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
                    "Consulting the orbital archives..."
                ):

                    resposta_stream = (
                        cliente.chat.completions.create(
                            model="gemini-3.5-flash-lite",
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
                        "The AI ​​did not return a response."
                        "Try sending the question again."
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
                       "🚀 The AI ​​request limit "
                        "has been reached.\n\n"
                        "Please wait for your quota to reset, or "
                        "check your project limits "
                        "in Google AI Studio."
                    )

                elif (
                    "401" in erro_texto
                    or "403" in erro_texto
                    or "AUTHENTICATION" in erro_texto
                    or "PERMISSION_DENIED" in erro_texto
                ):

                    st.error(
                        "🔐 Unable to authenticate "
                        "the API. Please check the key, "
                        "permissions, and project configuration."
                    )

                else:

                    st.error(
                       "Unable to get a response. "
                        "Check your connection and try again."
                    )

                # Não exibe detalhes técnicos nem a chave
                # da API diretamente para o visitante.


# ==========================================
# 5. POLÍTICA DE PRIVACIDADE E TERMOS
# ==========================================

elif pagina == "Privacy Policy & Terms":

    st.title("📜 Privacy Policy and Terms of Use")
    st.caption("Last updated: October 2026")
    st.divider()

    st.subheader("1. About the Project")

    st.write("""
    **ExplorerBot** is an interactive virtual assistant
    developed by Arthur R. Santos as part of an
    academic project at Universidade Paulista (UNIP).

    Its purpose is to provide educational and
    interactive information about space missions,
    satellites, and astronomy.
    """)

    st.subheader("2. Privacy and User Data")

    st.markdown("""
    - **Session history:** conversations are kept
      temporarily within Streamlit’s session state.
      The code does not save the history to a permanent database.

    - **AI processing:** selected messages
      are sent to the Google Gemini API to generate responses.

    - **Personal data:** do not submit any personal,
      confidential, or sensitive information during your interaction.
    """)

    st.subheader(
        "3. Copyright and Disclaimer"
    )

    st.markdown("""
    - Astronomical information may be based on public data
      from space agencies, such as NASA.

    - The project is for educational and academic purposes
      only, with no commercial intent.

    - Responses generated by artificial intelligence
      may contain inaccuracies. Please verify important
      information using reliable sources.
    """)

    st.divider()

    st.success(
        "Questions about the terms? Contact the "
        "academic development team."
    )