# agents/agent2_improve.py
from utils.text_improvement import improve_accident_text

def agent2_improve(text: str) -> str:
    """
    Improves the translated text by replacing general terms with more technical terms 
    related to road safety and safety engineering.
    """
    return improve_accident_text(text)
