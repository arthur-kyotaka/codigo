import streamlit as st
from openai import OpenAI

# 1. Configuração da página (Deve ser o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Guia Galático",
    page_icon="🛰️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO ESPACIAL (Tema Escuro & Azul RGB Otimizado) ---
st.markdown("""
    <style>
    /* Força o fundo absoluto do navegador e do Streamlit */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0b0f19 !important;
        color: #e2e8f0 !important;
    }
    
    /* Remove qualquer container cinza ou branco nas pontas */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: transparent !important;
    }
    
    /* Bloco principal de conteúdo */
    .main, .block-container {
        background-color: #0b0f19 !important;
    }
    
    /* Barra lateral estilizada */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1e3a8a !important;
    }
    
    /* CAIXAS DE CHAT (Usuário e Bot) */
    [data-testid="stChatMessage"] {
        background-color: #111827 !important;
        border: 1px solid #3b82f6 !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
    }
    
    /* Texto das mensagens super visível */
    [data-testid="stChatMessage"] p, 
    [data-testid="stChatMessage"] span, 
    [data-testid="stChatMessage"] li, 
    [data-testid="stChatMessage"] div {
        color: #f8fafc !important;
        font-size: 16px !important;
    }
    
    /* --- CORREÇÃO DA CAIXA DE INPUT (Fundo escuro e borda RGB) --- */
    
    /* Container principal da barra de chat na parte inferior */
    [data-testid="stChatInput"] {
        background-color: #111827 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 12px !important;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Força a área interna onde o usuário digita a ficar escura e sem fundo branco */
    [data-testid="stChatInput"] div, 
    [data-testid="stChatInput"] input, 
    [data-testid="stChatInput"] textarea {
        background-color: #111827 !important;
        color: #ffffff !important;
    }
    
    /* Botão de enviar dentro do input (deixa com a cara do tema espacial) */
    [data-testid="stChatInput"] button {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stChatInput"] button svg {
        fill: #60a5fa !important;
    }
    
    /* Títulos em azul espacial */
    h1, h2, h3 {
        color: #60a5fa !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL (Navegação) ---
st.sidebar.title("🚀 Navegação Galática")
pagina = st.sidebar.radio("Escolha a seção:", ["Chat ExplorerBot", "Política de Privacidade & Termos"])
st.sidebar.divider()
st.sidebar.info("Projeto acadêmico desenvolvido para exploração de dados espaciais da NASA.")


# ==========================================
# PÁGINA 1: O CHAT (EXPLORERBOT)
# ==========================================
if pagina == "Chat ExplorerBot":
    st.title("🛰️ ExplorerBot - NASA & Satélites")
    st.caption("Tire as suas dúvidas sobre missões espaciais, satélites e astronomia.")
    st.divider()

    # CHAVE API
    cliente = OpenAI(
        api_key=st.secrets["GEMINI_API_KEY"],
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Histórico de mensagem
    if "historico" not in st.session_state:
        st.session_state["historico"] = []

    # Exibir mensagens antigas
    for mensagem in st.session_state["historico"]:
        with st.chat_message(mensagem["role"]):
            st.write(mensagem["content"])

    # Campo para usuário interagir com o bot
    texto_usuario = st.chat_input("Digite a sua pergunta sobre o espaço...")

    if texto_usuario:
        st.session_state["historico"].append({"role": "user", "content": texto_usuario})
        with st.chat_message("user"):
            st.write(texto_usuario)
            
        # Resposta da IA com Streaming
        with st.chat_message("assistant"):
            with st.spinner("A consultar os arquivos orbitais..."):
                resposta_stream = cliente.chat.completions.create(
                    model="gemini-3.8-flash",
                    messages=st.session_state["historico"],
                    stream=True
                )
                
                resposta_completa = ""
                holder = st.empty()
                for chunk in resposta_stream:
                    if chunk.choices[0].delta.content is not None:
                        resposta_completa += chunk.choices[0].delta.content
                        holder.write(resposta_completa)
                        
        st.session_state["historico"].append({"role": "assistant", "content": resposta_completa})

# ==========================================
# PÁGINA 2: POLÍTICA DE PRIVACIDADE E TERMOS
# ==========================================
elif pagina == "Política de Privacidade & Termos":
    st.title("📜 Política de Privacidade e Termos de Uso")
    st.caption("Última atualização: Outubro de 2026")
    st.divider()

    st.subheader("1. Sobre o Projeto")
    st.write("""
    O **ExplorerBot** é um assistente virtual interativo desenvolvido por Arhur R. Santos, como parte de um trabalho acadêmico universitário da instituição Universidade Paulista (Unip). 
    O seu objetivo é fornecer informações educativas e interativas sobre missões espaciais, satélites e dados públicos da NASA.
    """)

    st.subheader("2. Privacidade e Dados dos Usuários")
    st.write("""
    * **Armazenamento de Sessão:** As conversas realizadas no chat são mantidas apenas temporariamente na memória da sessão (`st.session_state`) do seu navegador. Nenhum histórico de conversa é armazenado permanentemente em bancos de dados externos.
    * **Uso da API de IA:** As mensagens enviadas ao chat são processadas através da API do Google Gemini. Recomendamos que **não** envie informações pessoais, confidenciais ou sensíveis durante a interação.
    """)

    st.subheader("3. Direitos Autorais e Isenção de Responsabilidade")
    st.write("""
    * As informações astronómicas baseiam-se em dados públicos e abertos fornecidos por agências espaciais como a NASA e parcerias.
    * Este site tem fins estritamente educacionais e de pesquisa universitária, sem fins comerciais.
    """)

    st.divider()
    st.success("Dúvidas sobre os termos? Entre em contato com a equipe de desenvolvimento acadêmico.")