# utils/text_improvement.py
def improve_accident_text(text: str) -> str:
    """
    Improves the translated text by replacing general terms with more technical terms 
    related to road safety and safety engineering.
    For example, it may change "car" to "vehicle", "accident" to "incident", etc.
    Customize the replacement dictionary as needed.
    """
    replacements = {
        "car": "vehicle",
        "accident": "incident",
        "crash": "collision",
        "driver": "operator",
        "road": "transportation infrastructure",
        "safety": "security engineering"
        # Add more mappings as needed.
    }
    improved_text = text
    for old, new in replacements.items():
        improved_text = improved_text.replace(old, new)
    return improved_text