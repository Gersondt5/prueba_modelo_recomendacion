import streamlit as st
from utils import leer_pdf, procesar_texto, normalizar

st.set_page_config(page_title="Analizador Académico", layout="wide")

st.title("📊 Analizador de Historial Académico")

st.write("Sube tu historial en PDF y obtén las materias filtradas automáticamente.")

# 📤 SUBIR PDF
archivo = st.file_uploader("Subir archivo PDF", type=["pdf"])

# 🎯 LISTA REAL DE MATERIAS (IMPORTANTE: sin ...)
materias_objetivo = [
    "INTRODUCCION A LA PROGRAMACION",
    "PROGRAMACION I",
    "PROGRAMACION II",
    "ESTRUCTURA DE DATOS",
    "BASE DE DATOS I",
    "SISTEMAS OPERATIVOS",
    "ELECTRONICA BASICA",
    "BASE DE DATOS II",
    "ANALISIS Y DISENO I",
    "ARQUITECTURA DE COMPUTADORAS",
    "SISTEMAS DIGITALES",
    "ADMINISTRACION DE BASE DE DATOS",
    "TECNOLOGIAS EMERGENTES I",
    "ANALISIS Y DISENO II",
    "INGENIERIA DE REDES I",
    "INGENIERIA DE SISTEMAS I",
    "INGENIERIA DE SOFTWARE",
    "INGENIERIA DE REDES II",
    "SISTEMAS DE INFORMACION GEOGRAFICA",
    "INTELIGENCIA ARTIFICIAL I",
    "INGENIERIA DE SISTEMAS II",
    "SEGURIDAD DE SISTEMAS",
    "INGENIERIA DE REDES III",
    "ADMINISTRACION DE SERVIDORES",
    "AUDITORIA DE SISTEMAS",
    "ROBOTICA INDUSTRIAL",
    "AUTOMATIZACION Y CONTROL",
    "MODELADO Y SIMULACION DE SISTEMAS",
    "INTELIGENCIA ARTIFICIAL II"
]

# 🚀 PROCESAMIENTO
if archivo:

    with st.spinner("🔍 Procesando PDF..."):

        texto = leer_pdf(archivo)
        df = procesar_texto(texto)

        if df.empty:
            st.error("❌ No se pudieron extraer datos del PDF")
            st.stop()

        # 🔧 NORMALIZACIÓN
        materias_norm = [normalizar(m) for m in materias_objetivo]
        df["Materia_norm"] = df["Materia"].apply(normalizar)

        # 🎯 FILTRADO
        df_filtrado = df[df["Materia_norm"].isin(materias_norm)]
        df_filtrado = df_filtrado.drop(columns=["Materia_norm"])

    # 💾 GUARDAR EN MEMORIA (SESSION STATE)
    st.session_state["df_filtrado"] = df_filtrado

    st.success("✅ Procesamiento completado")

    # 📊 TABLA
    st.subheader("🎯 Materias filtradas")
    st.dataframe(df_filtrado, use_container_width=True)

    # 📥 DESCARGA
    csv = df_filtrado.to_csv(index=False).encode("utf-8")

    

    # 📚 BOTÓN A RECURSOS
    if st.button("📚 Mostrar Recursos"):
        st.switch_page("recursos.py")
