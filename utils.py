import pdfplumber
import re
import pandas as pd
import unicodedata


def normalizar(texto):
    texto = texto.upper()
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto.strip()


def leer_pdf(file):
    texto = ""
    with pdfplumber.open(file) as pdf:
        for pagina in pdf.pages:
            contenido = pagina.extract_text()
            if contenido:
                texto += contenido + " "
    return texto


def procesar_texto(texto):

    texto = re.sub(r"\s+", " ", texto)

    bloques = re.findall(r"(\d+\s+[A-Z]{3}-\d+.*?APROBADO)", texto)

    datos = []

    for bloque in bloques:
        try:
            numero = int(re.match(r"(\d+)", bloque).group(1))
            sigla = re.search(r"([A-Z]{3}-\d+)", bloque).group(1)

            nota = int(re.search(
                r"\b(100|[0-9]{2})\s+[A-Za-zÁÉÍÓÚáéíóúñÑ ]+\s+\d+\s*(?:\d+)?\s+APROBADO",
                bloque
            ).group(1))

            literal = re.search(
                r"\b(100|[0-9]{2})\s+([A-Za-zÁÉÍÓÚáéíóúñÑ ]+?)\s+\d+\s*(?:\d+)?\s+APROBADO",
                bloque
            ).group(2).strip()

            materia = re.search(
                rf"{sigla}\s+(.*?)\s+(PRE-U|[A-Z]{{3}}-\d+|\w+\.)",
                bloque
            ).group(1).strip()

            datos.append({
                "N°": numero,
                "Sigla": sigla,
                "Materia": materia,
                "Nota": nota,
                "Literal": literal
            })

        except:
            continue

    return pd.DataFrame(datos)