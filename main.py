# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# 📌 CONFIG
# ===============================
st.set_page_config(layout="wide")

st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ===============================
# ✅ LEER GOOGLE SHEETS EN CSV
# ===============================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"

try:
    df = pd.read_csv(url)
    st.success("✅ Datos cargados correctamente desde Google Sheets")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ Error al cargar CSV: {e}")
    st.stop()

# ===============================
# ✅ NORMALIZAR INSTITUCIÓN
# ===============================
if '¿De qué institución académica egresaste?' in df.columns:
    def normalizar_institucion(val):
        val = str(val).lower().strip()
        if 'colima' in val:
            return 'Universidad de Colima'
        elif 'ateneo' in val:
            return 'Colegio Ateneo'
        elif 'adonai' in val:
            return 'Instituto Adonai'
        elif 'icep' in val:
            return 'ICEP'
        elif 'isenco' in val:
            return 'ISENCO'
        elif 'cetis' in val or 'cbtis' in val or 'cbta' in val:
            return 'Bachillerato profesionalizante'
        else:
            return 'Otro'
    df['Institucion_Normalizada'] = df['¿De qué institución académica egresaste?'].apply(normalizar_institucion)

# ===============================
# ✅ NORMALIZAR MUNICIPIO
# ===============================
if 'Municipio donde vive actualmente' in df.columns:
    def normalizar_municipio(val):
        val = str(val).lower().strip()
        if 'villa' in val:
            return 'Villa de Álvarez'
        elif 'colima' in val:
            return 'Colima'
        elif 'manzanillo' in val:
            return 'Manzanillo'
        elif 'coquimatlan' in val:
            return 'Coquimatlán'
        elif 'cuauhtemoc' in val or 'cuahutemoc' in val:
            return 'Cuauhtémoc'
        elif 'comala' in val:
            return 'Comala'
        elif 'tecoman' in val:
            return 'Tecomán'
        elif 'aquila' in val:
            return 'Aquila'
        else:
            return 'Otro'
    df['Municipio_Normalizado'] = df['Municipio donde vive actualmente'].apply(normalizar_municipio)

# ===============================
# ✅ VALIDAR ENCABEZADOS
# ===============================
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
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "¿Cuántas horas al día dedica a estudiar fuera del aula?",
    "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?",
    "En el último año, ¿ha acudido a consulta por atención psicológica?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?"
]

headers = df.columns.tolist()
faltantes = [col for col in encabezados_esperados if col not in headers]

st.subheader("📌 Encabezados detectados:")
st.write(headers)

if faltantes:
    st.warning("⚠️ Encabezados faltantes:")
    for col in faltantes:
        st.write(f"- {col}")
else:
    st.success("✅ Todos los encabezados esperados están presentes.")

# ===============================
# ✅ FUNCIONES DE CONVERSIÓN
# ===============================
def convertir_edad(valor):
    if pd.isna(valor): return np.nan
    valor = str(valor).lower().strip()
    if "más de" in valor: return 23
    try: return float(valor)
    except: return np.nan

def convertir_rango_promedio(valor):
    if pd.isna(valor): return np.nan
    if isinstance(valor, (int, float)): return valor
    if "a" in str(valor):
        partes = str(valor).split("a")
        try: return (float(partes[0].strip()) + float(partes[1].strip())) / 2
        except: return np.nan
    try: return float(valor)
    except: return np.nan

def convertir_rango_tiempo(valor):
    if pd.isna(valor): return np.nan
    valor = str(valor).lower()
    if "menos de" in valor:
        num = [int(s) for s in valor.split() if s.isdigit()]
        return num[0]/2 if num else np.nan
    elif "de" in valor and "a" in valor:
        partes = valor.replace("min", "").split("a")
        try: return (int(partes[0].split()[-1].strip()) + int(partes[1].strip())) / 2
        except: return np.nan
    else: return np.nan

def convertir_rango_general(valor):
    if pd.isna(valor): return np.nan
    valor = str(valor).lower()
    if "ninguna" in valor: return 0
    if "menos de" in valor:
        num = [float(s) for s in valor.split() if s.replace('.', '', 1).isdigit()]
        return num[0]/2 if num else np.nan
    if "a" in valor:
        partes = valor.split("a")
        try: return (float(partes[0].strip()) + float(partes[1].strip())) / 2
        except: return np.nan
    try: return float(valor)
    except: return np.nan

# ===============================
# ✅ APLICAR CONVERSIONES
# ===============================
if "Edad en años cumplidos" in df.columns:
    df["Edad_Num"] = df["Edad en años cumplidos"].apply(convertir_edad)

if "¿Cuál fue tu promedio de calificación del tercer año de bachillerato?" in df.columns:
    df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango_promedio)

if "¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?" in df.columns:
    df["Tiempo_Desplazamiento_Num"] = df["¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?"].apply(convertir_rango_tiempo)

if "¿Cuántas horas al día dedica a estudiar fuera del aula?" in df.columns:
    df["Horas_Estudio_Num"] = df["¿Cuántas horas al día dedica a estudiar fuera del aula?"].apply(convertir_rango_general)

if "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?" in df.columns:
    df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango_general)

# ===============================
# ✅ GRÁFICAS DE PASTEL
# ===============================
columnas_categoricas = [
    'Seleccione su sexo',
    'Municipio_Normalizado',
    'Institucion_Normalizada',
    '¿A qué carrera desea ingresar?'
]

for col in columnas_categoricas:
    if col not in df.columns:
        continue

    st.markdown(f"### 📊 Distribución: {col}")
    conteo = df[col].value_counts().reset_index()
    conteo.columns = ['Categoria', 'Conteo']  # CORREGIDO

    fig, ax = plt.subplots()
    ax.pie(conteo['Conteo'], labels=conteo['Categoria'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ===============================
# ✅ OUTLIERS
# ===============================
columnas_continuas = [
    'Edad_Num', 'Promedio_Num', 'Tiempo_Desplazamiento_Num', 'Horas_Estudio_Num', 'Triste_Num'
]

for col in columnas_continuas:
    if col not in df.columns:
        continue

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]
    st.markdown(f"### 🧩 Datos atípicos: {col}")
    if not outliers.empty:
        st.warning(f"⚠️ Se encontraron {len(outliers)} datos atípicos.")
        st.dataframe(outliers)
    else:
        st.success("✅ Sin datos atípicos.")
