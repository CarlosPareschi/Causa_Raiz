import streamlit_authenticator as stauth

# Gera hashes para senhas
senha_cecilia = "Cecilia"
senha_charles = "Charles"

hashed_passwords = stauth.Hasher([senha_cecilia, senha_charles]).generate()

print(f"Senha hasheada da Cecilia: {hashed_passwords[0]}")
print(f"Senha hasheada do Charles: {hashed_passwords[1]}")
