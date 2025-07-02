# ============================================
# 📌 app.py - Reporte Integral Instituto Tecnológico de Colima
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from fpdf import FPDF

# ============================================
# 📌 CONFIGURACIÓN Y TÍTULO
# ============================================
st.set_page_config(layout="wide")
st.markdown("""
# 📊 Reporte gráfico de datos demográficos y áreas de oportunidad 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ============================================
# 📌 CARGA DE DATOS
# ============================================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)
st.success("✅ Datos cargados correctamente.")
st.dataframe(df)

# ============================================
# 📌 AGRUPAR RESPUESTAS DE MUNICIPIOS Y ESCUELAS
# ============================================
def normalizar_municipio(valor):
    valor = str(valor).strip().lower()
    if "villa" in valor:
        return "Villa de Álvarez"
    if "colima" in valor:
        return "Colima"
    if "coquimatlan" in valor:
        return "Coquimatlán"
    if "comala" in valor:
        return "Comala"
    if "cuauhtemoc" in valor:
        return "Cuauhtémoc"
    if "manzanillo" in valor:
        return "Manzanillo"
    if "tecoman" in valor:
        return "Tecomán"
    if "aquila" in valor:
        return "Aquila"
    if "tonila" in valor:
        return "Tonila"
    return valor.title()

def normalizar_escuela(valor):
    valor = str(valor).strip().lower()
    if "universidad de colima" in valor:
        return "Bachillerato Técnico UdeC"
    if "cety" in valor or "cbtis" in valor:
        return "CETyS/CBTIS/Profesionalizante"
    if "isenco" in valor:
        return "ISENCO"
    if "privada" in valor:
        return "Privada"
    if "ateneo" in valor:
        return "Ateneo"
    return valor.title()

df["Municipio_Normalizado"] = df["Municipio donde vive actualmente"].apply(normalizar_municipio)
df["Escuela_Normalizada"] = df["¿De qué institución académica egresaste?"].apply(normalizar_escuela)

# ============================================
# 📌 GRÁFICAS DE PASTEL
# ============================================
columnas_pastel = [
    "Seleccione su sexo",
    "¿A qué carrera desea ingresar?",
    "Municipio_Normalizado",
    "Escuela_Normalizada"
]

st.subheader("### 🥧 Distribuciones Categóricas")

for col in columnas_pastel:
    conteo = df[col].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        conteo.values,
        labels=conteo.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    ax.set_title(f"{col}")
    st.pyplot(fig)

# ============================================
# 📌 DATOS ATÍPICOS Y TABLA RESUMEN
# ============================================

def convertir_rango(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "más de" in valor or "mayor" in valor:
        return 23
    if "menos de" in valor:
        num = [float(s) for s in valor.split() if s.replace('.', '', 1).isdigit()]
        return num[0]/2 if num else np.nan
    if "a" in valor:
        partes = valor.replace("min", "").split("a")
        minimo = float(partes[0].strip())
        maximo = float(partes[1].split()[0].strip())
        return (minimo + maximo) / 2
    try:
        return float(valor)
    except:
        return np.nan

# Variables numéricas clave
df["Edad_Num"] = df["Edad en años cumplidos"].apply(convertir_rango)
df["Desplazamiento_Num"] = df["¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?"].apply(convertir_rango)
df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango)
df["Horas_Estudio_Num"] = df["¿Cuántas horas al día dedica a estudiar fuera del aula?"].apply(convertir_rango)
df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango)

# Detectar atípicos
outliers = pd.DataFrame()
for col in ["Edad_Num", "Desplazamiento_Num", "Promedio_Num", "Horas_Estudio_Num", "Triste_Num"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    mask = (df[col] < lower) | (df[col] > upper)
    outliers = pd.concat([outliers, df[mask]])

outliers = outliers.drop_duplicates()

st.subheader("## 📌 Tabla de Datos Atípicos Detectados")
if not outliers.empty:
    st.dataframe(outliers)
    csv = outliers.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Datos Atípicos (CSV)", csv, "datos_atipicos.csv", "text/csv")
else:
    st.success("✅ No se encontraron datos atípicos.")

# ============================================
# 📌 BOTÓN EXPORTACIÓN PDF
# ============================================

def exportar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Reporte de Datos Atípicos", ln=True, align='C')

    pdf.set_font("Arial", size=8)
    for index, row in outliers.iterrows():
        pdf.multi_cell(0, 10, str(row.to_dict()), border=0)

    return pdf

if not outliers.empty:
    if st.button("📄 Exportar Datos Atípicos en PDF"):
        pdf = exportar_pdf()
        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button(
            label="📄 Descargar PDF",
            data=pdf_output,
            file_name="datos_atipicos.pdf",
            mime="application/pdf"
        )
