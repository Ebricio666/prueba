# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ==========================
# TÍTULO Y LEYENDA
# ==========================
st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025

**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ==========================
# URL DE GOOGLE SHEETS
# ==========================
# Asegúrate de usar tu URL publicada correctamente como CSV
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTv7vibXy0mBSYxxxxxx/pub?output=csv"
df = pd.read_csv(url)

st.success("✅ Datos cargados correctamente desde Google Sheets.")
st.dataframe(df.head())

# ==========================
# NORMALIZAR INSTITUCIÓN
# ==========================
def normalizar_institucion(valor):
    valor = str(valor).lower().strip()
    if 'colima' in valor:
        return "Universidad de Colima"
    elif 'ateneo' in valor:
        return "Colegio Ateneo"
    elif 'adonia' in valor or 'adonai' in valor:
        return "Instituto Adonai"
    elif 'icep' in valor:
        return "ICEP"
    elif 'isenco' in valor:
        return "ISENCO"
    elif 'cbtis' in valor or 'cetis' in valor:
        return "Bachillerato profesionalizante"
    elif 'tecnico' in valor:
        return "Universidad de Colima"
    elif 'univa' in valor or 'tec' in valor or 'privada' in valor:
        return "Universidad Privada"
    else:
        return "Otro"

df['Institucion_Normalizada'] = df['¿De qué institución académica egresaste?'].apply(normalizar_institucion)

# ==========================
# NORMALIZAR MUNICIPIO
# ==========================
def normalizar_municipio(valor):
    valor = str(valor).lower().strip()
    if 'villa' in valor:
        return "Villa de Álvarez"
    elif 'colima' in valor:
        return "Colima"
    elif 'coquimatlan' in valor:
        return "Coquimatlán"
    elif 'cuauhtemoc' in valor or 'cuahutemoc' in valor:
        return "Cuauhtémoc"
    elif 'manzanillo' in valor:
        return "Manzanillo"
    elif 'tecoman' in valor:
        return "Tecomán"
    elif 'comala' in valor:
        return "Comala"
    elif 'aquila' in valor:
        return "Aquila"
    elif 'tonila' in valor:
        return "Tonila"
    else:
        return "Otro"

df['Municipio_Normalizado'] = df['Municipio donde vive actualmente'].apply(normalizar_municipio)

# ==========================
# CONVERSIÓN DE VARIABLES NUMÉRICAS
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

df["Edad_Num"] = df["Edad en años cumplidos"].apply(convertir_edad)

# ==========================
# DIAGRAMAS DE PASTEL
# ==========================
st.markdown("## 📊 Distribución de Instituciones y Municipios (Normalizados)")

columnas_categoricas = ['Institucion_Normalizada', 'Municipio_Normalizado']

for col in columnas_categoricas:
    st.markdown(f"### 🥧 {col}")
    conteo = df[col].value_counts().reset_index()
    value_col = conteo.columns[0]
    count_col = conteo.columns[1]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(conteo[count_col], labels=conteo[value_col], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ==========================
# ANÁLISIS DE DATOS ATÍPICOS
# ==========================
st.markdown("## 🔍 Detección de Datos Atípicos")

columnas_numericas = ['Edad_Num']

for col in columnas_numericas:
    if col not in df.columns:
        continue

    data = df[col].dropna()
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    st.markdown(f"### 📌 {col}")
    if outliers.empty:
        st.success(f"✅ No se encontraron datos atípicos en {col}.")
    else:
        st.warning(f"⚠️ Se encontraron {len(outliers)} datos atípicos en {col}:")
        st.dataframe(outliers[[col]])

st.success("🔗 Análisis completado correctamente.")
