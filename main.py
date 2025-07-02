# app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

# ==========================
# TÍTULO E INFORMACIÓN
# ==========================
st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ==========================
# LEER CSV EN LÍNEA
# ==========================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)

st.success("✅ Datos cargados directamente desde Google Sheets.")
st.subheader("📊 Vista previa de los datos")
st.dataframe(df)

# ==========================
# VALIDAR ENCABEZADOS
# ==========================
headers = df.columns.tolist()
st.subheader("📌 Encabezados detectados:")
st.write(headers)

encabezados_esperados = [
    "Dirección de correo electrónico",
    "¿A qué carrera desea ingresar?",
    "Ingrese su nombre completo",
    "Seleccione su sexo",
    "Edad en años cumplidos",
    "Municipio donde vive actualmente",
    "En este momento, usted",
    "¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?",
    "Actualmente, ¿realiza trabajo remunerado?",
    "¿Quién lo ha apoyado económicamente en sus estudios previos?",
    "¿De qué institución académica egresaste?",
    "¿Cuál fue tu promedio de calificación del tercer año de bachillerato?",
    "Nombre y número de teléfono del tutor o persona de confianza a quien contactar en caso de emergencia",
    "Si tiene alguna alergia, escríbalo",
    "Si tiene alguna enfermedad o síndrome, escríbano",
    "Si conoce su grupo sanguíneo, escríbano",
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "¿Cuántas horas al día dedica a estudiar fuera del aula?",
    "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?",
    "En el último año, ¿ha acudido a consulta por atención psicológica?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?"
]

faltantes = [col for col in encabezados_esperados if col not in headers]
if faltantes:
    st.warning("⚠️ Encabezados faltantes:")
    for col in faltantes:
        st.write(f"- {col}")
else:
    st.success("✅ Todos los encabezados esperados están presentes.")

# ==========================
# EJEMPLO: CONVERSIÓN DE EDAD
# ==========================
def convertir_edad(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower().strip()
    if "más de" in valor or "mas de" in valor:
        return 23
    try:
        return float(valor)
    except:
        return np.nan

if "Edad en años cumplidos" in df.columns:
    df["Edad en años cumplidos"] = df["Edad en años cumplidos"].apply(convertir_edad)

st.subheader("📊 Datos con conversión de edad")
st.dataframe(df)

# ==========================
# CONTINÚA CON TU ANÁLISIS AQUÍ
# ==========================
# Puedes seguir con tus diagramas, boxplots, etc.
