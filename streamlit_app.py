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
credentials = {"usernames": {}}
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

# Renderiza a tela de login
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    # Renderiza o botão de logout na sidebar (o método logout já renderiza seu botão)
    if authenticator.logout("Logout", "sidebar"):
        if "input_text" in st.session_state:
            del st.session_state["input_text"]
        st.stop()

    st.title("Análise de Causa Raiz da Descrição de Acidentes de Trânsito")
    
    # Inicializa a variável de input e o contador de limpeza, se não existirem
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""
    if "clear_counter" not in st.session_state:
        st.session_state.clear_counter = 0

    # Função callback para limpar o conteúdo e incrementar o contador
    def clear_data_callback():
        st.session_state.input_text = ""
        st.session_state.clear_counter += 1

    # Botão para limpar o conteúdo do campo de texto usando on_click
    st.button("Clear Data", key="clear_data_btn", on_click=clear_data_callback)
    
    # Exibe o text_area utilizando o valor da sessão e uma chave que depende do clear_counter
    input_text = st.text_area("Enter the accident description:",
                              value=st.session_state.input_text,
                              key=f"input_text_{st.session_state.clear_counter}")
    st.session_state.input_text = input_text  # Atualiza a sessão com o valor digitado
    
    if st.button("Process", key="process_btn"):
        if not agent0_validate(st.session_state.input_text):
            st.error("Isso não é uma descrição de acidente, favor redigir novamente o texto.")
        else:
            # Processamento dos textos
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
            
            # Cálculo dos tokens para cada categoria
            input_token_count = get_token_count(st.session_state.input_text)
            cached_input_token_count = get_token_count(improved_text)
            output_token_count = get_token_count(reasoning_text)
            
            # Exibe as contagens de tokens
            st.write(f"Input text tokens: {input_token_count}")
            st.write(f"Cached input tokens (improved text): {cached_input_token_count}")
            st.write(f"Output tokens (reasoning output): {output_token_count}")
            
            # Calcula o custo em dólares para cada categoria (por milhão de tokens)
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
