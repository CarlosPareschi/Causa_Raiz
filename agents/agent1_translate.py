# agents/agent1_translate.py
from utils.translation import translate_to_english

def agent1_translate(text: str) -> str:
    """
    Translates the input text from Portuguese to English.
    """
    return translate_to_english(text)
