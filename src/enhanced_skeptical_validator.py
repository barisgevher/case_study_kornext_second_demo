import re
from typing import Dict, List



class EnhancedSkepticalValidator:
    """
     Gelişmiş Şüpheci Doğrulayıcı

     yaklaşım: Çıkarım öncesi ön işleme ve çıkarım sonrası doğrulama
    """

    def __init__(self):
        self.validation_rules = {
            'name_validation': {
                'min_length': 3,
                'max_length': 50,
                'required_pattern': r'^[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞIİÖŞÜ\s]+$',
                'forbidden_patterns': [r'\d', r'[!@#$%^&*()]'],
                'turkish_name_bonus': [r'[çğıöşüÇĞIİÖŞÜ]']
            },
            'address_validation': {
                'location_keywords': ['mahalle', 'sokak', 'cadde', 'bulvar', 'köy', 'ilçe', 'il', 'mah.', 'sok.', 'cd.', 'blv.'],
                'suspicious_patterns': [r'\d{5,}', r'[!@#$%^&*()]'],
                'context_requirements': ['yaşa', 'ikamet', 'otur', 'ev', 'daire']
            },
            'consistency_checks': {
                'tone_consistency': True,
                'temporal_consistency': True,
                'logical_consistency': True
            }
        }


        self.category_rules = {
            "internet_telekomünikasyon": {
                "keywords": [
                    "internet",
                    "wifi",
                    "adsl",
                    "fiber",
                    "modem",
                    "router",
                    "bağlantı kesintisi",
                    "türk telekom",
                    "vodafone",
                    "turkcell",
                    "superonline",
                    "millenicom"
                ],
                "negative_keywords": [
                    "su",
                    "kanalizasyon",
                    "elektrik",
                    "doğalgaz"
                ],
                "priority_score": 10.0
            },
            "su_kanalizasyon": {
                "keywords": [
                    "su",
                    "kanalizasyon",
                    "atık",
                    "pis",
                    "tıkanık",
                    "akıt",
                    "sızıntı",
                    "taşma",
                    "koku",
                    "kirli",
                    "içme suyu",
                    "şebeke",
                    "kesinti",
                    "basınç",
                    "kaçak",
                    "rögar",
                    "menhol",
                    "boru",
                    "vana",
                    "sayaç",
                    "fatura",
                    "musluk",
                    "lavabo",
                    "banyo",
                    "mutfak",
                    "tuvalet",
                    "bahçe",
                    "sokak",
                    "kanal",
                    "drenaj",
                    "yağmur",
                    "kesik",
                    "akmıyor",
                    "gelmıyor",
                    "düşük",
                    "yüksek",
                    "bulanık",
                    "kokulu",
                    "sıcak",
                    "soğuk",
                    "donmuş"
                ],
                "negative_keywords": [
                    "internet",
                    "telefon",
                    "elektrik",
                    "gaz"
                ],
                "priority_score": 9.0
            },
            "elektrik": {
                "keywords": [
                    "elektrik",
                    "güç kesintisi",
                    "elektrik kesintisi",
                    "şalt",
                    "pano",
                    "kablo",
                    "aydınlatma",
                    "ampul",
                    "priz",
                    "ışık",
                    "lamba",
                    "karanlık",
                    "loş",
                    "projektör",
                    "led",
                    "sokak lambası",
                    "direk",
                    "yanmıyor",
                    "söndü",
                    "bozuk",
                    "kesiyor"
                ],
                "negative_keywords": [
                    "su",
                    "internet",
                    "gaz"
                ],
                "priority_score": 9.0
            },
            "guvenlik": {
                "keywords": [
                    "güvenlik",
                    "suç",
                    "hırsızlık",
                    "saldırı",
                    "tehdit",
                    "korku",
                    "emniyet",
                    "polis",
                    "bekçi",
                    "kamera",
                    "uyuşturucu",
                    "sarhoş",
                    "kavga",
                    "bıçak",
                    "silah",
                    "yaralama",
                    "darp",
                    "gasp",
                    "kapkaç",
                    "dolandırıcılık",
                    "tehlikeli",
                    "riskli",
                    "güvensiz",
                    "korkutucu",
                    "şüpheli",
                    "suçlu",
                    "illegal"
                ],
                "negative_keywords": [],
                "priority_score": 10.0
            },
            "saglik_hijyen": {
                "keywords": [
                    "sağlık",
                    "hijyen",
                    "dezenfekte",
                    "steril",
                    "mikrop",
                    "bakteri",
                    "virüs",
                    "hastalık",
                    "bulaşıcı",
                    "hastane",
                    "sağlık ocağı",
                    "eczane",
                    "ambulans",
                    "doktor",
                    "hemşire",
                    "tıbbi",
                    "tedavi",
                    "ilaç",
                    "acil",
                    "hasta",
                    "yaralı",
                    "enfeksiyon",
                    "zehirlenme",
                    "toksik"
                ],
                "negative_keywords": [],
                "priority_score": 9.5
            },
            "yapim_insaat": {
                "keywords": [
                    "inşaat",
                    "yapım",
                    "bina",
                    "yapı",
                    "köprü",
                    "beton",
                    "çimento",
                    "demir",
                    "tuğla",
                    "proje",
                    "müteahhit",
                    "vinç",
                    "gecikmeli",
                    "yarıda",
                    "durmuş",
                    "tamamlanmamış",
                    "eksik",
                    "hatalı",
                    "duran",
                    "terk edilmiş",
                    "çöken",
                    "çatlayan",
                    "tehlike",
                    "risk"
                ],
                "negative_keywords": [],
                "priority_score": 8.5
            },
            "yol_ulasim": {
                "keywords": [
                    "yol",
                    "asfalt",
                    "kaldırım",
                    "çukur",
                    "bozuk",
                    "tamir",
                    "trafik",
                    "kavşak",
                    "otobüs",
                    "durak",
                    "otopark",
                    "kaza",
                    "tehlike",
                    "trafik kazası",
                    "çökme",
                    "çatlak",
                    "delik",
                    "kaygan",
                    "tehlikeli",
                    "kapali",
                    "engelli",
                    "tıkalı"
                ],
                "negative_keywords": [],
                "priority_score": 8.0
            },
            "arıza": {
                "keywords": [
                    "asansör arızalı",
                    "yürüyen merdiven çalışmıyor",
                    "bozuk",
                    "aktif değil",
                    "arıza",
                    "baz istasyonu"
                ],
                "negative_keywords": [],
                "priority_score": 8.0
            },
            "cevre_temizlik": {
                "keywords": [
                    "çöp",
                    "atık",
                    "temizlik",
                    "hijyen",
                    "kirli",
                    "pis",
                    "koku",
                    "böcek",
                    "fare",
                    "haşere",
                    "konteyner",
                    "çöp kutusu",
                    "ilaçlama",
                    "dolu",
                    "taşan",
                    "saçılmış",
                    "leş",
                    "pislik",
                    "berbat",
                    "iğrenç"
                ],
                "negative_keywords": [],
                "priority_score": 7.5
            },
            "okul_sorunu": {
                "keywords": [
                    "kaloriferler yanmıyor",
                    "montla ders işliyor",
                    "sınıflar soğuk",
                    "sınıflar kirli",
                    "sınıflar kalabalık",
                    "şiddet",
                    "psikolojik şiddet",
                    "zorbalığa uğrama",
                    "öğretmen zorbalığı",
                    "akran zorbalığı"
                ],
                "negative_keywords": [],
                "priority_score": 7.0
            },
            "faturalandırma_sorunu": {
                "keywords": [
                    "olağandışı artış",
                    "haksız ödeme",
                    "vergi kaçırma",
                    "yüksek mebla",
                    "servis bedeli",
                    "yeniden ölçüm",
                    "yeniden faturalandırma",
                    "kaçak kullanım"
                ],
                "negative_keywords": [],
                "priority_score": 7.0
            },
            "gurultu_rahatsizlik": {
                "keywords": [
                    "gürültü",
                    "ses",
                    "bağırma",
                    "müzik",
                    "hoparlör",
                    "rahatsız",
                    "uyku",
                    "huzur",
                    "yüksek",
                    "aşırı",
                    "dayanılmaz",
                    "sürekli",
                    "geç saatte",
                    "uygunsuz",
                    "yasak"
                ],
                "negative_keywords": [],
                "priority_score": 6.5
            },
            "park_yesil_alan": {
                "keywords": [
                    "park",
                    "bahçe",
                    "yeşil",
                    "ağaç",
                    "çiçek",
                    "oyun alanı",
                    "çocuk parkı",
                    "bank",
                    "sulama",
                    "budama",
                    "bakım",
                    "kurumuş",
                    "kesilmiş",
                    "harap",
                    "bakımsız",
                    "kirli",
                    "tahrip"
                ],
                "negative_keywords": [],
                "priority_score": 6.0
            },
            "kargo_sorunu": {
                "keywords": [
                    "kargo",
                    "elime ulaşmadı",
                    "kargo takip",
                    "yolda",
                    "ptt",
                    "yurtiçi kargo",
                    "mng",
                    "ups",
                    "sürat kargo",
                    "kurye",
                    "kargo şubesine ulaşamıyorum",
                    "kargom hasarlı"
                ],
                "negative_keywords": [],
                "priority_score": 5.5
            },
            "telefon-sorunu": {
                "keywords": [
                    "şebeke",
                    "telefon çekmiyor",
                    "ulaşamıyorum",
                    "sesini alamıyorum",
                    "çekmiyor",
                    "arama",
                    "arayamıyorum"
                ],
                "negative_keywords": [],
                "priority_score": 5.0
            },
            "pazaryeri_sorunu": {
                "keywords": [
                    "pazar yeri",
                    "sebze meyve pazarı",
                    "pazaryeri düzenlemesi",
                    "pazaryeri taşıması"
                ],
                "negative_keywords": [],
                "priority_score": 4.0
            }

        }

        # Gerçek olmayan isim kalıpları algoritma isim gördüğü için çıkarmak için eklendi
        self.fake_name_patterns = [
            r'.*kesinti.*',
            r'.*sorun.*',
            r'.*arıza.*',
            r'.*problem.*',
            r'.*talep.*',
            r'.*şikayet.*',
            r'.*başvuru.*',
            r'internet.*',
            r'elektrik.*',
            r'su.*',
            r'.*hizmet.*'
        ]

    def preprocess_and_validate(self, extraction_result: Dict, original_text: str) -> Dict:
        """Ana doğrulama fonksiyonu : ön işleme ve doğrulama"""

        # ön işleme (çıkarım hatalarını düzelt)
        preprocessed_result = self._preprocess_extraction(extraction_result, original_text)

        # mevcut doğrulama sistemi
        validation_results = self.validate_extraction(preprocessed_result, original_text)

        # düzeltilmiş sonucu dahil et
        validation_results['corrected_extraction'] = preprocessed_result

        return validation_results

    def _preprocess_extraction(self, extraction: Dict, original_text: str) -> Dict:
        """Çıkarım sonuçlarını ön işleme"""
        corrected = extraction.copy()

        # isim düzeltmesi
        if 'person_name' in corrected and corrected['person_name']:
            corrected_name = self._correct_name_extraction(corrected['person_name'], original_text)
            corrected['person_name'] = corrected_name

        # kategori düzeltmesi
        if 'subject_category' in corrected:
            corrected_category = self._correct_category_extraction(corrected['subject_category'], original_text)
            corrected['subject_category'] = corrected_category

        # adres düzeltmesi
        if 'address_info' in corrected and corrected['address_info']:
            corrected_address = self._correct_address_extraction(corrected['address_info'], original_text)
            corrected['address_info'] = corrected_address

        return corrected

    def _correct_name_extraction(self, extracted_name: str, original_text: str) -> str:
        """İsim çıkarımını düzelt"""

        # sahte isim kontrolü
        for pattern in self.fake_name_patterns:
            if re.search(pattern, extracted_name.lower()):
                # Gerçek isim aramaya geç
                real_names = self._find_real_names_in_text(original_text)
                if real_names:
                    return real_names[0]  # En güvenilir ismi al
                else:
                    return None  # İsim bulunamadı

        return extracted_name

    def _find_real_names_in_text(self, text: str) -> List[str]:
        """metinde gerçek isimleri bul"""

        # türkçe isim kalıpları
        name_pattern = r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞIİÖŞÜ]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞIİÖŞÜ]+)*\b'
        potential_names = re.findall(name_pattern, text)

        real_names = []
        for name in potential_names:
            # hizmet ve şikayet kelimelerini filtrele
            if not any(fake_word in name.lower() for fake_word in
                       ['kesinti', 'sorun', 'arıza', 'internet', 'türk telekom', 'gümüşpala', 'adsl']):
                # türkçe isim benzeri kontrolü
                if len(name.split()) <= 3 and len(name) >= 3:  # maksimum 3 kelime, minimum 3 harf
                    real_names.append(name)

        return real_names

    def _correct_category_extraction(self, extracted_category: str, original_text: str) -> str:
        """kategori çıkarımını düzelt"""

        text_lower = original_text.lower()

        # her kategori için skor hesapla
        category_scores = {}

        for category, rules in self.category_rules.items():
            score = 0.0

            #  anahtar kelimeler
            for keyword in rules['keywords']:
                if keyword in text_lower:
                    score += rules['priority_score']

            # anahtar kelimeler negatif
            for neg_keyword in rules['negative_keywords']:
                if neg_keyword in text_lower:
                    score -= rules['priority_score'] * 0.5

            category_scores[category] = score

        # en yüksek skorlu kategoriyi seç
        best_category = max(category_scores, key=category_scores.get)

        # Eğer skor çok düşükse, 'belirsiz' döndür
        if category_scores[best_category] <= 0:
            return 'belirsiz'

        return best_category

    def _correct_address_extraction(self, extracted_address: str, original_text: str) -> str:
        """adres çıkarımını düzelt"""

        # tarih ve zaman ifadeleri içerenşüpheli adres kalıpları
        suspicious_patterns = [
            r'sabahından bu yana',
            r'\d+\s+(eylül|ocak|şubat|mart|nisan|mayıs|haziran|temmuz|ağustos|ekim|kasım|aralık)',
            r'bu yana',
            r'dan beri'
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, extracted_address.lower()):
                # gerçek adres bilgisini bul
                real_address = self._find_real_address_in_text(original_text)
                return real_address if real_address else extracted_address

        return extracted_address

    def _find_real_address_in_text(self, text: str) -> str:
        """Metinde gerçek adresi bul"""

        # adres kalıpları
        address_patterns = [
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)*)\s+(mahalle|sokak|cadde|bulvar)',
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+Mahallesi',
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(daire|apartman|blok)',
        ]

        for pattern in address_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                return match.group().strip()

        return None

    def validate_extraction(self, extraction_result: Dict, original_text: str) -> Dict:
        """mevcut doğrulama sistemi"""
        validation_results = {
            'overall_validity': True,
            'confidence_adjustment': 1.0,
            'validation_details': {},
            'red_flags': [],
            'quality_score': 0.0,
            'corrections_applied': []
        }

        # isim doğrulaması
        if 'person_name' in extraction_result and extraction_result['person_name']:
            name_validation = self._validate_name(extraction_result['person_name'])
            validation_results['validation_details']['name'] = name_validation

            if not name_validation['is_valid']:
                validation_results['red_flags'].append("Şüpheli isim formatı")
                validation_results['confidence_adjustment'] *= 0.7
        else:
            validation_results['red_flags'].append("İsim bilgisi bulunamadı")
            validation_results['confidence_adjustment'] *= 0.8


        if 'address_info' in extraction_result and extraction_result['address_info']:
            address_validation = self._validate_address(extraction_result['address_info'], original_text)
            validation_results['validation_details']['address'] = address_validation

            if not address_validation['is_valid']:
                validation_results['red_flags'].append("Adres bilgisi şüpheli")
                validation_results['confidence_adjustment'] *= 0.8

        # kategori doğrulaması
        if 'subject_category' in extraction_result:
            category_validation = self._validate_category(extraction_result['subject_category'], original_text)
            validation_results['validation_details']['category'] = category_validation

            if not category_validation['is_valid']:
                validation_results['red_flags'].append("Kategori ataması şüpheli")
                validation_results['confidence_adjustment'] *= 0.7

        # tutarlılık kontrolü
        consistency_check = self._check_consistency(extraction_result, original_text)
        validation_results['validation_details']['consistency'] = consistency_check

        if not consistency_check['is_consistent']:
            validation_results['red_flags'].append("İçerik tutarsızlıkları tespit edildi")
            validation_results['confidence_adjustment'] *= 0.6

        # genel geçerlilik genel olarak algoritma sonuçları yeterli ve geçerli mi
        if validation_results['confidence_adjustment'] < 0.5:
            validation_results['overall_validity'] = False

        # kalite skoru
        validation_results['quality_score'] = self._calculate_quality_score(validation_results)

        return validation_results

    def _validate_category(self, category: str, original_text: str) -> Dict:
        """kategori doğrulaması"""

        if category not in self.category_rules:
            return {
                'is_valid': False,
                'issues': ['Bilinmeyen kategori'],
                'confidence': 0.1
            }

        rules = self.category_rules[category]
        text_lower = original_text.lower()

        #  kanıt sayısı
        positive_evidence = sum(1 for keyword in rules['keywords'] if keyword in text_lower)

        # negatif kanıt sayısı
        negative_evidence = sum(1 for neg_keyword in rules['negative_keywords'] if neg_keyword in text_lower)

        is_valid = positive_evidence > 0 and negative_evidence == 0

        issues = []
        if positive_evidence == 0:
            issues.append("Kategori için destekleyici kanıt bulunamadı")
        if negative_evidence > 0:
            issues.append(f"Çelişkili kanıt sayısı: {negative_evidence}")

        confidence = max(0.1, (positive_evidence - negative_evidence) / max(1, len(rules['keywords'])))

        return {
            'is_valid': is_valid,
            'issues': issues,
            'positive_evidence': positive_evidence,
            'negative_evidence': negative_evidence,
            'confidence': confidence
        }

    def _validate_name(self, name: str) -> Dict:
        """isim doğrulaması"""
        rules = self.validation_rules['name_validation']

        is_valid = True
        issues = []

        # null kontrolü
        if name is None:
            return {
                'is_valid': False,
                'issues': ['İsim bulunamadı'],
                'turkish_bonus': 0,
                'confidence': 0.0
            }

        # length kontrolü
        if len(name) < rules['min_length'] or len(name) > rules['max_length']:
            is_valid = False
            issues.append(f"Uzunluk uygunsuz: {len(name)}")

        # kural ve kalıp  kontrolü
        if not re.match(rules['required_pattern'], name):
            is_valid = False
            issues.append("Türkçe isim formatına uymuyor")

        # sahte isim kontrolü
        for pattern in self.fake_name_patterns:
            if re.search(pattern, name.lower()):
                is_valid = False
                issues.append("Sahte isim kalıbı tespit edildi")

        # yasak karakter kontrolü
        for forbidden in rules['forbidden_patterns']:
            if re.search(forbidden, name):
                is_valid = False
                issues.append(f"Yasak karakter: {forbidden}")


        turkish_bonus = 0
        for bonus_pattern in rules['turkish_name_bonus']:
            if re.search(bonus_pattern, name):
                turkish_bonus += 0.1

        return {
            'is_valid': is_valid,
            'issues': issues,
            'turkish_bonus': min(turkish_bonus, 0.3),
            'confidence': max(0.3, 1.0 - len(issues) * 0.2 + turkish_bonus)
        }

    def _validate_address(self, address: str, context: str) -> Dict:
        """adres doğrulaması"""
        rules = self.validation_rules['address_validation']

        is_valid = True
        issues = []

        # konum anahtar kelimeleri kontrolü
        has_location_keyword = any(keyword in address.lower() for keyword in rules['location_keywords'])
        if not has_location_keyword:
            is_valid = False
            issues.append("Adres anahtar kelimeleri eksik")

        # zaman ifadeleri şüpheli pattern kontrolü - algoritma zaman verilerini isimle karıştırdığı için güncelleme
        time_patterns = [r'sabahından', r'bu yana', r'\d+\s+(eylül|ocak|şubat)', r'dan beri']
        for pattern in time_patterns:
            if re.search(pattern, address.lower()):
                is_valid = False
                issues.append(f"Adres yerine zaman ifadesi: {pattern}")

        # bağlam ve mantık kontrolü
        context_support = any(req in context.lower() for req in rules['context_requirements'])
        if not context_support:
            issues.append("Adres bilgisi bağlamda desteklenmiyor")

        return {
            'is_valid': is_valid,
            'issues': issues,
            'context_support': context_support,
            'confidence': max(0.2, 1.0 - len(issues) * 0.3)
        }

    def _check_consistency(self, extraction: Dict, original_text: str) -> Dict:
        """tutarlılık kontrolü """
        issues = []

        # ton tutarlılığı çıkarımı
        text_lower = original_text.lower()
        formal_indicators = sum(1 for word in ['saygı', 'arz', 'gereği', 'takdir'] if word in text_lower)
        informal_indicators = sum(1 for word in ['ya', 'yani', 'işte'] if word in text_lower)

        if formal_indicators > 0 and informal_indicators > 0:
            issues.append("Dil tutarsızlığı: Formal ve günlük dil karışımı")

        # kategori-içerik tutarlılığı
        if 'subject_category' in extraction:
            category = extraction['subject_category']
            if category in self.category_rules:
                expected_keywords = self.category_rules[category]['keywords']
                found_keywords = [kw for kw in expected_keywords if kw in text_lower]

                if len(found_keywords) == 0:
                    issues.append(f"Kategori-içerik tutarsızlığı: {category} kategorisi ama ilgili anahtar kelime yok")

        # mantıksal tutarlılık
        if 'acil' in text_lower and 'uygun gördüğünüzde' in text_lower:
            issues.append("Mantık tutarsızlığı: Acil ama esnek zaman talebi")

        return {
            'is_consistent': len(issues) == 0,
            'issues': issues,
            'confidence': max(0.4, 1.0 - len(issues) * 0.4)
        }

    def _calculate_quality_score(self, validation_results: Dict) -> float:
        """Genel kalite skoru (güncellenmiş)"""
        base_score = validation_results['confidence_adjustment']

        # red flag cezası
        red_flag_penalty = len(validation_results['red_flags']) * 0.15

        # Detay bonusu
        detail_count = len(validation_results['validation_details'])
        detail_bonus = min(detail_count * 0.1, 0.3)

        final_score = max(0.1, base_score - red_flag_penalty + detail_bonus)
        return round(final_score, 3)