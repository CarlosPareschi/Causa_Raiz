import streamlit as st
import re
from agents.agent1_translate import agent1_translate
from agents.agent2_improve import agent2_improve
from agents.agent3_classify import agent3_classify
from agents.agent4_translate import agent4_translate
from utils.token_count import get_token_count

# Importe o novo agente para sugerir causa
from agents.agent5_suggest import agent5_suggest_cause

st.title("Análise de Causa Raiz da Descrição de Acidentes de Trânsito")

# Botão para limpar os dados da sessão
if st.button("Clear Data"):
    st.session_state.clear()

# Mantém a entrada de texto na sessão
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

st.session_state.input_text = st.text_area("Enter the accident description:", st.session_state.input_text)

if st.button("Process"):
    # Agent 1: Tradução para inglês.
    translated_text = agent1_translate(st.session_state.input_text)
    
    # Agent 2: Melhora do texto traduzido.
    improved_text = agent2_improve(translated_text)
    
    # Agent 3: Classificação do acidente e geração do chain-of-thought.
    classification_result = agent3_classify(improved_text)
    reasoning_text = classification_result["explanation"]
    
    # Extração de "Selected Cause" e "Score" usando regex.
    selected_cause = "Not extracted"
    score = "Not extracted"
    cause_match = re.search(r"Selected Cause:\s*(.+)", reasoning_text)
    score_match = re.search(r"Score:\s*([\d\.]+)", reasoning_text)
    if cause_match:
        selected_cause = cause_match.group(1).strip()
    if score_match:
        score = score_match.group(1).strip()
    
    # Agent 4: Tradução da causa selecionada para o português.
    translated_cause = agent4_translate(selected_cause)
    
    # Contagem de tokens.
    input_token_count = get_token_count(st.session_state.input_text)
    improved_token_count = get_token_count(improved_text)
    reasoning_token_count = get_token_count(reasoning_text)
    total_tokens = input_token_count + improved_token_count + reasoning_token_count
    
    # Exibe o chain-of-thought completo.
    st.subheader("Full Model Reasoning:")
    st.text_area("Reasoning Output:", reasoning_text, height=300)
    
    # Exibe os resultados extraídos (sempre).
    st.subheader("Extracted Results:")
    st.write(f"Translated Cause (Portuguese): {translated_cause}")
    st.write(f"Confidence Score: {score}")
    
    # Se a causa traduzida for "Outros", permitir que o modelo sugira uma nova causa.
    if "outros" in translated_cause.lower():
        # Chama o novo agente para sugerir uma causa mais específica.
        suggested_cause = agent5_suggest_cause(improved_text)
        
        tab1, tab2 = st.tabs(["Nova Causa Sugerida", "Detalhes Adicionais"])
    
        with tab1:
            st.write(f"Nova Causa Sugerida: {suggested_cause}")
            st.write(f"Confidence Score: {score}")
    
        with tab2:
            st.write("Detalhes adicionais podem ser exibidos aqui, se necessário.")
    
    st.subheader("Token Count Information:")
    st.write(f"Input text tokens: {input_token_count}")
    st.write(f"Improved text tokens: {improved_token_count}")
    st.write(f"Reasoning output tokens: {reasoning_token_count}")
    st.write(f"Total tokens processed: {total_tokens}")
