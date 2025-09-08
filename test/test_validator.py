from src.validator import SkepticalValidator
def example_usage():
    """Gelişmiş doğrulayıcı kullanım örneği"""

    validator = SkepticalValidator()

    # Problematik çıkarım sonucu (sizin örneğiniz)
    extraction_result = {
        "person_name": "İnternet Kesintisi",
        "address_info": "sabahından bu yana İzmir Gümüşpala",
        "institution": None,
        "subject_category": "su_kanalizasyon",
        "urgency_level": "high",
        "request_type": "cozum_talebi"
    }

    original_text = """İzmir Gümüşpala'da Uzun Süreli Ve İlgisiz Türk Telekom İnternet Kesintisi

    Ben Barış Gevher 4 Eylül 2024 sabahından bu yana İzmir Gümüşpala Mahallesi'indeki dairemde 
    Türk Telekom ADSL internetim tamamen kesik. Sadece benim dairemde sorun yaşanıyor, 
    apartmanda başka kimse aynı problemi yaşamıyor."""

    # Doğrulama ve düzeltme
    results = validator.preprocess_and_validate(extraction_result, original_text)

    print("Düzeltilmiş Çıkarım:")
    print(f"İsim: {results['corrected_extraction']['person_name']}")
    print(f"Adres: {results['corrected_extraction']['address_info']}")
    print(f"Kategori: {results['corrected_extraction']['subject_category']}")

    print(f"\nKalite Skoru: {results['quality_score']}")
    print(f"Red Flagler: {results['red_flags']}")


if __name__ == "__main__":
    example_usage()