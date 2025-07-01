import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# Subir archivo
uploaded_file = st.file_uploader("📁 Sube el archivo Excel con los datos", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Verificar encabezados
    headers = df.columns.tolist()
    st.subheader("📌 Encabezados detectados:")
    st.write(headers)

    duplicados = df.columns[df.columns.duplicated()].unique().tolist()
    if duplicados:
        st.warning("⚠️ Encabezados duplicados encontrados:")
        for col in duplicados:
            st.write(f"- {col}")
    else:
        st.success("✅ No hay encabezados duplicados.")

    encabezados_esperados = [
        "Fecha",
        "Homoclave del docente",
        "Correo",
        "Carrera",
        "Nombre",
        "Sexo",
        "Edad",
        "Lugar donde vive",
        "¿Vive con?",
        "Tiempo de desplazamiento",
        "Trabaja",
        "¿Vive con?",  # ⚠️ Renombra si tienes duplicados
        "Bachillerato",
        "Promedio",
        "Tel de contacto",
        "Alergia",
        "Enfermedades",
        "Grupo sanguíneo",
        "Espacio para trabajar",
        "Acceso a internet y pc",
        "Tiempo estudio",
        "Triste",
        "Psicologo",
        "Apoyo carrera"
    ]

    faltantes = [col for col in encabezados_esperados if col not in headers]
    if faltantes:
        st.error("❌ Encabezados faltantes:")
        for col in faltantes:
            st.write(f"- {col}")
        st.stop()
    else:
        st.success("✅ Todos los encabezados esperados están presentes.")

    # ✅ TODOS pueden ver todos los datos
    df['Homoclave del docente'] = df['Homoclave del docente'].fillna("").astype(str)
    st.subheader("📊 Todos los datos cargados")
    st.dataframe(df)

    # 🔍 Búsqueda opcional por nombre
    nombre_cols = [col for col in df.columns if "Nombre" in col]
    if nombre_cols:
        nombre_col = nombre_cols[0]

        if st.radio("🔍 ¿Desea realizar una búsqueda personalizada?", ["No", "Sí"]) == "Sí":
            nombre_estudiante = st.text_input(f"Introduce el nombre del estudiante (columna '{nombre_col}')").strip()
            if nombre_estudiante:
                df_estudiante = df[
                    df[nombre_col].astype(str).str.lower().str.contains(nombre_estudiante.lower(), na=False)
                ]
                if df_estudiante.empty:
                    st.warning("⚠️ No se encontró al estudiante.")
                else:
                    st.subheader(f"🎓 Datos del estudiante: {nombre_estudiante}")
                    st.dataframe(df_estudiante)

    # ✅ FUNCION PARA CONVERTIR RANGO A PROMEDIO NUMÉRICO
    def convertir_rango_a_promedio(valor):
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, (int, float)):
            return valor
        if isinstance(valor, str) and "a" in valor:
            partes = valor.split("a")
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

    # ✅ Aplicar conversión
    if "Promedio" in df.columns:
        df["Promedio_Num"] = df["Promedio"].apply(convertir_rango_a_promedio)

    # Variables categóricas
    columnas_categoricas = [
        "Sexo",
        "Edad",
        "Carrera",
        "Lugar donde vive",
        "¿Vive con?",
        "Tiempo de desplazamiento",
        "Trabaja",
        "Bachillerato",
        "Promedio",
        "Espacio para trabajar",
        "Acceso a internet y pc",
        "Triste",
        "Psicologo",
        "Apoyo carrera"
    ]

    columnas_categoricas = list(dict.fromkeys(columnas_categoricas))  # Quitar duplicados

    for col in columnas_categoricas:
        if col not in df.columns:
            st.info(f"ℹ️ La columna '{col}' no se encontró en los datos. Se omite.")
            continue

        st.markdown(f"### 📊 Distribución: {col}")

        if col == 'Promedio':
            conteo = df[col].value_counts().sort_index()
        else:
            conteo = df[col].value_counts(dropna=False)

        porcentaje = (conteo / conteo.sum()) * 100
        categorias = porcentaje.index.tolist()

        fig, ax = plt.subplots(figsize=(10, 2))
        left = 0
        for cat in categorias:
            val = porcentaje[cat]
            n = conteo[cat]
            label = f"{cat} ({n})"
            ax.barh(0, val, left=left, label=label)
            left += val

        ax.set_xlim(0, 100)
        ax.set_xlabel('Porcentaje (%)')
        ax.set_yticks([])
        ax.legend(title='Respuesta', bbox_to_anchor=(1.02, 1), loc='upper left')
        st.pyplot(fig)

    # Variables continuas
    columnas_a_evaluar = [
        'Edad',
        'Promedio_Num',  # Usar columna numérica convertida
        'Tiempo estudio'
    ]

    for col in columnas_a_evaluar:
        if col not in df.columns:
            st.info(f"ℹ️ La columna '{col}' no se encontró en los datos. Se omite.")
            continue

        st.markdown(f"### 📈 Distribución de {col}")

        datos = df[[nombre_col, col]].dropna()

        if datos.empty:
            st.warning(f"⚠️ No hay datos disponibles para '{col}'.")
            continue

        Q1 = datos[col].quantile(0.25)
        Q3 = datos[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        if 'Edad' in col:
            bins = np.arange(17, 22, 2)
        elif 'Promedio' in col:
            bins = np.arange(6.0, 10.5, 0.5)
        else:
            bins = 10

        df.loc[:, 'Rango_' + col] = pd.cut(df[col], bins=bins)
        conteo_barras = df['Rango_' + col].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 4))
        conteo_barras.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel('Número de estudiantes')
        ax.set_xlabel('Rangos')
        ax.grid(axis='y')
        st.pyplot(fig)

        outliers = datos[(datos[col] < lower) | (datos[col] > upper)]
        if not outliers.empty:
            st.warning(f"⚠️ Se encontraron {len(outliers)} dato(s) atípico(s) en '{col}':")
            for _, row in outliers.iterrows():
                st.text(f"- {row[nombre_col]}: {col} = {row[col]}")
        else:
            st.success(f"✅ No se encontraron datos atípicos en '{col}'.")
