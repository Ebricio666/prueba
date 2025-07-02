import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ================================
# TÍTULO Y CREDITAUTORES
# ================================
st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ================================
# ✅ USA EL VÍNCULO CORRECTO
# ================================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"

try:
    df = pd.read_csv(url)
    st.success("✅ Datos cargados correctamente")
    st.dataframe(df.head())
except Exception as e:
    st.error(f"❌ No se pudo cargar el CSV.\n\nVerifica la URL y los permisos.\n\nError: {e}")

# ================================
# NORMALIZA EJEMPLO
# ================================
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
        elif 'cetis' in val or 'cbtis' in val:
            return 'Bachillerato profesionalizante'
        else:
            return 'Otro'
    df['Institucion_Normalizada'] = df['¿De qué institución académica egresaste?'].apply(normalizar_institucion)

# ================================
# GRÁFICA DE PASTEL
# ================================
if 'Institucion_Normalizada' in df.columns:
    conteo = df['Institucion_Normalizada'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(conteo, labels=conteo.index, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

# ================================
# DETECTAR OUTLIERS
# ================================
if 'Edad en años cumplidos' in df.columns:
    df['Edad_Num'] = df['Edad en años cumplidos'].apply(lambda x: float(x) if str(x).isdigit() else np.nan)
    Q1 = df['Edad_Num'].quantile(0.25)
    Q3 = df['Edad_Num'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df['Edad_Num'] < lower) | (df['Edad_Num'] > upper)]
    if not outliers.empty:
        st.warning(f"⚠️ {len(outliers)} outliers detectados:")
        st.dataframe(outliers)
    else:
        st.success("✅ No se encontraron datos atípicos.")
