import os
import streamlit as st
import base64
from openai import OpenAI

# ✅ 1. Esto debe ir primero SIEMPRE
st.set_page_config(page_title="Análisis de Imagen", layout="centered", initial_sidebar_state="collapsed")

# ✅ 2. Luego, aplicamos el estilo personalizado
st.markdown("""
    <style>
        body {
            background-color: white !important;
            color: #1a1a1a;
            font-family: 'Segoe UI', sans-serif;
        }
        .stApp {
            background-color: white;
        }
        h1, h2, h3, h4 {
            color: #111;
            font-weight: 700;
        }
        label, .stTextInput > div > div > input {
            font-weight: 600;
            color: #222;
        }
        .stTextInput input, .stTextArea textarea {
            border: 1px solid #cccccc;
            border-radius: 8px;
            padding: 10px;
            background-color: #f9f9f9;
        }
        button[kind="secondary"] {
            background-color: #005f73 !important;
            color: white !important;
            border-radius: 8px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #0a9396 !important;
            color: #fff;
        }
        .st-expanderHeader {
            font-weight: 600;
            color: #444;
        }
        .stSpinner > div > div {
            color: #005f73;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ 3. Título
st.title("🔍 Análisis de Imagen")

# ✅ 4. Clave API
ke = st.text_input('🔑 Ingresa tu clave de OpenAI')
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

# ✅ 5. Inicializar cliente
client = OpenAI(api_key=api_key)

# ✅ 6. Subir imagen
uploaded_file = st.file_uploader("📁 Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("📸 Vista previa de la imagen", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# ✅ 7. Detalles opcionales
show_details = st.toggle("✏️ Adicionar detalles sobre la imagen", value=False)
if show_details:
    additional_details = st.text_area("🗒️ Contexto adicional:", disabled=not show_details)

# ✅ 8. Botón de análisis
analyze_button = st.button("🚀 Analiza la imagen", type="secondary")

# ✅ 9. Función para codificar imagen
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# ✅ 10. Análisis
if uploaded_file is not None and api_key and analyze_button:
    with st.spinner("🧠 Analizando imagen..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe lo que ves en la imagen en español"
        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado:\n{additional_details}"
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
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
        st.warning("⚠️ Ingresa tu clave de API.")

