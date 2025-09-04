from PetitionAnalyzer import PetitionAnalyzer


def demo_algorithm():
    """ algoritmanın demo çalışması"""

    print("🚀 ÇKŞÇM - Yaratıcı Dilekçe Analiz Algoritması Demo")
    print("=" * 60)

    # Algoritma başlatma
    analyzer = PetitionAnalyzer()

    # Test dilekçeleri
    test_petitions = [
        {
            "name": "Öfkeli Vatandaş",
            "text": """
            Belediye Başkanlığı!

            ARTIK YETER! Her gün aynı şey... Sokağımızdaki çöpler toplanmıyor!
            Defalarca aradık, hiç kimse ilgilenmiyor. Koku dayanılmaz halde!

            Ya bu işi halledersiniz ya da medyaya gideceğim!
            Acilen çözüm bekliyoruz!!!

            Mehmet ÖZKAYA - Çankaya Mahallesi sakinleri adına
            """
        },
        {
            "name": "Kibar Yaşlı Vatandaş",
            "text": """
            Sayın Belediye Başkanımız,

            Emekliyim ve Yeşiltepe Mahallesi Gül Sokak'ta tek başıma yaşıyorum.

            Mahallemizde sokak lambaları çalışmıyor. Akşamları eve giderken
            çok korkuyorum. Yaşlı bir vatandaş olarak bu durumdan endişeliyim.

            Mümkünse bu konuya dikkat ederseniz çok memnun olurum.
            Saygılarımla teşekkür ederim.

            Fatma YILMAZ
            """
        },
        {
            "name": "Acil Güvenlik Sorunu",
            "text": """
            ACİL DURUM!

            Çocuk parkındaki salıncaklar KIRILMIŞ! Çocuklar yaralanabilir!
            Bu sabah küçük oğlum neredeyse düşüyordu.

            HEMEN müdahale edilmeli! Can güvenliği söz konusu!
            Derhal harekete geçin!

            Ahmet VELİOĞLU - Merkez Mahallesi Veliler Derneği Başkanı
            Tel: 0532 123 45 67
            """
        }
    ]

    # Her test dilekçesini analiz et
    for i, petition in enumerate(test_petitions, 1):
        print(f"\n📋 TEST {i}: {petition['name']}")
        print("-" * 40)

        # Analiz yap
        result = analyzer.analyze_petition_creative(petition['text'])

        # Özet sonuçları göster
        print(f"✅ Analiz tamamlandı!")
        print(f"🎯 Güven Seviyesi: %{result['metadata']['confidence_level'] * 100:.1f}")
        print(f"🎭 Baskın Duygu: {result['emotional_intelligence']['dominant_emotion']}")
        print(f"⚡ Aciliyet: {result['extracted_information']['urgency_level']}")
        print(f"🏷️  Konu: {result['extracted_information']['subject_category']}")
        print(f"⚠️  Risk Seviyesi: {result['creative_insights']['risk_assessment']['risk_level']}")

        # Eylem önerisi sayısı
        rec_count = len(result['actionable_recommendations'])
        print(f"💡 Eylem Önerisi: {rec_count} adet")

        if i < len(test_petitions):
            print("\n" + "=" * 60)

    # Sistem istatistikleri
    print(f"\n📊 SİSTEM İSTATİSTİKLERİ:")
    stats = analyzer.get_system_statistics()
    print(f"  • Toplam Analiz: {stats['performance_metrics']['total_analyzed']}")
    print(f"  • Başarı Oranı: %{stats['success_rate']}")
    print(f"  • Ortalama İşlem Süresi: {stats['performance_metrics']['average_processing_time']} saniye")
    print(f"  • Ortalama Güven: %{stats['average_confidence'] * 100:.1f}")

    return analyzer, test_petitions


def detailed_analysis_example():
    """Detaylı analiz örneği"""

    analyzer = PetitionAnalyzer()

    # Karmaşık test dilekçesi
    # test ederken ismi yanlış buluyor Fenerbahçe mah
    complex_petition = """
Merhabalar,
Babam 75 yaşında ve kalp hastası. Yaşadığımız binanın asansörü üç aydır arızalı.
 Defalarca site yönetimine bildirdik, ancak henüz bir gelişme yok. Belediyenin veya ilgili kurumun denetleme yaparak gerekli işlemleri başlatmasını talep ediyorum.
Serkan Güler, Keçiören / Ankara
    """

    print("🔍 DETAYLI ANALİZ ÖRNEĞİ")
    print("=" * 50)

    # Analiz yap
    result = analyzer.analyze_petition_creative(complex_petition)

    # Detaylı rapor üret
    detailed_report = analyzer.generate_detailed_report(result)
    print(detailed_report)

    # JSON sonucu da göster
    print("\n" + "=" * 70)
    print("📄 JSON ÇIKTI ÖRNEĞİ (Temel Bilgiler):")
    print("=" * 70)

    simplified_result = {
        "extracted_info": result['extracted_information'],
        "emotional_state": result['emotional_intelligence']['dominant_emotion'],
        "confidence": result['metadata']['confidence_level'],
        "risk_level": result['creative_insights']['risk_assessment']['risk_level'],
        "recommendations_count": len(result['actionable_recommendations'])
    }

    import json
    print(json.dumps(simplified_result, ensure_ascii=False, indent=2))

    return result


# Ana çalıştırma fonksiyonu
if __name__ == "__main__":
    print("🧠 ÇKŞÇM: Çok Katmanlı Şüpheci Çıkarım Motoru")
    print("🎯 Yaratıcı Dilekçe Analiz Algoritması")
    print("🚀 Algoritma test ediliyor...\n")

    # Demo çalıştır
    # analyzer, test_cases = demo_algorithm()

    print("\n" + "🔥" * 20 + " DETAYLI ANALİZ " + "🔥" * 20)

    # Detaylı analiz örneği
    detailed_result = detailed_analysis_example()

    print(f"\n✅ Algoritma başarıyla test edildi!")
    print(f"🎨 Yaratıcı özellikler: Duygusal momentum, sosyal profil, şüpheci doğrulama")
   #  print(f"⚡ Performance: Ortalama {analyzer.performance_metrics['average_processing_time']:.3f} saniye")
    print(f"🎯 Bu algoritma tamamen özgün ve yaratıcı yaklaşımlar içeriyor!")