import PyPDF2

def pdf_to_text(path: str) -> str:
    """
    Verilen yoldaki bir PDF dosyasını okur ve metin içeriğini döndürür.
    """
    try:
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        return text
    except FileNotFoundError:
        print(f"Hata: {path} dosyası bulunamadı.")
        return ""
    except Exception as e:
        print(f"PDF okunurken bir hata oluştu: {e}")
        return ""