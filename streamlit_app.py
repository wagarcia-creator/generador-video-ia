import os
import sys

# Forzar la instalación de replicate si no está presente
try:
    import replicate
except ImportError:
    os.system(f"{sys.executable} -m pip install replicate")
    import replicate

import streamlit as st

# Configuración principal de la interfaz
st.set_page_config(page_title="Mi Generador de Video IA", page_icon="🎬", layout="wide")

st.title("🎬 Tu Generador Personal de Video por IA")
st.write("Escribe una idea en texto y la IA creará las escenas en video.")

# Barra lateral para ingresar tu clave secreta de API
with st.sidebar:
    st.header("🔑 Configuración")
    api_token = st.text_input("Ingresa tu API Token de Replicate:", type="password")
    st.info("Obtén tu token en replicate.com/account/api-tokens")

# Área de texto para la idea del usuario
prompt_usuario = st.text_area(
    "Escribe la idea para tu video:", 
    placeholder="Ej: Un coche deportivo del futuro conduciendo por una ciudad de noche con luces neón...",
    height=120
)

# Botón principal
if st.button("🚀 Generar Video"):
    if not api_token:
        st.error("⚠️ Por favor ingresa tu API Token de Replicate en la barra lateral izquierda.")
    elif not prompt_usuario:
        st.warning("⚠️ Escribe una idea antes de generar.")
    else:
        try:
            client = replicate.Client(api_token=api_token)
            st.info("🧠 Procesando tu prompt y conectando con los servidores de video...")
            
            with st.spinner("Generando clip de video con IA... (esto toma entre 1 y 2 minutos)"):
                output = client.run(
                    "minimax/video-01",
                    input={
                        "prompt": prompt_usuario,
                        "prompt_optimizer": True
                    }
                )
                
                st.success("¡Tu video está listo!")
                st.video(output)
                
        except Exception as e:
            st.error(f"Ocurrió un error al procesar el video: {str(e)}")
