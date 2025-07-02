# ================================================
# main.py - App Streamlit Completa
# ================================================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================================================
# Configuración
# ================================================
st.set_page_config(page_title="📊 Reporte Demográfico ITColima", layout="wide")
st.title("📊 Reporte gráfico de datos demográficos y áreas de oportunidad")
st.markdown("""
**Instituto Tecnológico de Colima 2025**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ================================================
# Carga de datos desde Google Sheets (CSV publicado)
# ================================================
# ⚠️ REEMPLAZA AQUÍ con tu enlace CSV publicado
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/edit?usp=sharing"

try:
    df = pd.read_csv(url)
    st.success(f"✅ Archivo cargado correctamente. Registros: {len(df)}")
except Exception as e:
    st.error(f"❌ Error al cargar el archivo CSV: {e}")
    st.stop()

st.dataframe(df.head())

# ================================================
# Normalización de columnas clave
# ================================================
def normalizar_institucion(v):
    v = str(v).lower()
    if "colima" in v:
        return "Universidad de Colima"
    elif "aten" in v:
        return "Colegio Ateneo"
    elif "adonai" in v:
        return "Instituto Adonai"
    elif "isenco" in v:
        return "ISENCO"
    elif "icep" in v:
        return "ICEP"
    elif "privada" in v:
        return "Universidad Privada"
    elif "cetis" in v or "cbtis" in v or "cbta" in v:
        return "Bachillerato Profesionalizante"
    else:
        return v.strip().capitalize()

def normalizar_municipio(v):
    v = str(v).lower()
    if "colima" in v:
        return "Colima"
    elif "villa" in v:
        return "Villa de Álvarez"
    elif "cuauhtemoc" in v or "cuahutemoc" in v:
        return "Cuauhtémoc"
    elif "comala" in v:
        return "Comala"
    elif "manzanillo" in v:
        return "Manzanillo"
    elif "tecoman" in v:
        return "Tecomán"
    elif "aquila" in v:
        return "Aquila"
    elif "tonila" in v:
        return "Tonila"
    else:
        return v.strip().capitalize()

df['Municipio_Normalizado'] = df['Municipio donde vive actualmente'].apply(normalizar_municipio)
df['Institucion_Normalizada'] = df['¿De qué institución académica egresaste?'].apply(normalizar_institucion)

# ================================================
# Conversión de rangos
# ================================================
def convertir_rango(v):
    if pd.isna(v): return np.nan
    v = str(v).lower()
    if "menos de" in v:
        nums = [float(s) for s in v.split() if s.replace('.', '', 1).isdigit()]
        return nums[0]/2 if nums else np.nan
    if "a" in v:
        try:
            partes = v.split("a")
            return (float(partes[0].strip()) + float(partes[1].split()[0].strip()))/2
        except: return np.nan
    if "más de" in v: return 23
    try: return float(v)
    except: return np.nan

df['Edad_Num'] = df['Edad en años cumplidos'].apply(convertir_rango)
df['Promedio_Num'] = df['¿Cuál fue tu promedio de calificación del tercer año de bachillerato?'].apply(convertir_rango)
df['Tiempo_Desplazamiento_Num'] = df['¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?'].apply(convertir_rango)
df['Tiempo_Estudio_Num'] = df['¿Cuántas horas al día dedica a estudiar fuera del aula?'].apply(convertir_rango)
df['Triste_Num'] = df['En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?'].apply(convertir_rango)

# ================================================
# Variables categóricas: Diagramas de pastel
# ================================================
st.header("🥧 Diagramas de pastel por variable")
columnas_pastel = [
    'Seleccione su sexo',
    'Municipio_Normalizado',
    'Institucion_Normalizada',
    '¿A qué carrera desea ingresar?',
    'En este momento, usted',
    '¿Quién lo ha apoyado económicamente en sus estudios previos?',
    '¿Tengo acceso a internet y computadora en casa?',
    '¿Cuenta con un lugar adecuado para estudiar en casa?',
    'En el último año, ¿ha acudido a consulta por atención psicológica?',
    '¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?'
]

for col in columnas_pastel:
    if col in df.columns:
        conteo = df[col].value_counts().reset_index()
        conteo.columns = ['Categoria', 'Conteo']
        fig, ax = plt.subplots()
        ax.pie(conteo['Conteo'], labels=conteo['Categoria'], autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Distribución: {col}")
        st.pyplot(fig)

# ================================================
# Variables continuas: Datos atípicos
# ================================================
st.header("📈 Detección de datos atípicos (Outliers)")
for col in ['Edad_Num', 'Promedio_Num', 'Tiempo_Desplazamiento_Num', 'Tiempo_Estudio_Num', 'Triste_Num']:
    datos = df[[col]].dropna()
    if datos.empty:
        continue
    Q1 = datos[col].quantile(0.25)
    Q3 = datos[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    outliers = datos[(datos[col]<lower)|(datos[col]>upper)]
    st.subheader(f"🔎 Outliers para {col}")
    if not outliers.empty:
        st.dataframe(outliers)
    else:
        st.success(f"✅ Sin datos atípicos en {col}")
