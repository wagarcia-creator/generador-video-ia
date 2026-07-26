import streamlit as st
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="Traductor y Voz IA", page_icon="🎙️", layout="wide")

st.title("🎙️ Tu Estudio de Narración IA")
st.write("Escribe tu guion en inglés, tradúcelo y genera una voz humana profesional para tus casos.")

# Barra lateral para configuraciones
with st.sidebar:
    st.header("🔑 Configuración")
    openai_key = st.text_input("Ingresa tu OpenAI API Key:", type="password")
    st.info("Obtén tu API Key en platform.openai.com/api-keys")
    
    st.markdown("---")
    # Selección de voz
    st.subheader("🗣️ Elige el tono de voz")
    voz_seleccionada = st.selectbox(
        "Voces disponibles:",
        ("onyx", "echo", "fable", "alloy", "nova", "shimmer"),
        help="Onyx y Echo son excelentes voces graves para misterio."
    )

# Área principal
guion_ingles = st.text_area(
    "1. Escribe tu guion en Inglés:", 
    placeholder="Ej: The case remained unsolved for 20 years, until one night...",
    height=150
)

col1, col2 = st.columns(2)

# Columna de Traducción
with col1:
    if st.button("🇺🇸 ➡️ 🇪🇸 Traducir Guion al Español Neutro"):
        if not openai_key:
            st.error("⚠️ Falta tu API Key de OpenAI.")
        elif not guion_ingles:
            st.warning("⚠️ Escribe el guion primero.")
        else:
            with st.spinner("Traduciendo como un experto..."):
                try:
                    client = OpenAI(api_key=openai_key)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Eres un narrador experto de misterio. Traduce este texto al español neutro manteniendo el tono de suspenso y documental."},
                            {"role": "user", "content": guion_ingles}
                        ]
                    )
                    st.session_state['traduccion'] = response.choices[0].message.content
                    st.success("¡Traducción lista!")
                except Exception as e:
                    st.error(f"Error: {e}")

guion_espanol = st.session_state.get('traduccion', "")

if guion_espanol:
    st.text_area("2. Guion en Español:", value=guion_espanol, height=150, disabled=True)

# Columna de Audio
with col2:
    if st.button("🎙️ Generar Pista de Audio"):
        if not openai_key:
            st.error("⚠️ Falta tu API Key de OpenAI.")
        elif not guion_espanol:
            st.warning("⚠️ Necesitas traducir un guion primero.")
        else:
            with st.spinner("Grabando voz... (esto es muy rápido)"):
                try:
                    client = OpenAI(api_key=openai_key)
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice=voz_seleccionada,
                        input=guion_espanol
                    )
                    
                    audio_path = "narracion.mp3"
                    response.stream_to_file(audio_path)
                    
                    st.success("¡Pista de audio lista para descargar!")
                    st.audio(audio_path)
                    
                    with open(audio_path, "rb") as file:
                        st.download_button(
                            label="📥 Descargar MP3",
                            data=file,
                            file_name="narracion_caso.mp3",
                            mime="audio/mp3",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"Error: {e}")
