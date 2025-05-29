import os
import streamlit as st
import base64
from openai import OpenAI

# ✅ Esto debe ser lo PRIMERO que usas de Streamlit
st.set_page_config(page_title="Análisis de Imagen", layout="centered", initial_sidebar_state="collapsed")

# ✅ Aquí va el BLOQUE DE ESTILO para aplicar la nueva interfaz
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

<style>
    html, body, .stApp {
        background-color: #fefefe;
        color: #1a1a1a !important;
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111 !important;
        font-weight: 700;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: white;
        color: #1a1a1a !important;
        border: 1px solid #dcdcdc;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    label, .stMarkdown, .st-expanderHeader {
        color: #222 !important;
        font-weight: 600;
    }

    .stButton>button {
        background-color: #0077b6 !important;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 10px 18px;
    }

    .stButton>button:hover {
        background-color: #023e8a !important;
    }

    .st-expander {
        border: 1px solid #eaeaea;
        border-radius: 8px;
        background-color: #fafafa;
    }

    .stFileUploader {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 8px;
    }

    .stAlert {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
        border-radius: 8px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ✅ A partir de aquí sigue tu app normalmente
st.title("🔍 Análisis de Imagen")
