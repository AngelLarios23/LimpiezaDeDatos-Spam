import os
import joblib
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Descargar stopwords en español si no están disponibles
nltk.download("stopwords")
from nltk.corpus import stopwords
spanish_stopwords = stopwords.words("spanish")

# Importar limpieza
from cleaner.clean_text import clean_email_body

# Función para cargar correos y etiquetarlos
def load_emails(folder: str, label: int) -> list:
    emails = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                raw = f.read()
                cleaned = clean_email_body(raw)["cleaned"]
                if cleaned:  # evitar vacíos
                    emails.append((cleaned, label))
    return emails

# Cargar datos
spam = load_emails("data/spam", 1)
ham = load_emails("data/ham", 0)
all_data = spam + ham

# Separar texto y etiquetas
if not all_data:
    raise ValueError("No se encontraron correos en las carpetas 'data/spam' y 'data/ham'. Verifica que los archivos existen y contienen texto.")
texts, labels = zip(*all_data)

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Crear pipeline de entrenamiento
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words=spanish_stopwords)),
    ("nb", MultinomialNB())
])

# Entrenar modelo
model.fit(X_train, y_train)

# Evaluar modelo
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Guardar modelo entrenado
joblib.dump(model, "model/spam_model.joblib")
print("✅ Modelo guardado en model/spam_model.joblib")