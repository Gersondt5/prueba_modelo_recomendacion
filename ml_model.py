import json
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os

# Archivos
RECURSOS_FILE = "recursos.json"
PRUEBAS_FILE = "pruebas.json"
FEEDBACK_FILE = "feedback.json"
MODELO_FILE = "modelo_recursos.pkl"

# Cargar recursos y pruebas
with open(RECURSOS_FILE, "r", encoding="utf-8") as f:
    recursos_data = json.load(f)
with open(PRUEBAS_FILE, "r", encoding="utf-8") as f:
    pruebas_data = json.load(f)

# --- Feedback ---
def leer_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            f.write("{}")
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def guardar_feedback(feedback):
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2)

def actualizar_feedback(materia, nivel, recurso, tipo):
    feedback = leer_feedback()
    if materia not in feedback:
        feedback[materia] = {}
    if nivel not in feedback[materia]:
        feedback[materia][nivel] = {}
    if recurso not in feedback[materia][nivel]:
        feedback[materia][nivel][recurso] = {"likes":0,"dislikes":0}
    feedback[materia][nivel][recurso][tipo] += 1
    guardar_feedback(feedback)

# --- Clasificación de nivel por nota ---
def clasificar_nivel(nota):
    if nota < 60:
        return "bajo"
    elif nota < 80:
        return "medio"
    else:
        return "alto"

# --- Recomendaciones básicas ---
def recomendar_recursos(materia, nivel):
    return recursos_data.get(materia, {}).get(nivel, [])

def obtener_prueba(materia, nivel):
    return pruebas_data.get(materia, {}).get(nivel, "#")

# --- ML: Entrenar modelo usando feedback ---
def entrenar_modelo():
    feedback = leer_feedback()
    registros = []
    for mat, niveles in feedback.items():
        for niv, recursos in niveles.items():
            for rec, stats in recursos.items():
                likes = stats.get("likes",0)
                dislikes = stats.get("dislikes",0)
                utilidad = 1 if (likes - dislikes) > 0 else 0
                registros.append({"Materia": mat, "Nivel": niv, "Recurso": rec, 
                                  "Likes": likes, "Dislikes": dislikes, "Utilidad": utilidad})
    if not registros:
        return None  # nada que entrenar
    df = pd.DataFrame(registros)
    X = df[["Materia","Nivel","Recurso","Likes","Dislikes"]]
    y = df["Utilidad"]

    # Pipeline para convertir categóricas en dummies
    ct = ColumnTransformer([
        ("onehot", OneHotEncoder(handle_unknown="ignore"), ["Materia","Nivel","Recurso"])
    ], remainder="passthrough")
    model = Pipeline([("preproc", ct), ("clf", RandomForestClassifier(n_estimators=100, random_state=42))])
    model.fit(X, y)
    joblib.dump(model, MODELO_FILE)
    return model

# --- ML: Predecir utilidad de un recurso ---
def predecir_utilidad(materia, nivel, recurso, likes=0, dislikes=0):
    if not os.path.exists(MODELO_FILE):
        entrenar_modelo()
    model = joblib.load(MODELO_FILE)
    X_pred = pd.DataFrame([{"Materia":materia,"Nivel":nivel,"Recurso":recurso,"Likes":likes,"Dislikes":dislikes}])
    score = model.predict_proba(X_pred)[0,1]  # probabilidad de ser útil
    return score