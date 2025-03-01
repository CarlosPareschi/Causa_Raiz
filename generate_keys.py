import pickle
from pathlib import Path
import streamlit_authenticator as stauth

# Cria um dicionário com a estrutura esperada:
credentials = {
    "usernames": {
        "Cecilia": {"password": "XXX"},
        "Charles": {"password": "XXX"}
    }
}

# Gera os hashes usando o método estático hash_passwords()
hashed_credentials = stauth.Hasher.hash_passwords(credentials)

# Opcional: extraia somente os hashes se precisar de uma lista, por exemplo:
hashed_passwords = {
    username: details["password"] for username, details in hashed_credentials["usernames"].items()
}

# Salva os hashes em um arquivo pickle
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

print("Hashes gerados com sucesso!")
