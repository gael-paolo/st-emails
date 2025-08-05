# app.py

import streamlit as st
import google.generativeai as genai
import os

# --- Configuración de la API Key desde streamlit ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("❌ No se encontró 'GOOGLE_API_KEY' en st.secrets. Configúralo en Streamlit Cloud.")
    st.stop()

# Inicializa el modelo Gemini 2.0 Flash
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
except Exception as e:
    st.error(f"Error al cargar el modelo Gemini: {e}")
    st.stop()

# --- Configuración de la página ---
st.set_page_config(page_title="Asistente de e-mails", layout="centered")

st.markdown("""
<style>
textarea {
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

st.title("✉️ Asistente para Redacción de e-mails")
st.markdown("Genera correos profesionales a partir de un mensaje recibido e instrucciones.")

# --- Entradas del usuario ---
correo_recibido = st.text_area("📥 Correo recibido", height=300, max_chars=3000)
idea_respuesta = st.text_area("💡 Idea principal para la respuesta", height=150, max_chars=1000)

formalidad = st.selectbox("🎩 Nivel de formalidad", ["Alto", "Medio", "Bajo"])
detalle = st.selectbox("🧾 Nivel de detalle", ["Breve", "Medio", "Detallado"])
tono_emocional = st.selectbox("🎭 Tono emocional", ["Neutro", "Cortés", "Cercano", "Empático", "Firme"])

# --- Botón para generar respuesta ---
if st.button("Generar Respuesta"):
    if not correo_recibido.strip() or not idea_respuesta.strip():
        st.warning("Por favor, completa tanto el correo recibido como la idea para la respuesta.")
    else:
        with st.spinner("✍️ Generando la respuesta..."):
            prompt = f"""Actúa como un asistente de redacción profesional de correos electrónicos para la empresa TAIYO MOTORS.
Genera la respuesta en español de Latinoamérica, en primera persona del singular, como si la respuesta la enviara un individuo.

Correo recibido:
<<< {correo_recibido} >>>

Idea principal para la respuesta:
<<< {idea_respuesta} >>>

Parámetros seleccionados:
- Nivel de formalidad: {formalidad}
- Nivel de detalle: {detalle}
- Tono emocional: {tono_emocional}

Redacta la respuesta siguiendo estas reglas:
1. Usa el nivel de formalidad indicado.
2. Responde coherentemente con la idea principal.
3. Ajusta la longitud al nivel de detalle.
4. Refleja el tono emocional solicitado.

Formato:
- Inicia con un saludo breve.
- Responde con claridad y coherencia.
- Finaliza con una despedida adecuada.

Genera solo el texto del correo.
"""
            try:
                response = model.generate_content(prompt)
                st.success("✅ Respuesta generada correctamente:")
                st.text_area("📤 Respuesta generada", value=response.text, height=350)
            except Exception as e:
                st.error(f"Ocurrió un error al generar la respuesta: {e}")
