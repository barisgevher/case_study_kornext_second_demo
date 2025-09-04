import re
import math
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, Counter
from dataclasses import dataclass
import json

from EmotionalMomentumTracker import EmotionalMomentumTracker
from SkepticalValidator import SkepticalValidator
from SocialSignalAnalyzer import SocialSignalAnalyzer


@dataclass
class SemanticSignal:
    """Semantik sinyal verisi"""
    signal_type: str
    confidence: float
    evidence: List[str]
    position_weight: float
    context_modifier: float


class SkepticalInferenceEngine:
    """
    🔍 ÇKŞÇM - Ana Algoritma Sınıfı

    Temel Felsefe: "Güven ama doğrula"
    Her çıkarım en az 2 farklı yöntemle kontrol edilir
    """

    def __init__(self):
        # 🎯 Katman 1: Temel Pattern Kütüphanesi
        self.core_patterns = self._initialize_core_patterns()

        # 🎯 Katman 2: Bağlamsal Ağırlıklar
        self.contextual_weights = self._initialize_contextual_weights()

        # 🎯 Katman 3: Duygusal Momentum Takibi
        self.emotional_momentum = EmotionalMomentumTracker()

        # 🎯 Katman 4: Sosyal Sinyal Analizörü
        self.social_analyzer = SocialSignalAnalyzer()

        # 🎯 Katman 5: Şüpheci Doğrulayıcı
        self.skeptical_validator = SkepticalValidator()

        # İstatistikler
        self.analysis_stats = {
            'confidence_scores': [],
            'validation_failures': 0,
            'cross_validation_success': 0
        }

    def _initialize_core_patterns(self) -> Dict:
        """Çekirdek pattern kütüphanesi - Özelleştirilmiş Türkçe desenleri"""
        return {
            # 👤 İsim Tespiti - Çoklu Yöntem
            'person_identity': {
                'signature_patterns': [
                    r'saygılarım(?:la|ızla)[,\s]*([A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]{3,35})$',
                    r'(?:ben|adım|ismim)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)+)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)(?:\s+olarak|\s+adına)'
                    r'(?:adım|ismim|ben)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)(?:\s+(?:olarak|adına))'
                ],
                'context_clues': [
                    'vatandaşınız', 'sakin', 'mukim', 'ikamet', 'adına'
                ],
                'validation_patterns': [
                    r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][A-Z]*[a-zçğıöşü]+',  # Türkçe isim formatı
                ]
            },

            # 📍 Konum Analizi - Hiyerarşik Yaklaşım
            'location_hierarchy': {
                'district_patterns': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:ilçesi|İlçesi)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+/[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)'
                ],
                'neighborhood_patterns': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:mahallesi|Mahallesi|mah\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:köyü|Köyü)'
                ],
                'street_patterns': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:caddesi|Caddesi|cad\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:sokağı|Sokağı|sok\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:bulvarı|Bulvarı|blv\.)'
                ],
                'address_indicators': [
                    'yaşadığım', 'ikamet', 'oturduğum', 'evim', 'adresim'
                ]
            },

            # 🏛️ Kurum Tespiti - Otorite Tanıma
            'authority_recognition': {
                'primary_authorities': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:belediyesi|Belediyesi)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:büyükşehir|Büyükşehir)\s+(?:belediyesi|Belediyesi)'
                ],
                'secondary_authorities': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:müdürlüğü|Müdürlüğü)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:başkanlığı|Başkanlığı)'
                ],
                'authority_titles': [
                    r'sayın\s+([^,\n]{5,40})(?:,|\n)',
                    r'muhterem\s+([^,\n]{5,40})(?:,|\n)'
                ]
            }
        }

    def _initialize_contextual_weights(self) -> Dict:
        """Bağlamsal ağırlık matrisi - Kelimelerin konumsal önemi"""
        return {
            'position_multipliers': {
                'document_start': 1.5,  # İlk %20'lik kısım
                'document_middle': 1.0,  # Orta %60'lık kısım
                'document_end': 1.3,  # Son %20'lik kısım
                'sentence_start': 1.2,  # Cümle başları
                'after_punctuation': 1.1  # Noktalama sonrası
            },

            'semantic_proximity': {
                'same_sentence': 2.0,  # Aynı cümledeki kelimeler
                'adjacent_sentence': 1.5,  # Bitişik cümleler
                'same_paragraph': 1.2,  # Aynı paragraf
                'document_wide': 1.0  # Genel doküman
            },

            'urgency_amplifiers': {
                'exclamation_nearby': 1.4,  # Yakında ünlem
                'caps_lock_context': 1.6,  # Büyük harf bağlamı
                'repetition_pattern': 1.3,  # Tekrarlanan ifadeler
                'temporal_pressure': 1.8  # Zaman baskısı kelimeleri
            }
        }

