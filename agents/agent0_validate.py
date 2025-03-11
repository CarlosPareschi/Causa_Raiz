# agents/agent0_validate.py
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def agent0_validate(text: str) -> bool:
    """
    Valida se o texto fornecido é uma descrição de acidente de trânsito.
    Retorna yes se for uma descrição válida, caso contrário, no.
    """
    system_message = (
        "You are an assistant specialized in validating traffic accident descriptions. "
        "Only respond with 'YES' if the provided text is a valid traffic accident description, "
        "which includes detailed information about vehicle collisions, road conditions, involvement of pedestrians, animals, or objects in the road, "
        "as well as any mention of property damage, injuries, or other relevant contextual details (such as location, time, or contributing factors). "
        "If the text does not clearly depict a traffic accident or includes unrelated content, respond with 'NO'."
    )

    user_message = f"Text: {text}\n\nIs this a valid traffic accident description? Answer with YES or NO."
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    response = openai.ChatCompletion.create(
        model="o3-mini",  # ou o modelo que preferir
        messages=messages,
        reasoning_effort="medium",
        max_completion_tokens=10000
    )
    
    result = response["choices"][0]["message"]["content"].strip().upper()
    return result == "YES"
