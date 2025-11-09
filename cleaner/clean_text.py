import re
import unicodedata
from bs4 import BeautifulSoup

# Lista básica de palabras clave de spam (puedes expandirla)
SPAM_KEYWORDS = [
    "gratis", "haz clic", "urgente", "oferta", "dinero rápido", "compra ahora",
    "sin costo", "gana dinero", "promoción", "descuento", "prueba gratuita"
]

def normalize_text(text: str) -> str:
    """Convierte a minúsculas, elimina acentos y normaliza espacios."""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
    text = re.sub(r"\s+", " ", text).strip()
    return text

def remove_html(text: str) -> str:
    """Elimina etiquetas HTML si el texto viene de correos en formato HTML."""
    return BeautifulSoup(text, "html.parser").get_text()

def remove_emojis(text: str) -> str:
    """Elimina emojis y caracteres especiales."""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticonos
        u"\U0001F300-\U0001F5FF"  # símbolos y pictogramas
        u"\U0001F680-\U0001F6FF"  # transporte y símbolos
        u"\U0001F1E0-\U0001F1FF"  # banderas
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r"", text)

def detect_spam_keywords(text: str) -> list:
    """Detecta palabras clave de spam en el texto limpio."""
    found = [kw for kw in SPAM_KEYWORDS if kw in text]
    return found

def clean_email_body(text: str) -> dict:
    """Aplica limpieza completa y detecta spam."""
    raw = text
    text = remove_html(text)
    text = remove_emojis(text)
    text = normalize_text(text)
    keywords = detect_spam_keywords(text)
    return {
        "original": raw,
        "cleaned": text,
        "spam_keywords": keywords,
        "is_spam": len(keywords) > 0
    }