import re
from typing import Dict


class SkepticalValidator:
    """
    🔍 Şüpheci Doğrulayıcı

    YARATICI YAKLAŞIM: Her bulguyu şüpheyle karşılar ve çapraz doğrular
    "Güvenilir misin?" sorusu her adımda
    """

    def __init__(self):
        self.validation_rules = {
            'name_validation': {
                'min_length': 3,
                'max_length': 50,
                'required_pattern': r'^[A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]+$',
                'forbidden_patterns': [r'\d', r'[!@#$%^&*()]'],
                'turkish_name_bonus': [r'[çğıöşüÇĞIİÖŞÜ]']
            },

            'address_validation': {
                'location_keywords': ['mahalle', 'sokak', 'cadde', 'bulvar', 'köy'],
                'suspicious_patterns': [r'\d{5,}', r'[!@#$%^&*()]'],
                'context_requirements': ['yaşa', 'ikamet', 'otur', 'ev']
            },

            'consistency_checks': {
                'tone_consistency': True,  # Formal dil + argo karışmamalı
                'temporal_consistency': True,  # Zaman ifadeleri tutarlı olmalı
                'logical_consistency': True  # Mantıksal çelişkiler kontrol edilir
            }
        }

    def validate_extraction(self, extraction_result: Dict, original_text: str) -> Dict:
        """Çıkarım sonuçlarını doğrula"""
        validation_results = {
            'overall_validity': True,
            'confidence_adjustment': 1.0,
            'validation_details': {},
            'red_flags': [],
            'quality_score': 0.0
        }

        # İsim doğrulaması
        if 'person_name' in extraction_result and extraction_result['person_name']:
            name_validation = self._validate_name(extraction_result['person_name'])
            validation_results['validation_details']['name'] = name_validation

            if not name_validation['is_valid']:
                validation_results['red_flags'].append("Şüpheli isim formatı")
                validation_results['confidence_adjustment'] *= 0.7

        # Adres doğrulaması
        if 'address' in extraction_result and extraction_result['address']:
            address_validation = self._validate_address(extraction_result['address'], original_text)
            validation_results['validation_details']['address'] = address_validation

            if not address_validation['is_valid']:
                validation_results['red_flags'].append("Adres bilgisi şüpheli")
                validation_results['confidence_adjustment'] *= 0.8

        # Tutarlılık kontrolü
        consistency_check = self._check_consistency(extraction_result, original_text)
        validation_results['validation_details']['consistency'] = consistency_check

        if not consistency_check['is_consistent']:
            validation_results['red_flags'].append("İçerik tutarsızlıkları tespit edildi")
            validation_results['confidence_adjustment'] *= 0.6

        # Genel geçerlilik
        if validation_results['confidence_adjustment'] < 0.5:
            validation_results['overall_validity'] = False

        # Kalite skoru
        validation_results['quality_score'] = self._calculate_quality_score(validation_results)

        return validation_results

    def _validate_name(self, name: str) -> Dict:
        """İsim doğrulaması"""
        rules = self.validation_rules['name_validation']

        is_valid = True
        issues = []

        # Uzunluk kontrolü
        if len(name) < rules['min_length'] or len(name) > rules['max_length']:
            is_valid = False
            issues.append(f"Uzunluk uygunsuz: {len(name)}")

        # Pattern kontrolü
        if not re.match(rules['required_pattern'], name):
            is_valid = False
            issues.append("Türkçe isim formatına uymuyor")

        # Yasak karakterler
        for forbidden in rules['forbidden_patterns']:
            if re.search(forbidden, name):
                is_valid = False
                issues.append(f"Yasak karakter: {forbidden}")

        # Türkçe bonus
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
        """Adres doğrulaması"""
        rules = self.validation_rules['address_validation']

        is_valid = True
        issues = []

        # Konum anahtar kelimeleri kontrolü
        has_location_keyword = any(keyword in address.lower() for keyword in rules['location_keywords'])
        if not has_location_keyword:
            is_valid = False
            issues.append("Adres anahtar kelimeleri eksik")

        # Şüpheli pattern kontrolü
        for suspicious in rules['suspicious_patterns']:
            if re.search(suspicious, address):
                issues.append(f"Şüpheli pattern: {suspicious}")

        # Bağlam kontrolü
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
        """Tutarlılık kontrolü"""
        issues = []

        # Ton tutarlılığı (formal dil + argo kontrol)
        text_lower = original_text.lower()
        formal_indicators = sum(1 for word in ['saygı', 'arz', 'gereği', 'takdir'] if word in text_lower)
        informal_indicators = sum(1 for word in ['ya', 'yani', 'işte'] if word in text_lower)

        if formal_indicators > 0 and informal_indicators > 0:
            issues.append("Dil tutarsızlığı: Formal ve günlük dil karışımı")

        # Mantıksal tutarlılık örnekleri
        if 'acil' in text_lower and 'uygun gördüğünüzde' in text_lower:
            issues.append("Mantık tutarsızlığı: Acil ama esnek zaman talebi")

        return {
            'is_consistent': len(issues) == 0,
            'issues': issues,
            'confidence': max(0.4, 1.0 - len(issues) * 0.4)
        }

    def _calculate_quality_score(self, validation_results: Dict) -> float:
        """Genel kalite skoru"""
        base_score = validation_results['confidence_adjustment']

        # Red flag cezası
        red_flag_penalty = len(validation_results['red_flags']) * 0.15

        # Detay bonusu
        detail_count = len(validation_results['validation_details'])
        detail_bonus = min(detail_count * 0.1, 0.3)

        final_score = max(0.1, base_score - red_flag_penalty + detail_bonus)
        return round(final_score, 3)