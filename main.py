# ==============================
# 📊 ENCUESTA ITC 2025 - STREAMLIT
# ==============================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 🚦 CONFIG
# ==============================
st.set_page_config(layout="wide")

st.title("📊 Reporte gráfico de datos demográficos y áreas de oportunidad")
st.markdown("""
**Instituto Tecnológico de Colima 2025**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ==============================
# 📂 CARGA DESDE GOOGLE SHEETS
# ==============================
# Tu vínculo CSV PUBLICADO de Google Sheets
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ5dZVqZ9lFSPkPKG8Kd_FID_ACTUALIZA_ESTE_LINK/pub?output=csv"

df = pd.read_csv(url)

st.success("✅ Datos cargados correctamente desde Google Sheets")
st.write(f"Número de registros: {df.shape[0]}")
st.dataframe(df.head())

# ==============================
# 🔎 NORMALIZAR MUNICIPIO / INSTITUCIÓN
# ==============================

def normalizar_institucion(valor):
    valor = str(valor).lower()
    if "colima" in valor:
        return "Universidad de Colima"
    elif "ateneo" in valor:
        return "Colegio Ateneo"
    elif "ad" in valor or "adonai" in valor:
        return "Instituto Adonai"
    elif "isenco" in valor:
        return "ISENCO"
    elif "icep" in valor:
        return "ICEP"
    elif "tecnico" in valor:
        return "Universidad de Colima"
    elif "privada" in valor:
        return "Universidad Privada"
    elif "cetis" in valor or "cbtis" in valor or "cbta" in valor or "emsad" in valor or "tele" in valor or "cobaem" in valor:
        return "Bachillerato Profesionalizante"
    else:
        return valor.strip().capitalize()

def normalizar_municipio(valor):
    valor = str(valor).lower().strip()
    if "colima" in valor:
        return "Colima"
    elif "villa" in valor:
        return "Villa de Álvarez"
    elif "cuauhtemoc" in valor or "cuahutemoc" in valor:
        return "Cuauhtémoc"
    elif "comala" in valor or "cómala" in valor:
        return "Comala"
    elif "manzanillo" in valor:
        return "Manzanillo"
    elif "tecoman" in valor or "tecomán" in valor:
        return "Tecomán"
    elif "aquila" in valor:
        return "Aquila"
    elif "tonila" in valor:
        return "Tonila"
    else:
        return valor.capitalize()

if '¿De qué institución académica egresaste?' in df.columns:
    df['Institucion_Normalizada'] = df['¿De qué institución académica egresaste?'].apply(normalizar_institucion)

if 'Municipio donde vive actualmente' in df.columns:
    df['Municipio_Normalizado'] = df['Municipio donde vive actualmente'].apply(normalizar_municipio)

# ==============================
# 🔢 CONVERSIÓN DE RANGOS NUMÉRICOS
# ==============================

def convertir_rango(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "menos de" in valor:
        num = [float(s) for s in valor.split() if s.replace('.', '', 1).isdigit()]
        return num[0]/2 if num else np.nan
    if "a" in valor:
        partes = valor.split("a")
        try:
            minimo = float(partes[0].strip())
            maximo = float(partes[1].split()[0].strip())
            return (minimo + maximo)/2
        except:
            return np.nan
    if "más de" in valor or "mas de" in valor:
        return 23  # ejemplo para edad
    try:
        return float(valor)
    except:
        return np.nan

if 'Edad en años cumplidos' in df.columns:
    df['Edad_Num'] = df['Edad en años cumplidos'].apply(convertir_rango)

if '¿Cuál fue tu promedio de calificación del tercer año de bachillerato?' in df.columns:
    df['Promedio_Num'] = df['¿Cuál fue tu promedio de calificación del tercer año de bachillerato?'].apply(convertir_rango)

if '¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?' in df.columns:
    df['Tiempo_Desplazamiento_Num'] = df['¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?'].apply(convertir_rango)

if '¿Cuántas horas al día dedica a estudiar fuera del aula?' in df.columns:
    df['Tiempo_Estudio_Num'] = df['¿Cuántas horas al día dedica a estudiar fuera del aula?'].apply(convertir_rango)

if 'En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?' in df.columns:
    df['Triste_Num'] = df['En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?'].apply(convertir_rango)

# ==============================
# 🥧 DIAGRAMAS DE PASTEL
# ==============================

columnas_categoricas = [
    'Seleccione su sexo',
    'Municipio_Normalizado',
    'Institucion_Normalizada',
    '¿A qué carrera desea ingresar?',
    'En este momento, usted',
    '¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?',
    'Actualmente, ¿realiza trabajo remunerado?',
    '¿Quién lo ha apoyado económicamente en sus estudios previos?',
    '¿Cuenta con un lugar adecuado para estudiar en casa?',
    '¿Tengo acceso a internet y computadora en casa?',
    'En el último año, ¿ha acudido a consulta por atención psicológica?',
    '¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?'
]

for col in columnas_categoricas:
    if col not in df.columns:
        continue
    st.subheader(f"📊 Distribución: {col}")
    conteo = df[col].value_counts(dropna=False).reset_index()
    conteo.columns = ['Categoria', 'Conteo']

    fig, ax = plt.subplots()
    ax.pie(conteo['Conteo'], labels=conteo['Categoria'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ==============================
# ⚡ DATOS ATÍPICOS
# ==============================
columnas_continuas = [
    'Edad_Num',
    'Promedio_Num',
    'Tiempo_Desplazamiento_Num',
    'Tiempo_Estudio_Num',
    'Triste_Num'
]

for col in columnas_continuas:
    if col not in df.columns:
        continue

    st.subheader(f"🔍 Detección de Atípicos: {col}")
    datos = df[[col]].dropna()

    if datos.empty:
        continue

    Q1 = datos[col].quantile(0.25)
    Q3 = datos[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    mask = (datos[col] < lower) | (datos[col] > upper)
    outliers = datos[mask]

    if not outliers.empty:
        st.warning(f"⚠️ {len(outliers)} dato(s) atípico(s) encontrados:")
        st.dataframe(outliers)
    else:
        st.success("✅ Sin datos atípicos detectados.")
