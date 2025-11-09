import joblib
from cleaner.clean_text import clean_email_body

model = joblib.load("model/spam_model.joblib")

def predict_spam(text: str) -> dict:
    cleaned = clean_email_body(text)["cleaned"]
    prediction = model.predict([cleaned])[0]
    probas = model.predict_proba([cleaned])[0]
    spam_score = round(max(probas), 2)

    return {
        "is_spam": bool(prediction),
        "confidence": spam_score,
        "cleaned_text": cleaned
    }