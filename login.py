import streamlit as st

# Usuarios válidos
USUARIOS = {
    "admin": "1234",
    "eduin": "colombia"
}

def login():
    st.sidebar.subheader("🔐 Iniciar sesión")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if username in USUARIOS and USUARIOS[username] == password:
        st.sidebar.success("✅ Autenticado")
        return True
    elif username and password:
        st.sidebar.error("❌ Usuario o contraseña incorrectos")
    return False
