# ===============================================
# 📌 app.py - Reporte gráfico ITColima 2025
# ===============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from fpdf import FPDF

# -----------------------------------------------
# 📌 CONFIGURACIÓN GENERAL
# -----------------------------------------------
st.set_page_config(layout="wide")
st.title("📊 Reporte gráfico de datos demográficos y áreas de oportunidad")
st.markdown("""
**Instituto Tecnológico de Colima 2025**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# -----------------------------------------------
# 📌 CARGAR DATOS
# -----------------------------------------------
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)
st.success("✅ Datos cargados desde Google Sheets")
st.dataframe(df.head())

# -----------------------------------------------
# 📌 FUNCIONES PARA NORMALIZAR RANGOS
# -----------------------------------------------
def convertir_rango(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "más de" in valor or "mayor" in valor:
        return 23
    if "menos de" in valor:
        nums = re.findall(r'\d+\.?\d*', valor)
        return float(nums[0])/2 if nums else np.nan
    if "a" in valor:
        nums = re.findall(r'\d+\.?\d*', valor)
        if len(nums) >= 2:
            minimo = float(nums[0])
            maximo = float(nums[1])
            return (minimo + maximo) / 2
        else:
            return np.nan
    nums = re.findall(r'\d+\.?\d*', valor)
    return float(nums[0]) if nums else np.nan

# -----------------------------------------------
# 📌 APLICAR CONVERSIÓN A COLUMNAS CLAVE
# -----------------------------------------------
df["Edad_Num"] = df["Edad en años cumplidos"].apply(convertir_rango)
df["Desplazamiento_Num"] = df["¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?"].apply(convertir_rango)
df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango)
df["Horas_Estudio_Num"] = df["¿Cuántas horas al día dedica a estudiar fuera del aula?"].apply(convertir_rango)
df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango)

# -----------------------------------------------
# 📌 FUNCIONES PARA DETECCIÓN DE ATÍPICOS
# -----------------------------------------------
def detectar_outliers(df, col):
    datos = df[col].dropna()
    Q1 = datos.quantile(0.25)
    Q3 = datos.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    return outliers, lower, upper

# -----------------------------------------------
# 📌 MOSTRAR OUTLIERS
# -----------------------------------------------
st.subheader("🔎 Datos Atípicos")
columnas = ["Edad_Num", "Desplazamiento_Num", "Promedio_Num", "Horas_Estudio_Num", "Triste_Num"]
outliers_total = pd.DataFrame()

for col in columnas:
    outliers, lower, upper = detectar_outliers(df, col)
    st.write(f"**{col}**: rango aceptable [{lower:.2f}, {upper:.2f}]")
    if not outliers.empty:
        st.dataframe(outliers)
        outliers_total = pd.concat([outliers_total, outliers])

# -----------------------------------------------
# 📌 GRÁFICAS DE PASTEL
# -----------------------------------------------
st.subheader("🥧 Diagramas de Pastel")
columnas_categoricas = [
    "Seleccione su sexo",
    "¿A qué carrera desea ingresar?",
    "Municipio donde vive actualmente",
    "¿De qué institución académica egresaste?",
    "Actualmente, ¿realiza trabajo remunerado?",
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?"
]

for col in columnas_categoricas:
    if col in df.columns:
        conteo = df[col].value_counts()
        fig, ax = plt.subplots()
        ax.pie(conteo, labels=conteo.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# -----------------------------------------------
# 📌 BOTÓN EXPORTAR A PDF
# -----------------------------------------------
if st.button("📄 Exportar Reporte PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte gráfico ITColima 2025", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, "Datos atípicos detectados:\n")
    for col in columnas:
        outliers, _, _ = detectar_outliers(df, col)
        if not outliers.empty:
            pdf.cell(0, 8, f"{col}:", ln=True)
            for index, row in outliers.iterrows():
                pdf.cell(0, 8, f" - Fila {index+1}: {row[col]}", ln=True)

    pdf.output("reporte_ITColima.pdf")
    st.success("✅ Reporte PDF generado: **reporte_ITColima.pdf**")
