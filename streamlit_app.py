# streamlit_app.py
import streamlit as st
import re
from agents.agent1_translate import agent1_translate
from agents.agent2_improve import agent2_improve
from agents.agent3_classify import agent3_classify
from agents.agent4_translate import agent4_translate
from utils.token_count import get_token_count

st.title("Análise de Causa Raiz da Descrição de Acidentes de Trânsito")

# Botão para limpar os dados da sessão
if st.button("Clear Data"):
    st.session_state.clear()

# Mantém a entrada de texto na sessão
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.session_state.input_text = st.text_area("Enter the accident description:", st.session_state.input_text)

if st.button("Process"):
    # Agent 1: Translate to English.
    translated_text = agent1_translate(st.session_state.input_text)
    
    # Agent 2: Improve the translated text.
    improved_text = agent2_improve(translated_text)
    
    # Agent 3: Classify the accident using reasoning with o3-mini (or alternative model).
    classification_result = agent3_classify(improved_text)
    reasoning_text = classification_result["explanation"]
    
    # Tenta extrair "Selected Cause" e "Score" do output do modelo usando regex.
    selected_cause = "Not extracted"
    score = "Not extracted"
    cause_match = re.search(r"Selected Cause:\s*(.+)", reasoning_text)
    score_match = re.search(r"Score:\s*([\d\.]+)", reasoning_text)
    if cause_match:
        selected_cause = cause_match.group(1).strip()
    if score_match:
        score = score_match.group(1).strip()
    
    # Agent 4: Translate the selected cause to Brazilian Portuguese.
    translated_cause = agent4_translate(selected_cause)
    
    # Contagem de tokens usando a função get_token_count.
    # (Você pode ajustar o parâmetro 'model' conforme necessário; aqui usamos o modelo padrão do tiktoken)
    input_token_count = get_token_count(st.session_state.input_text)
    improved_token_count = get_token_count(improved_text)
    reasoning_token_count = get_token_count(reasoning_text)
    total_tokens = input_token_count + improved_token_count + reasoning_token_count
    
    # Exibe os resultados em duas áreas.
    st.subheader("Full Model Reasoning:")
    st.text_area("Reasoning Output:", reasoning_text, height=300)
    
    # Exibe os resultados extraídos sem o Selected Cause em inglês.
    st.subheader("Extracted Results:")
    st.write(f"Translated Cause (Portuguese): {translated_cause}")
    st.write(f"Confidence Score: {score}")

    # Verifica se a causa traduzida é "Outros" e cria uma aba condicional para exibir sugestões adicionais.
    if translated_cause.lower() == "outros":
        tab1, tab2 = st.tabs(["Causa Provável", "Sugestão Adicional"])
    
        with tab1:
            st.write("Causa Probável: Outros")
        with tab2:
            # Aqui você pode colocar o que o modelo ou sua lógica adicional sugere como causa
            st.write("Sugestão de causa adicional: Visibilidade ou atenção inadequada ao obstáculo na estrada")

    
    st.subheader("Token Count Information:")
    st.write(f"Input text tokens: {input_token_count}")
    st.write(f"Improved text tokens: {improved_token_count}")
    st.write(f"Reasoning output tokens: {reasoning_token_count}")
    st.write(f"Total tokens processed: {total_tokens}")
