# utils/translation.py
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def translate_to_english(text: str) -> str:
    """
    Translate the text from Portuguese to English.
    For simplicity, this function currently returns a dummy translation.
    Replace this with an actual API call or translation logic if needed.
    """
    return "Translated to English: " + text

def translate_to_portuguese(text: str) -> str:
    """
    Translate an accident cause from English to Brazilian Portuguese using a predefined mapping.
    """
    translation_map = {
        "Driver distraction": "Distração ao volante",
        "Speeding": "Excesso de velocidade",
        "Driving under the influence of alcohol or drugs": "Condução sob efeito de álcool ou drogas",
        "Disregard for traffic rules": "Desrespeito às regras de trânsito",
        "Fatigue and drowsiness": "Fadiga e sonolência",
        "Lack of vehicle maintenance": "Falta de manutenção de veículo",
        "Adverse weather conditions": "Condições climáticas adversas",
        "Inadequate infrastructure": "Infraestrutura inadequada",
        "Aggressive behavior": "Comportamento agressivo",
        "Lack of experience": "Falta de experiência",
        "Inadequate use of safety equipment": "Uso inadequado de equipamentos de segurança",
        "Animals on the road": "Animais na pista",
        "Visibility issues": "Problemas de visibilidade",
        "Disregard for right of way": "Desrespeito às preferenciais",
        "Improper lane usage": "Uso inadequado de faixas",
        "Lack of attention to pedestrians and cyclists": "Falta de atenção a pedestres e ciclistas",
        "Driver health issues": "Problemas de saúde do motorista",
        "Pedestrian inattention": "Falta de atenção do pedestre",
        "Visibility or inadequate attention to the obstacle on the road": "Visibilidade ou atenção inadequada ao obstáculo na estrada",
        "Others": "Outros"
    }
    return translation_map.get(text, text)

