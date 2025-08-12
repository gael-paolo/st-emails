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

# --- Interfaz de usuario con Streamlit ---
st.set_page_config(page_title="Redactor de Correos - TAIYO MOTORS", layout="centered")
st.markdown("""
<style>
textarea {
  width: 100% !important;
}
</style>
""", unsafe_allow_html=True)


st.title("✉️ Asistente para redacción de Correos")
st.markdown("Redacta correos profesionales de forma automática. Elige entre crear un correo nuevo desde cero o  responder a un correo recibido.")

# --- Creación de las pestañas con el orden corregido ---
tab1, tab2 = st.tabs(["Redactar un  Nuevo Correo", "Responder a Correo Recibido"])

with tab1:
    st.header("Redactar un nuevo correo")
    
    # Campos de entrada para redactar uno nuevo
    idea_nuevo_correo = st.text_area("💡 Describe brevemente tu idea para el nuevo correo", height=150, max_chars=3000, key="idea_nuevo")

    formalidad_nuevo = st.selectbox("🎩 Nivel de formalidad", ["Alto", "Medio", "Bajo"], key="formalidad_nuevo")
    detalle_nuevo = st.selectbox("🧾 Tamaño del correo", ["Breve", "Medio", "Detallado"], key="detalle_nuevo")
    tono_emocional_nuevo = st.selectbox("🎭 Tono emocional", ["Neutro", "Cortés", "Cercano", "Empático", "Firme", "Profesional"], key="tono_nuevo")

    # Botón para generar el nuevo correo
    if st.button("Generar Correo", key="btn_nuevo"):
        if not idea_nuevo_correo.strip():
            st.warning("Por favor, completa la idea para el correo.")
        else:
            with st.spinner("✍️ Generando el correo..."):
                prompt_nuevo = f"""Actúa como un asistente de redacción profesional de correos electrónicos para la empresa TAIYO MOTORS.
Genera un correo nuevo en español de Latinoamérica, en primera persona del singular.

Idea principal para el correo:
<<< {idea_nuevo_correo} >>>

Parámetros seleccionados:
- Nivel de formalidad: {formalidad_nuevo}
- Nivel de detalle: {detalle_nuevo}
- Tono emocional: {tono_emocional_nuevo}

Redacta el correo siguiendo estas reglas:
1. Usa el nivel de formalidad indicado.
2. Escribe coherentemente con la idea principal.
3. Ajusta la longitud al nivel de detalle.
4. Refleja el tono emocional solicitado.

Formato:
- Inicia con un saludo breve.
- Redacta el mensaje con claridad y coherencia.
- Finaliza con una despedida adecuada.

Genera solo el texto del correo.
"""
                try:
                    response = model.generate_content(prompt_nuevo)
                    st.success("✅ Correo generado correctamente:")
                    st.text_area("📤 Correo generado", value=response.text, height=350)
                except Exception as e:
                    st.error(f"Ocurrió un error al generar el correo: {e}")

with tab2:
    st.header("Responder a correo recibido")
    
    # Campos de entrada para responder
    correo_recibido = st.text_area("📥 Pega aquí el correo recibido", height=300, max_chars=3000, key="correo_recibido_resp")
    idea_respuesta = st.text_area("💡 Describe brevemente tu idea para el correo de respuesta", height=150, max_chars=1000, key="idea_respuesta_resp")

    formalidad = st.selectbox("🎩 Nivel de formalidad", ["Alto", "Medio", "Bajo"], key="formalidad_resp")
    detalle = st.selectbox("🧾 Tamaño del correo", ["Breve", "Medio", "Detallado"], key="detalle_resp")
    tono_emocional = st.selectbox("🎭 Tono emocional", ["Neutro", "Cortés", "Cercano", "Empático", "Firme", "Profesional"], key="tono_resp")

    # Botón para generar respuesta
    if st.button("Generar Respuesta", key="btn_resp"):
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