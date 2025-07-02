# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Título e información institucional
st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ==========================
# VINCULO GOOGLE SHEETS CSV
# ==========================
url = "import pandas as pd
    
url = "https://docs.google.com/spreadsheets/d/e/<ID>/pub?output=csv"
df = pd.read_csv(url)
print(df.head())

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
# FUNCIONES DE CONVERSIÓN
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

def convertir_rango_promedio(valor):
    if pd.isna(valor):
        return np.nan
    if isinstance(valor, (int, float)):
        return valor
    if "a" in str(valor):
        partes = str(valor).split("a")
        try:
            minimo = float(partes[0].strip())
            maximo = float(partes[1].strip())
            return (minimo + maximo) / 2
        except:
            return np.nan
    try:
        return float(valor)
    except:
        return np.nan

def convertir_rango_tiempo_desplazamiento(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "menos de" in valor:
        try:
            num = [int(s) for s in valor.split() if s.isdigit()][0]
            return num / 2
        except:
            return np.nan
    elif "de" in valor and "a" in valor:
        partes = valor.replace("min", "").split("a")
        try:
            minimo = int(partes[0].split()[-1].strip())
            maximo = int(partes[1].strip())
            return (minimo + maximo) / 2
        except:
            return np.nan
    else:
        return np.nan

def convertir_rango_general(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "ninguna" in valor:
        return 0
    if "menos de" in valor:
        try:
            num = [float(s) for s in valor.split() if s.replace('.', '', 1).isdigit()][0]
            return num / 2
        except:
            return np.nan
    if "a" in valor:
        partes = valor.split("a")
        try:
            minimo = float(partes[0].strip())
            maximo = float(partes[1].split()[0].strip())
            return (minimo + maximo) / 2
        except:
            return np.nan
    try:
        return float(valor)
    except:
        return np.nan

# ==========================
# APLICAR CONVERSIONES
# ==========================
if "Edad en años cumplidos" in df.columns:
    df["Edad en años cumplidos"] = df["Edad en años cumplidos"].apply(convertir_edad)

if "¿Cuál fue tu promedio de calificación del tercer año de bachillerato?" in df.columns:
    df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango_promedio)

if "¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?" in df.columns:
    df["Tiempo_desplazamiento_Num"] = df["¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?"].apply(convertir_rango_tiempo_desplazamiento)

if "¿Cuántas horas al día dedica a estudiar fuera del aula?" in df.columns:
    df["Tiempo_Num"] = df["¿Cuántas horas al día dedica a estudiar fuera del aula?"].apply(convertir_rango_general)

if "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?" in df.columns:
    df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango_general)

# ==========================
# CONTINÚA CON TU ANÁLISIS...
# ==========================
# Tu bloque de pastel y outliers se queda igual
# ...
