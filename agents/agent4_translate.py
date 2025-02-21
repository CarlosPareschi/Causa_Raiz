# agents/agent4_translate.py
from utils.translation import translate_to_portuguese

def agent4_translate(root_cause: str) -> str:
    """
    Translates the given accident cause from English to Brazilian Portuguese
    using a predefined mapping.
    """
    return translate_to_portuguese(root_cause)
