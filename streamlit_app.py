import streamlit as st
import re
from agents.agent0_validate import agent0_validate
from agents.agent1_translate import agent1_translate
from agents.agent2_improve import agent2_improve
from agents.agent3_classify import agent3_classify
from agents.agent4_translate import agent4_translate
from agents.agent5_suggest import agent5_suggest_cause
from utils.token_count import get_token_count

import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# --- Autenticação ---
# Carrega os hashes previamente gerados
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_credentials = pickle.load(file)

credentials = {
    "usernames": {
        "Cecilia": {
            "name": "Cecilia",
            "password": hashed_credentials["Cecilia"],
            "email": "jsmith@gmail.com"
        },
        "Charles": {
            "name": "Charles",
            "password": hashed_credentials["Charles"],
            "email": "rbriggs@gmail.com"
        }
    }
}

# Create the authenticator object correctly
authenticator = stauth.Authenticate(
    credentials,
    "your_app_name",  # Use a unique name for your app
    "your_signature_key",  # Use a random secure key
    cookie_expiry_days=30,
    preauthorized=None  # Disable pre-authorization
)

# Correct way to call the login method
try:
    name, authentication_status, username = authenticator.login("Login")
    # Note: no additional location parameter
except Exception as e:
    st.error(f"Authentication error: {e}")

# Then check the authentication status
if authentication_status is None:
    st.warning("Por favor, faça login para continuar")
elif authentication_status is False:
    st.error("Usuário ou senha incorretos")
elif authentication_status:
    st.success(f"Bem-vindo, {name}!")
    # Rest of your code...
    
    # Botão de logout
    if st.sidebar.button("Logout"):
        authenticator.logout(location="main")
    st.sidebar.title(f"Olá, {name}!")
    
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
