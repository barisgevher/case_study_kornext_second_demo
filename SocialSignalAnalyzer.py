from collections import defaultdict
from typing import Dict


class SocialSignalAnalyzer:
    """ Sosyal Sinyal Analizörü

    YARATICI YAKLAŞIM: Vatandaşın sosyal durumunu dilinden çıkarır
    """

    def __init__(self):
        self.social_indicators = {
            'family_status': {
                'has_family': [
                    'çocuk', 'çocuğ', 'bebek', 'aile', 'eş', 'karı', 'koca',
                    'anne', 'baba', 'oğl', 'kız', 'evlat', 'torun'
                ],
                'single_indicators': [
                    'tek başına', 'yalnız', 'kimsem yok', 'tek kişi'
                ],
                'elderly_indicators': [
                    'yaşlı', 'emekli', 'büyük', 'ihtiyar', 'nine', 'dede'
                ]
            },

            'economic_status': {
                'financial_stress': [
                    'para', 'maaş', 'geçim', 'borç', 'kredi', 'fatura',
                    'pahalı', 'masraf', 'bütçe', 'ekonomik'
                ],
                'property_ownership': [
                    'ev sahibi', 'malik', 'mülk', 'apartman', 'daire',
                    'kiracı', 'kira', 'emlak'
                ]
            },

            'education_level': {
                'high_education': [
                    'üniversite', 'doktor', 'mühendis', 'öğretmen',
                    'araştırma', 'proje', 'analiz', 'değerlendirme'
                ],
                'formal_language': [
                    'müsaade', 'takdir', 'arz', 'istirham', 'maruzat',
                    'gereği', 'münasip', 'tensib'
                ]
            },

            'civic_engagement': {
                'active_citizen': [
                    'hak', 'görev', 'sorumluluk', 'demokrasi', 'katılım',
                    'önceden', 'defalarca', 'takip', 'başvuru'
                ],
                'community_awareness': [
                    'mahalle', 'komşu', 'herkes', 'tüm', 'genel', 'ortak'
                ]
            }
        }

    def analyze_social_profile(self, text: str) -> Dict:
        """Sosyal profil analizi"""
        text_lower = text.lower()

        profile_scores = defaultdict(int)
        detected_signals = defaultdict(list)

        # Her kategori için sinyal topla
        for category, subcategories in self.social_indicators.items():
            for subcategory, keywords in subcategories.items():
                for keyword in keywords:
                    if keyword in text_lower:
                        profile_scores[f"{category}_{subcategory}"] += 1
                        detected_signals[f"{category}_{subcategory}"].append(keyword)

        # Profil çıkarımları
        inferred_profile = self._infer_citizen_profile(profile_scores, detected_signals)

        return {
            'raw_scores': dict(profile_scores),
            'detected_signals': dict(detected_signals),
            'inferred_profile': inferred_profile,
            'social_confidence': self._calculate_social_confidence(profile_scores)
        }

    def _infer_citizen_profile(self, scores: Dict, signals: Dict) -> Dict:
        """Sosyal profil çıkarımı"""
        profile = {
            'age_group': 'unknown',
            'family_status': 'unknown',
            'economic_level': 'unknown',
            'education_level': 'unknown',
            'civic_engagement': 'unknown'
        }

        # Yaş grubu çıkarımı
        if scores.get('family_status_elderly_indicators', 0) > 0:
            profile['age_group'] = 'elderly'
        elif scores.get('family_status_has_family', 0) > 0:
            profile['age_group'] = 'middle_aged'
        elif 'öğrenci' in str(signals):
            profile['age_group'] = 'young'

        # Aile durumu
        if scores.get('family_status_has_family', 0) > 0:
            profile['family_status'] = 'has_family'
        elif scores.get('family_status_single_indicators', 0) > 0:
            profile['family_status'] = 'single'

        # Eğitim seviyesi
        if scores.get('education_level_high_education', 0) > 0:
            profile['education_level'] = 'high'
        elif scores.get('education_level_formal_language', 0) > 0:
            profile['education_level'] = 'medium'
        else:
            profile['education_level'] = 'basic'

        # Ekonomik durum
        if scores.get('economic_status_financial_stress', 0) > 2:
            profile['economic_level'] = 'low'
        elif scores.get('economic_status_property_ownership', 0) > 0:
            profile['economic_level'] = 'middle_high'
        else:
            profile['economic_level'] = 'middle'

        # Sivil katılım
        if scores.get('civic_engagement_active_citizen', 0) > 1:
            profile['civic_engagement'] = 'high'
        elif scores.get('civic_engagement_community_awareness', 0) > 0:
            profile['civic_engagement'] = 'medium'
        else:
            profile['civic_engagement'] = 'low'

        return profile

    def _calculate_social_confidence(self, scores: Dict) -> float:
        """Sosyal analiz güven skoru"""
        total_signals = sum(scores.values())
        if total_signals == 0:
            return 0.1

        # Çeşitlilik bonusu (farklı kategorilerden sinyal)
        categories = set(key.split('_')[0] for key in scores.keys())
        diversity_bonus = len(categories) * 0.15

        base_confidence = min(total_signals / 10.0, 0.8)  # Max 0.8
        final_confidence = min(base_confidence + diversity_bonus, 1.0)

        return round(final_confidence, 3)