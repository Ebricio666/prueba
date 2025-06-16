import streamlit as st
import pandas as pd

st.title("Cuestionario de Ingreso para Estudiantes")

# Datos Demográficos
st.header("Datos Demográficos")
nombre = st.text_input("Nombre completo")
sexo = st.selectbox("Sexo", ["Femenino", "Masculino", "Otro"])
edad = st.number_input("Edad", min_value=15, max_value=100, step=1)
telefono_tutor = st.text_input("Número de contacto de tutor")
trabaja = st.selectbox("¿Actualmente trabaja?", ["No", "Diario", "Fin de semana"])
lugar_vive = st.text_input("Lugar donde actualmente vive")
tiempo_desplazo = st.text_input("¿Cuánto tiempo le toma llegar a la institución?")
vive_con = st.selectbox("¿Vive con?", ["Solo/a", "Familiares"])
bachillerato = st.text_input("¿De qué bachillerato egresaste?")
promedio_bachillerato = st.text_input("¿Cuál es tu promedio de calificación del tercer año de bachillerato?")

# Datos Clínicos
st.header("Datos Clínicos")
grupo_sanguineo = st.selectbox("Grupo sanguíneo", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-", "No sabe"])
alergias = st.text_area("¿Es alérgico a algún alimento o medicamento?")
padecimientos = st.text_area("¿Padece alguna enfermedad o síndrome?")

# Preguntas Adicionales
st.header("Preguntas Adicionales")
preguntas = [
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tiene acceso constante a internet y computadora?",
    "¿Cuántas horas al día puede dedicar al estudio fuera del aula?",
    "¿Cuál fue su promedio final en el último ciclo escolar?",
    "¿Se ha sentido triste o desmotivado frecuentemente en las últimas dos semanas?",
    "¿A quién acudiría si tuviera un problema emocional o académico?",
    "¿Ha recibido atención psicológica en el último año?",
    "¿Quién lo(a) apoya económicamente durante sus estudios?",
    "¿Cuenta con personas cercanas que lo(a) motivan a continuar con su carrera?",
    "¿Por qué eligió esta carrera?",
    "¿Qué espera lograr durante sus estudios universitarios?",
    "¿Cuáles cree que serán los principales retos que enfrentará?"
]

respuestas = [st.text_area(pregunta) for pregunta in preguntas]

# Botón para enviar
if st.button("Enviar"):
    st.success("¡Gracias por completar el formulario!")
    
    datos = {
        "Nombre": nombre,
        "Sexo": sexo,
        "Edad": edad,
        "Teléfono Tutor": telefono_tutor,
        "Trabaja": trabaja,
        "Lugar donde vive": lugar_vive,
        "Tiempo de desplazamiento": tiempo_desplazo,
        "Vive con": vive_con,
        "Bachillerato": bachillerato,
        "Promedio Bachillerato": promedio_bachillerato,
        "Grupo sanguíneo": grupo_sanguineo,
        "Alergias": alergias,
        "Padecimientos": padecimientos,
    }

    for i, pregunta in enumerate(preguntas):
        datos[pregunta] = respuestas[i]

    df = pd.DataFrame([datos])
    st.download_button(
        label="📥 Descargar respuestas en CSV",
        data=df.to_csv(index=False),
        file_name="respuestas_cuestionario.csv",
        mime="text/csv"
    )
