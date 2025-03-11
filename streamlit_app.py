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

credentials = dict(st.secrets["credentials"])

authenticator = stauth.Authenticate(
    credentials,
    st.secrets["cookie"]["name"],
    st.secrets["cookie"]["key"],
    cookie_expiry_days=st.secrets["cookie"]["expiry_days"]
)

name, authentication_status, username = authenticator.login("Login", "main")

def custom_logout():
    # Zera as chaves de autenticação
    st.session_state["authentication_status"] = None
    st.session_state["name"] = None
    st.session_state["username"] = None
    # Força o recarregamento automático da página via meta refresh:
    st.markdown("<meta http-equiv='refresh' content='0'>", unsafe_allow_html=True)

if authentication_status:
    st.sidebar.button("Logout", key="logout_btn", on_click=custom_logout)

    st.title("Análise de Causa Raiz da Descrição de Acidentes de Trânsito")
    
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "clear_counter" not in st.session_state:
        st.session_state.clear_counter = 0

    def clear_data_callback():
        st.session_state.input_text = ""
        st.session_state.clear_counter += 1

    st.button("Clear Data", key="clear_data_btn", on_click=clear_data_callback)
    
    input_text = st.text_area("Enter the accident description:",
                              value=st.session_state.input_text,
                              key=f"input_text_{st.session_state.clear_counter}")
    st.session_state.input_text = input_text
    
    if st.button("Process", key="process_btn"):
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
            cached_input_token_count = get_token_count(improved_text)
            output_token_count = get_token_count(reasoning_text)
            
            st.write(f"Input text tokens: {input_token_count}")
            st.write(f"Cached input tokens (improved text): {cached_input_token_count}")
            st.write(f"Output tokens (reasoning output): {output_token_count}")
            
            cost_input = input_token_count / 1_000_000 * 1.10
            cost_cached_input = cached_input_token_count / 1_000_000 * 0.55
            cost_output = output_token_count / 1_000_000 * 4.40
            total_cost = cost_input + cost_cached_input + cost_output
            
            st.subheader("Token Cost Information:")
            st.write(f"Input tokens cost: ${cost_input:.6f}")
            st.write(f"Cached input tokens cost: ${cost_cached_input:.6f}")
            st.write(f"Output tokens cost: ${cost_output:.6f}")
            st.write(f"Total cost: ${total_cost:.6f}")
            
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
else:
    if authentication_status is False:
        st.error("Usuário ou senha incorretos")
    else:
        st.warning("Por favor, faça login para continuar")
