import streamlit as st
from openai import OpenAI

# Configuración de la página
st.set_page_config(page_title="Estudio de Narración IA", page_icon="🎙️", layout="wide")

st.title("🎙️ Tu Estudio de Narración IA")
st.write("Genera narraciones de alta calidad en inglés y español para tus documentales de misterio.")

# Barra lateral
with st.sidebar:
    st.header("🔑 Configuración")
    openai_key = st.text_input("Ingresa tu OpenAI API Key:", type="password")
    st.info("Recarga saldo y obtén tu API Key en platform.openai.com")
    
    st.markdown("---")
    st.subheader("🗣️ Elige el tono de voz")
    voz_seleccionada = st.selectbox(
        "Voces disponibles:",
        ("onyx", "echo", "fable", "alloy", "nova", "shimmer"),
        help="Onyx y Echo son excelentes voces graves para misterio."
    )

# Área principal
guion_ingles = st.text_area(
    "1. Escribe tu guion en Inglés:", 
    placeholder="Ej: The evidence was hidden for decades...",
    height=150
)

col1, col2 = st.columns(2)

# Columna Izquierda: Acciones en Inglés y Traducción
with col1:
    # Botón para audio en Inglés
    if st.button("🎙️ Generar Audio (Inglés)"):
        if not openai_key:
            st.error("⚠️ Falta tu API Key de OpenAI.")
        elif not guion_ingles:
            st.warning("⚠️ Escribe el guion primero.")
        else:
            with st.spinner("Grabando voz en inglés..."):
                try:
                    client = OpenAI(api_key=openai_key)
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice=voz_seleccionada,
                        input=guion_ingles
                    )
                    audio_path_en = "narracion_en.mp3"
                    response.stream_to_file(audio_path_en)
                    st.success("¡Audio en inglés listo!")
                    st.audio(audio_path_en)
                    with open(audio_path_en, "rb") as file:
                        st.download_button(label="📥 Descargar MP3 (Inglés)", data=file, file_name="narracion_ingles.mp3", mime="audio/mp3")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    
    # Botón para traducir
    if st.button("🇺🇸 ➡️ 🇪🇸 Traducir Guion al Español Neutro"):
        if not openai_key:
            st.error("⚠️ Falta tu API Key.")
        elif not guion_ingles:
            st.warning("⚠️ Escribe el guion primero.")
        else:
            with st.spinner("Traduciendo como un experto documental..."):
                try:
                    client = OpenAI(api_key=openai_key)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Eres un narrador experto de misterio. Traduce este texto al español neutro manteniendo el tono de suspenso documental."},
                            {"role": "user", "content": guion_ingles}
                        ]
                    )
                    st.session_state['traduccion'] = response.choices[0].message.content
                except Exception as e:
                    st.error(f"Error: {e}")

# Columna Derecha: Resultado en Español y su Audio
with col2:
    guion_espanol = st.session_state.get('traduccion', "")
    st.text_area("2. Guion en Español:", value=guion_espanol, height=150, disabled=True)
    
    if guion_espanol:
        if st.button("🎙️ Generar Audio (Español)"):
            with st.spinner("Grabando voz en español..."):
                try:
                    client = OpenAI(api_key=openai_key)
                    response = client.audio.speech.create(
                        model="tts-1",
                        voice=voz_seleccionada,
                        input=guion_espanol
                    )
                    audio_path_es = "narracion_es.mp3"
                    response.stream_to_file(audio_path_es)
                    st.success("¡Audio en español listo!")
                    st.audio(audio_path_es)
                    with open(audio_path_es, "rb") as file:
                        st.download_button(label="📥 Descargar MP3 (Español)", data=file, file_name="narracion_espanol.mp3", mime="audio/mp3")
                except Exception as e:
                    st.error(f"Error: {e}")
