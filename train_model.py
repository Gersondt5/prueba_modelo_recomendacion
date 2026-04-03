import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Dataset simple
data = {
    "nota": [10, 20, 30, 40, 55, 65, 75, 85, 90, 100],
    "nivel": ["bajo", "bajo", "bajo", "bajo", "bajo", "medio", "medio", "alto", "alto", "alto"]
}

df = pd.DataFrame(data)

X = df[["nota"]]
y = df["nivel"]

modelo = DecisionTreeClassifier()
modelo.fit(X, y)

# 💾 GUARDAR MODELO
joblib.dump(modelo, "modelo.pkl")

print("✅ Modelo creado correctamente")