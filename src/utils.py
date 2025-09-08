import PyPDF2

def pdf_to_text(path: str) -> str:
    """
    verilen yoldaki bir PDF dosyasını okur ve metin içeriğini döndürür.
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



def format_result_summary(result_data):
    """
    Karmaşık JSON sonucunu alıp okunabilir bir metin özeti oluşturur.
    """
    try:
        # Ana bilgileri extracted_information bölümünden alıyoruz
        info = result_data.get('extracted_information', {})
        person_name = info.get('person_name', 'Belirtilmemiş')
        subject_category = info.get('subject_category', 'Belirtilmemiş')
        urgency_level = info.get('urgency_level', 'Belirtilmemiş')
        request_type = info.get('request_type', 'Belirtilmemiş')

        # Duygu analizi bilgilerini alıyoruz
        emotion_info = result_data.get('emotional_intelligence', {})
        dominant_emotion = emotion_info.get('dominant_emotion', 'Belirtilmemiş')

        # Kurumsal önerileri creative_insights bölümünden alıyoruz
        insights = result_data.get('creative_insights', {})
        response_rec = insights.get('institutional_response_recommendation', {})
        priority = response_rec.get('response_priority', 'Belirtilmemiş')
        timeline = response_rec.get('suggested_timeline', 'Belirtilmemiş')

        # Risk değerlendirmesi bilgilerini alıyoruz
        risk = insights.get('risk_assessment', {})
        risk_level = risk.get('risk_level', 'Belirtilmemiş')

        # Kaynak dosya bilgisini alıyoruz
        source_file = result_data.get('kaynak_dosya', 'Belirtilmemiş')

        # Tüm bilgileri düzenli bir metin bloğu haline getiriyoruz
        summary = (
            f"--- ÖZET RAPOR ---\n\n"
            f"Kaynak Dosya: {source_file}\n"
            f"----------------------------------------\n\n"
            f"👤 KİŞİ BİLGİLERİ\n"
            f"  - Ad Soyad: {person_name}\n\n"
            f"📑 TALEP DETAYLARI\n"
            f"  - Kategori: {subject_category}\n"
            f"  - Talep Türü: {request_type}\n"
            f"  - Aciliyet: {urgency_level.capitalize()}\n\n"
            f"🧠 ANALİZ SONUÇLARI\n"
            f"  - Baskın Duygu: {dominant_emotion.capitalize()}\n"
            f"  - Risk Seviyesi: {risk_level.capitalize()}\n\n"
            f"💡 KURUMSAL ÖNERİLER\n"
            f"  - Öncelik: {priority.capitalize()}\n"
            f"  - Tahmini Çözüm Süresi: {timeline}\n"
        )
        return summary

    except Exception as e:
        return f"Veri işlenirken bir hata oluştu: {e}\n\nLütfen ham veriyi kontrol edin."