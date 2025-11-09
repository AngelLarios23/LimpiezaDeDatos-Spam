from fastapi import APIRouter, UploadFile, File
import pandas as pd
from model.predict import predict_spam

router = APIRouter()

@router.post("/batch-predict")
async def batch_predict(file: UploadFile = File(...)):
    try:
        # Leer archivo según extensión
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file, encoding="latin1")
        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(file.file)
        else:
            return {"error": "Formato no soportado. Usa .csv o .xlsx"}

        # Validar columna esperada
        if "text" not in df.columns:
            return {"error": "El archivo debe tener una columna llamada 'text'"}

        # Filtrar filas vacías o con solo espacios
        df = df[df["text"].notna() & (df["text"].str.strip() != "")]

        # Procesar cada fila
        results = []
        for i, row in df.iterrows():
            text = str(row["text"]).strip()
            result = predict_spam(text)
            results.append({
                "index": i,
                "original_text": text,
                "cleaned_text": result["cleaned_text"],
                "is_spam": result["is_spam"],
                "confidence": result["confidence"]
            })

        return {"results": results}
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el archivo: {str(e)}"}