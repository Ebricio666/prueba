# ============================================
# 📌 IMPORTS
# ============================================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# ============================================
# 📌 CONFIG INICIAL
# ============================================
st.set_page_config(layout="wide")
st.title("📊 Reporte gráfico de datos demográficos y áreas de oportunidad")
st.markdown("""
**Instituto Tecnológico de Colima 2025**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ============================================
# 📌 CARGAR DATOS
# ============================================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)

st.success("✅ Datos cargados correctamente")
st.dataframe(df.head())

# ============================================
# 📌 AGRUPAR MUNICIPIOS: Top 13 + Otros
# ============================================
municipios_top = df['Municipio donde vive actualmente'].value_counts().nlargest(13).index.tolist()

def agrupar_municipio(x):
    if pd.isna(x):
        return "Otros"
    x = str(x).strip()
    return x if x in municipios_top else "Otros"

df["Municipio Agrupado"] = df["Municipio donde vive actualmente"].apply(agrupar_municipio)

# ============================================
# 📌 AGRUPAR BACHILLERATOS: Top 4 + Otros
# ============================================
bachilleratos_top = df['¿De qué institución académica egresaste?'].value_counts().nlargest(4).index.tolist()

def agrupar_bachillerato(x):
    if pd.isna(x):
        return "Otros"
    x = str(x).strip()
    return x if x in bachilleratos_top else "Otros"

df["Bachillerato Agrupado"] = df["¿De qué institución académica egresaste?"].apply(agrupar_bachillerato)

# ============================================
# 📌 FUNCIONES PARA CONVERTIR RANGOS
# ============================================
def convertir_rango(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "más de" in valor or "mayor" in valor:
        return 23
    if "menos de" in valor:
        return 1
    if "a" in valor:
        partes = valor.replace("min", "").split("a")
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

# ============================================
# 📌 APLICAR CONVERSIONES A VARIABLES NUMÉRICAS
# ============================================
df["Edad_Num"] = df["Edad en años cumplidos"].apply(convertir_rango)
df["Desplazamiento_Num"] = df["¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?"].apply(convertir_rango)
df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango)
df["Horas_Estudio_Num"] = df["¿Cuántas horas al día dedica a estudiar fuera del aula?"].apply(convertir_rango)
df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango)

# ============================================
# 📌 DIAGRAMAS DE PASTEL CON LEYENDA LIMPIA
# ============================================
st.header("🥧 Diagramas de Pastel")

columnas_categoricas = [
    "Seleccione su sexo",
    "¿A qué carrera desea ingresar?",
    "Municipio Agrupado",
    "Bachillerato Agrupado",
    "Actualmente, ¿realiza trabajo remunerado?",
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?"
]

for col in columnas_categoricas:
    if col in df.columns:
        conteo = df[col].value_counts().sort_index()
        total = conteo.sum()
        sizes = conteo.values
        categorias = conteo.index.tolist()

        # Título claro antes del gráfico
        st.subheader(f"📌 {col}")

        fig, ax = plt.subplots(figsize=(7, 7))
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=None,  # Sin texto dentro
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10},
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )

        ax.axis('equal')
        ax.set_title(col, fontsize=14)

        # Leyenda con categoría + cantidad
        legend_labels = [f"{cat} ({num})" for cat, num in zip(categorias, sizes)]
        ax.legend(
            wedges,
            legend_labels,
            title="Categorías",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=10
        )

        st.pyplot(fig)

# ============================================
# 📌 DETECCIÓN DE DATOS ATÍPICOS
# ============================================
st.header("📊 Detección de Datos Atípicos")

columnas_numericas = ["Edad_Num", "Desplazamiento_Num", "Promedio_Num", "Horas_Estudio_Num", "Triste_Num"]

for col in columnas_numericas:
    datos = df[col].dropna()
    Q1 = datos.quantile(0.25)
    Q3 = datos.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    st.subheader(f"Datos Atípicos: {col}")
    if not outliers.empty:
        st.dataframe(outliers)
    else:
        st.success(f"No se encontraron datos atípicos en {col}")

# ============================================
# 📌 BOTÓN PARA EXPORTAR PDF BÁSICO
# ============================================
st.header("📄 Exportar Resumen a PDF")

if st.button("Generar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="📊 Reporte ITColima 2025", ln=True, align='C')

    pdf.multi_cell(0, 10, "Este PDF es un resumen con:\n"
                          "- Top 13 Municipios + Otros\n"
                          "- Top 4 Bachilleratos + Otros\n"
                          "- Diagramas de pastel con título y leyenda.\n"
                          "- Tabla de datos atípicos por variable numérica.")

    pdf.output("reporte_ITColima.pdf")
    st.success("✅ PDF generado como 'reporte_ITColima.pdf'. Descárgalo desde tu carpeta local.")
