from cleaner.clean_text import clean_email_body

def test_clean_email_body():
    sample = "<html><body>¡Gana dinero rápido! Haz clic aquí para tu promoción 🎉</body></html>"
    result = clean_email_body(sample)
    assert result["is_spam"] is True
    assert "gana dinero" in result["spam_keywords"]
    assert "haz clic" in result["spam_keywords"]