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
        "¿Vive con?",  # ⚠️ Revisa duplicado
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

    # Inicia filtrado por homoclave
    homoclave = st.text_input("🔑 Introduce la homoclave del docente (ej. PROF1003)").strip().upper()
    if homoclave:
        df_docente = df[df['Homoclave del docente'].str.upper() == homoclave]

        if df_docente.empty:
            st.warning("⚠️ No se encontraron datos para esa homoclave.")
        else:
            st.subheader(f"📊 Datos filtrados para la homoclave: {homoclave}")
            st.dataframe(df_docente)

            busqueda = st.radio("🔍 ¿Desea realizar una búsqueda personalizada?", ["No", "Sí"])

            nombre_cols = [col for col in df_docente.columns if "Nombre" in col]
            if not nombre_cols:
                st.error("❌ No se encontró una columna con 'Nombre'.")
                st.stop()
            nombre_col = nombre_cols[0]

            if busqueda == "Sí":
                nombre_estudiante = st.text_input(f"Introduce el nombre del estudiante (columna '{nombre_col}')").strip()
                if nombre_estudiante:
                    df_estudiante = df_docente[
                        df_docente[nombre_col].str.lower().str.contains(nombre_estudiante.lower(), na=False)
                    ]
                    if df_estudiante.empty:
                        st.warning("⚠️ No se encontró al estudiante.")
                    else:
                        st.subheader(f"🎓 Datos del estudiante: {nombre_estudiante}")
                        st.dataframe(df_estudiante)
            else:
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

                # Quitar duplicados de la lista
                columnas_categoricas = list(dict.fromkeys(columnas_categoricas))

                for col in columnas_categoricas:
                    if col not in df_docente.columns:
                        st.info(f"ℹ️ La columna '{col}' no se encontró en los datos. Se omite.")
                        continue

                    st.markdown(f"### 📊 Distribución: {col}")

                    if col == 'Promedio':
                        bins = np.arange(6.0, 10.5, 0.5)
                        etiquetas = [f'{i:.1f} - {i + 0.4:.1f}' for i in bins[:-1]]
                        df_docente.loc[:, 'Rango Promedio'] = pd.cut(df_docente[col], bins=bins, labels=etiquetas)
                        conteo = df_docente['Rango Promedio'].value_counts().sort_index()
                    else:
                        conteo = df_docente[col].value_counts(dropna=False)

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

                columnas_a_evaluar = [
                    'Edad',
                    'Promedio',
                    'Tiempo estudio'
                ]

                for col in columnas_a_evaluar:
                    if col not in df_docente.columns:
                        st.info(f"ℹ️ La columna '{col}' no se encontró en los datos. Se omite.")
                        continue

                    st.markdown(f"### 📈 Distribución de {col}")

                    datos = df_docente[[nombre_col, col]].dropna()

                    if datos.empty:
                        st.warning(f"⚠️ No hay datos disponibles para '{col}'.")
                        continue

                    Q1 = datos[col].quantile(0.25)
                    Q3 = datos[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower = Q1 - 1.5 * IQR
                    upper = Q3 + 1.5 * IQR

                    if col == 'Edad':
                        bins = np.arange(17, 22, 2)
                    elif 'promedio' in col.lower():
                        bins = np.arange(6.0, 10.5, 0.5)
                    else:
                        bins = 10

                    df_docente.loc[:, 'Rango_' + col] = pd.cut(df_docente[col], bins=bins)
                    conteo_barras = df_docente['Rango_' + col].value_counts().sort_index()

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
