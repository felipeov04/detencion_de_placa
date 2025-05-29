import os
import streamlit as st
import base64
from openai import OpenAI

# ---------------- CONFIGURACIÓN DE PÁGINA ----------------
st.set_page_config(
    page_title="Análisis de Imagen",
    layout="centered",
    initial_sidebar_state="collapsed",
    theme={"base": "light"}  # Forzar tema claro
)

# ---------------- ESTILO PERSONALIZADO ----------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
    html, body, .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
    }

    h1 {
        font-weight: 700;
        color: #111;
        font-size: 2.4em;
        margin-bottom: 0.5em;
    }

    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }

    .stFileUploader {
        background-color: #fafafa;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px;
    }

    label, .stMarkdown, .st-expanderHeader {
        color: #111;
        font-weight: 600;
    }

    .stButton>button {
        background-color: #0077b6;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }

    .stButton>button:hover {
        background-color: #023e8a;
    }

    .st-expander {
        border-radius: 8px;
        background-color: #f9f9f9;
        border: 1px solid #e6e6e6;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCIONES ----------------
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ---------------- INTERFAZ ----------------
st.title("🔍 Análisis de Imagen")
ke = st.text_input('🔑 Ingresa tu Clave')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key)

uploaded_file = st.file_uploader("📁 Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("📸 Vista previa", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

show_details = st.toggle("📝 Adiciona detalles sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area(
        "🗒️ Contexto adicional:",
        disabled=not show_details
    )

analyze_button = st.button("🚀 Analiza la imagen")

# ---------------- PROCESAMIENTO ----------------
if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🧠 Analizando ..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = ("Describe lo que ves en la imagen en español")
        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado por el usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o", messages=messages,
                max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
else:
    if not uploaded_file and analyze_button:
        st.warning("⚠️ Por favor, sube una imagen.")
    if not api_key:
        st.warning("⚠️ Por favor ingresa tu API key.")
