import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def agent5_suggest_cause(text: str) -> str:
    """
    Given the improved accident description, this agent asks the model to suggest a more specific cause
    in Brazilian Portuguese if the initial classification was "Outros".
    """
    system_message = (
        "You are a data science assistant specialized in analyzing road accident descriptions. "
        "The initial classification was 'Others', so please analyze the following improved text and "
        "suggest a more specific accident cause. Provide your answer in Brazilian Portuguese."
    )
    user_message = f"Improved Accident Description: {text}\n\nSuggest a more specific accident cause."
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # ou outro modelo de sua escolha
        messages=messages,
        temperature=0.3,
        max_tokens=100
    )
    
    result = response["choices"][0]["message"]["content"]
    return result.strip()
