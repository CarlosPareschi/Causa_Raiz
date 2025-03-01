import streamlit as st
import re
from agents.agent0_validate import agent0_validate
from agents.agent1_translate import agent1_translate
from agents.agent2_improve import agent2_improve
from agents.agent3_classify import agent3_classify
from agents.agent4_translate import agent4_translate
from agents.agent5_suggest import agent5_suggest_cause
from utils.token_count import get_token_count

import streamlit_authenticator as stauth

# Carrega as senhas do secrets.toml
usernames = ["Cecilia", "Charles"]
names = ["Cecilia", "Charles"]
hashed_passwords = [st.secrets["passwords"]["Cecilia"], st.secrets["passwords"]["Charles"]]

# Configura as credenciais
credentials = {
    "usernames": {}
}

for i in range(len(names)):
    credentials["usernames"][usernames[i]] = {
        "name": names[i],
        "password": hashed_passwords[i]
    }

# Cria o autenticador
authenticator = stauth.Authenticate(
    credentials,
    st.secrets["cookie"]["name"],
    st.secrets["cookie"]["key"],
    cookie_expiry_days=st.secrets["cookie"]["expiry_days"]
)

# Mostra a tela de login
# Adicione um nome para o formulário de login
name, authentication_status, username = authenticator.login("Login", "main")

# Verifica o status de autenticação
if authentication_status is None:
    st.warning("Por favor, faça login para continuar")
elif authentication_status is False:
    st.error("Usuário ou senha incorretos")
elif authentication_status:
    # Layout com duas colunas para mostrar o nome do usuário e botão de logout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.success(f"Bem-vindo, {name}!")
    
    with col2:
        # Botão de logout no canto direito
        try:
            authenticator.logout("Logout", "main")
        except KeyError:
            st.warning("Cookie não encontrado. Talvez o usuário não esteja logado ou o cookie já expirou.")





    
    st.title("Análise de Causa Raiz da Descrição de Acidentes de Trânsito")
    
    # Botão para limpar os dados da sessão
    if st.button("Clear Data"):
        st.session_state.clear()

    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
        
    st.session_state.input_text = st.text_area("Enter the accident description:", st.session_state.input_text)
    
    if st.button("Process"):
        if not agent0_validate(st.session_state.input_text):
            st.error("Isso não é uma descrição de acidente, favor redigir novamente o texto.")
        else:
            translated_text = agent1_translate(st.session_state.input_text)
            improved_text = agent2_improve(translated_text)
            classification_result = agent3_classify(improved_text)
            reasoning_text = classification_result["explanation"]

            selected_cause = "Not extracted"
            score = "Not extracted"
            cause_match = re.search(r"Selected Cause:\s*(.+)", reasoning_text)
            score_match = re.search(r"Score:\s*([\d\.]+)", reasoning_text)
            if cause_match:
                selected_cause = cause_match.group(1).strip()
            if score_match:
                score = score_match.group(1).strip()

            translated_cause = agent4_translate(selected_cause)
            input_token_count = get_token_count(st.session_state.input_text)
            improved_token_count = get_token_count(improved_text)
            reasoning_token_count = get_token_count(reasoning_text)
            total_tokens = input_token_count + improved_token_count + reasoning_token_count

            st.subheader("Full Model Reasoning:")
            st.text_area("Reasoning Output:", reasoning_text, height=300)

            st.subheader("Extracted Results:")
            st.write(f"Causa raiz: {translated_cause}")
            st.write(f"Confidence Score: {score}")

            if "outros" in translated_cause.lower():
                suggested_cause = agent5_suggest_cause(improved_text)
                tabs = st.tabs(["Nova Causa Sugerida"])
                with tabs[0]:
                    st.write(f"Nova Causa Sugerida: {suggested_cause}")
                    st.write(f"Confidence Score: {score}")

            st.subheader("Token Count Information:")
            st.write(f"Input text tokens: {input_token_count}")
            st.write(f"Improved text tokens: {improved_token_count}")
            st.write(f"Reasoning output tokens: {reasoning_token_count}")
            st.write(f"Total tokens processed: {total_tokens}")
