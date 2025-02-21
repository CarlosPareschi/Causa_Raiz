# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
