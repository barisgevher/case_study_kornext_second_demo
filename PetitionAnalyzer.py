import re
from collections import defaultdict
from typing import Dict, List, Counter

from EmotionalMomentumTracker import EmotionalMomentumTracker
from SemanticSignal import SkepticalInferenceEngine
from SkepticalValidator import SkepticalValidator
from SocialSignalAnalyzer import SocialSignalAnalyzer


class PetitionAnalyzer:
    """
    🚀 Ana Yaratıcı Dilekçe Analizörü

    ÇKŞÇM'yi birleştiren master sınıf
    """

    def __init__(self):
        self.inference_engine = SkepticalInferenceEngine()
        self.emotional_tracker = EmotionalMomentumTracker()
        self.social_analyzer = SocialSignalAnalyzer()
        self.validator = SkepticalValidator()

        # Analiz istatistikleri
        self.analysis_history = []
        self.performance_metrics = {
            'total_analyzed': 0,
            'high_confidence_results': 0,
            'validation_failures': 0,
            'average_processing_time': 0.0
        }

    def analyze_petition_creative(self, text: str) -> Dict:
        """
        🎯 Ana yaratıcı analiz fonksiyonu

        WORKFLOW:
        1. Çoklu katmanlı bilgi çıkarımı
        2. Duygusal momentum takibi
        3. Sosyal sinyal analizi
        4. Şüpheci doğrulama
        5. Sonuçları birleştirme ve güvenilirlik skoru
        """
        import time
        start_time = time.time()

        # 📝 Preprocessing
        sentences = self._smart_sentence_split(text)

        # 🎯 Katman 1: Çoklu Yöntem Bilgi Çıkarımı
        extraction_results = self._multi_method_extraction(text, sentences)

        # 🎭 Katman 2: Duygusal Momentum Analizi
        emotional_analysis = self.emotional_tracker.calculate_emotional_flow(sentences)

        # 🧑‍🤝‍🧑 Katman 3: Sosyal Profil Analizi
        social_analysis = self.social_analyzer.analyze_social_profile(text)

        # 🔍 Katman 4: Şüpheci Doğrulama
        validation_results = self.validator.validate_extraction(extraction_results, text)

        # 🧠 Katman 5: Yaratıcı Sentez ve Çıkarım
        creative_insights = self._generate_creative_insights(
            extraction_results, emotional_analysis, social_analysis, validation_results
        )

        # ⚡ Performance tracking
        processing_time = time.time() - start_time
        self._update_performance_metrics(processing_time, validation_results)

        # 📊 Final Result Assembly
        final_result = {
            "metadata": {
                "analysis_timestamp": time.time(),
                "processing_time_seconds": round(processing_time, 4),
                "algorithm_version": "ÇKŞÇM_v1.0",
                "confidence_level": self._calculate_overall_confidence(
                    extraction_results, validation_results, emotional_analysis
                )
            },

            "extracted_information": extraction_results,

            "emotional_intelligence": {
                "momentum_analysis": emotional_analysis,
                "dominant_emotion": emotional_analysis['dominant_overall'],
                "emotional_stability": emotional_analysis['emotional_stability'],
                "predicted_citizen_state": self._predict_citizen_psychological_state(emotional_analysis)
            },

            "social_intelligence": {
                "citizen_profile": social_analysis['inferred_profile'],
                "social_signals": social_analysis['detected_signals'],
                "engagement_level": self._calculate_engagement_level(social_analysis)
            },

            "validation_report": {
                "overall_validity": validation_results['overall_validity'],
                "quality_score": validation_results['quality_score'],
                "red_flags": validation_results['red_flags'],
                "confidence_adjustment": validation_results['confidence_adjustment']
            },

            "creative_insights": creative_insights,

            "actionable_recommendations": self._generate_actionable_recommendations(
                extraction_results, emotional_analysis, social_analysis, creative_insights
            )
        }

        # Save to history
        self.analysis_history.append(final_result)

        return final_result

    def _smart_sentence_split(self, text: str) -> List[str]:
        """Akıllı cümle bölme - Türkçe'ye özel"""
        # Standart noktalama ile böl
        sentences = re.split(r'[.!?]+', text)

        # Boş cümleleri temizle ve kısa olanları birleştir
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Çok kısa cümleler (<5 kelime) bir öncekiyle birleştirilir
                if len(sentence.split()) < 5 and cleaned_sentences:
                    cleaned_sentences[-1] += ". " + sentence
                else:
                    cleaned_sentences.append(sentence)

        return cleaned_sentences

    def _multi_method_extraction(self, text: str, sentences: List[str]) -> Dict:
        """Çoklu yöntemle bilgi çıkarımı"""

        results = {
            'person_name': None,
            'address_info': None,
            'institution': None,
            'subject_category': None,
            'urgency_level': None,
            'request_type': None,
            'extraction_methods': {},
            'cross_validation_score': 0.0
        }

        # 👤 İsim Çıkarımı - 3 farklı yöntem
        name_candidates = []

        # Yöntem 1: Pattern matching
        for pattern in self.inference_engine.core_patterns['person_identity']['signature_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            name_candidates.extend(matches)

        # Yöntem 2: Bağlam analizi
        context_clues = self.inference_engine.core_patterns['person_identity']['context_clues']
        for sentence in sentences:
            if any(clue in sentence.lower() for clue in context_clues):
                # Bu cümlede isim ara
                potential_names = re.findall(r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\b', sentence)
                name_candidates.extend(potential_names)

        # Yöntem 3: Pozisyonel analiz (son cümle, imza alanı)
        if sentences:
            last_sentence = sentences[-1]
            signature_names = re.findall(r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][A-Z]*[a-zçğıöşü]+\b', last_sentence)
            name_candidates.extend(signature_names)

        # En iyi isim adayını seç
        if name_candidates:
            # Frekans + uzunluk bazlı seçim
            name_scores = Counter(name_candidates)
            best_name = max(name_scores, key=lambda x: (name_scores[x], len(x)))
            results['person_name'] = best_name
            results['extraction_methods']['name'] = {
                'candidates': list(set(name_candidates)),
                'selected': best_name,
                'confidence': min(name_scores[best_name] / len(name_candidates), 1.0)
            }

        # 📍 Adres Bilgisi - Hiyerarşik çıkarım
        address_components = {}

        for level, patterns in self.inference_engine.core_patterns['location_hierarchy'].items():
            if level != 'address_indicators':
                matches = []
                for pattern in patterns:
                    found = re.findall(pattern, text, re.IGNORECASE)
                    matches.extend(found)

                if matches:
                    address_components[level] = max(matches, key=len)  # En uzun eşleşmeyi al

        # Adres bileşenlerini birleştir
        if address_components:
            address_parts = []
            priority_order = ['street_patterns', 'neighborhood_patterns', 'district_patterns']
            for level in priority_order:
                if level in address_components:
                    address_parts.append(address_components[level])

            results['address_info'] = ' / '.join(address_parts)
            results['extraction_methods']['address'] = address_components

        # 🏛️ Kurum Tespiti
        institution_candidates = []

        for authority_type, patterns in self.inference_engine.core_patterns['authority_recognition'].items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                institution_candidates.extend(matches)

        if institution_candidates:
            # En sık geçen kurumu seç
            institution_scores = Counter(institution_candidates)
            results['institution'] = max(institution_scores, key=institution_scores.get)

        # 🎯 Konu Kategorisi - Gelişmiş sınıflandırma
        category_scores = self._advanced_category_classification(text, sentences)
        if category_scores:
            results['subject_category'] = max(category_scores, key=category_scores.get)
            results['extraction_methods']['category'] = category_scores

        # ⚡ Aciliyet Seviyesi - Momentum bazlı
        urgency_analysis = self._analyze_urgency_with_momentum(text, sentences)
        results['urgency_level'] = urgency_analysis['level']
        results['extraction_methods']['urgency'] = urgency_analysis

        # 📝 Talep Türü
        request_analysis = self._classify_request_type(text)
        results['request_type'] = request_analysis['type']

        # Cross-validation score
        results['cross_validation_score'] = self._calculate_cross_validation_score(results)

        return results

    def _advanced_category_classification(self, text: str, sentences: List[str]) -> Dict:
        """Gelişmiş konu sınıflandırması"""

        # Genişletilmiş kategori sözlüğü
        advanced_categories = {
            'yol_ulaşim': {
                'primary': ['yol', 'asfalt', 'kaldırım', 'çukur', 'bozuk'],
                'secondary': ['trafik', 'kavşak', 'işaret', 'geçit', 'otobüs'],
                'context': ['araç', 'yürüme', 'ulaşım', 'geçiş']
            },
            'su_kanalizasyon': {
                'primary': ['su', 'kanalizasyon', 'atık', 'tıkanık', 'akıt'],
                'secondary': ['pis su', 'içme suyu', 'kesinti', 'basma'],
                'context': ['musluk', 'boru', 'sızıntı', 'taşma']
            },
            'cevre_temizlik': {
                'primary': ['çöp', 'kirli', 'temizlik', 'süpür', 'hijyen'],
                'secondary': ['atık', 'konteyner', 'toplama', 'koku'],
                'context': ['böcek', 'fare', 'hijyen', 'sağlık']
            },
            'gurultu_rahatsizlik': {
                'primary': ['gürültü', 'ses', 'rahatsız', 'müzik', 'bağır'],
                'secondary': ['hoparlör', 'çığlık', 'patırtı', 'gürültücü'],
                'context': ['uyku', 'dinlenmek', 'sessizlik', 'huzur']
            },
            'aydinlatma': {
                'primary': ['ışık', 'aydınlatma', 'karanlık', 'lamba'],
                'secondary': ['sokak lambası', 'projektör', 'ampul'],
                'context': ['gece', 'görme', 'güvenlik', 'korku']
            },
            'park_yesil_alan': {
                'primary': ['park', 'bahçe', 'yeşil', 'ağaç', 'çiçek'],
                'secondary': ['peyzaj', 'çimen', 'oyun alanı', 'bank'],
                'context': ['çocuk', 'dinlenmek', 'spor', 'doğa']
            },
            'guvenlik': {
                'primary': ['güvenlik', 'hırsız', 'tehlike', 'korku'],
                'secondary': ['suç', 'kamera', 'bekçi', 'polis'],
                'context': ['emniyet', 'can', 'mal', 'güven']
            }
        }

        text_lower = text.lower()
        category_scores = defaultdict(float)

        for category, keywords in advanced_categories.items():
            score = 0.0

            # Primary keywords (yüksek ağırlık)
            for keyword in keywords['primary']:
                count = text_lower.count(keyword)
                score += count * 3.0

            # Secondary keywords (orta ağırlık)
            for keyword in keywords['secondary']:
                count = text_lower.count(keyword)
                score += count * 2.0

            # Context keywords (düşük ağırlık ama sinerjik)
            context_score = 0
            for keyword in keywords['context']:
                if keyword in text_lower:
                    context_score += 1

            # Context bonus (ana kelimelerle birlikte varsa)
            if score > 0 and context_score > 0:
                score *= (1 + context_score * 0.2)

            if score > 0:
                category_scores[category] = score

        return dict(category_scores)

    def _analyze_urgency_with_momentum(self, text: str, sentences: List[str]) -> Dict:
        """Momentum bazlı aciliyet analizi"""

        urgency_keywords = {
            'critical': ['acil', 'hemen', 'derhal', 'ivedi', 'can', 'tehlike', 'ölüm'],
            'high': ['bir an önce', 'çok önemli', 'yakın zamanda', 'mümkün olan'],
            'medium': ['uygun gördüğünüzde', 'zamanınız olduğunda', 'müsait'],
            'low': ['fırsat bulduğunuzda', 'boş vakit', 'acele yok']
        }

        text_lower = text.lower()
        urgency_scores = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}

        # Temel kelime sayımı
        for level, keywords in urgency_keywords.items():
            for keyword in keywords:
                count = text_lower.count(keyword)
                urgency_scores[level] += count

        # Momentum etkisi - tekrarlanan vurgu
        repetition_patterns = ['tekrar', 'yine', 'gene', 'defalarca', 'sürekli']
        repetition_score = sum(1 for pattern in repetition_patterns if pattern in text_lower)

        if repetition_score > 0:
            # Mevcut aciliyet skorunu artır
            max_urgency = max(urgency_scores, key=urgency_scores.get)
            urgency_scores[max_urgency] *= (1 + repetition_score * 0.3)

        # Büyük harf ve ünlem etkisi
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        exclamation_count = text.count('!')

        emotional_amplifier = 1 + (caps_ratio * 2) + (exclamation_count * 0.2)

        # En yüksek skoru bul ve amplifier uygula
        if urgency_scores:
            max_urgency = max(urgency_scores, key=urgency_scores.get)
            urgency_scores[max_urgency] *= emotional_amplifier

        # Final level determination
        final_level = max(urgency_scores, key=urgency_scores.get) if any(urgency_scores.values()) else 'medium'

        return {
            'level': final_level,
            'scores': urgency_scores,
            'repetition_score': repetition_score,
            'emotional_amplifier': round(emotional_amplifier, 2),
            'confidence': min(max(urgency_scores.values()) / 10.0, 1.0)
        }

    def _classify_request_type(self, text: str) -> Dict:
        """Talep türü sınıflandırması"""

        request_patterns = {
            'cozum_talebi': [
                'çözülmesini', 'giderilmesini', 'yapılmasını', 'düzeltilmesini',
                'halledelim', 'çözüm', 'tamir', 'onar'
            ],
            'bilgi_talebi': [
                'bilgi', 'açıklama', 'ne zaman', 'nasıl', 'neden', 'niçin',
                'öğrenmek', 'soruyorum', 'merak'
            ],
            'denetim_talebi': [
                'denetim', 'kontrol', 'inceleme', 'araştırma', 'müfettiş',
                'kontrol et', 'incele', 'araştır'
            ],
            'sikayet': [
                'şikayetim', 'şikayet', 'rahatsızım', 'memnun değilim',
                'eleştirim', 'itirazım', 'protesto'
            ],
            'oneri': [
                'önerim', 'öneriyorum', 'teklif', 'öneri', 'fikrim',
                'düşüncum', 'tavsiye'
            ],
            'tesekkur': [
                'teşekkür', 'sağ ol', 'minnettarım', 'takdir',
                'memnunum', 'övgü'
            ]
        }

        text_lower = text.lower()
        request_scores = {}

        for req_type, patterns in request_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text_lower)
            if score > 0:
                request_scores[req_type] = score

        if request_scores:
            primary_type = max(request_scores, key=request_scores.get)
        else:
            primary_type = 'genel_basvuru'

        return {
            'type': primary_type,
            'scores': request_scores,
            'confidence': max(request_scores.values()) / 5.0 if request_scores else 0.3
        }

    def _calculate_cross_validation_score(self, results: Dict) -> float:
        """Çapraz doğrulama skoru"""

        # Çıkarılan bilgi sayısı
        extracted_fields = sum(1 for value in results.values() if value and isinstance(value, str))

        # Method confidence'larının ortalaması
        method_confidences = []
        if 'extraction_methods' in results:
            for method_data in results['extraction_methods'].values():
                if isinstance(method_data, dict) and 'confidence' in method_data:
                    method_confidences.append(method_data['confidence'])

        avg_method_confidence = sum(method_confidences) / len(method_confidences) if method_confidences else 0.5

        # Field coverage score (0-1)
        field_coverage = extracted_fields / 6.0  # 6 ana alan var

        # Final cross-validation score
        cross_val_score = (avg_method_confidence * 0.6) + (field_coverage * 0.4)

        return round(cross_val_score, 3)

    def _generate_creative_insights(self, extraction: Dict, emotional: Dict, social: Dict, validation: Dict) -> Dict:
        """Yaratıcı içgörüler üretimi"""

        insights = {
            'citizen_urgency_profile': None,
            'communication_style_analysis': None,
            'predicted_satisfaction_level': None,
            'institutional_response_recommendation': None,
            'risk_assessment': None
        }

        # 🎯 Citizen Urgency Profile
        urgency_level = extraction.get('urgency_level', 'medium')
        emotional_state = emotional['dominant_overall']

        if urgency_level == 'critical' and emotional_state == 'anger':
            insights['citizen_urgency_profile'] = "Yüksek riskli acil müdahale gerektiren profil"
        elif urgency_level == 'high' and emotional_state == 'desperation':
            insights['citizen_urgency_profile'] = "Çaresizlik gösteren öncelikli müdahale profili"
        else:
            insights['citizen_urgency_profile'] = "Standart işlem sırası uygun profil"

        # 🎭 Communication Style Analysis
        formality = 'formal' if any(word in extraction.get('person_name', '').lower()
                                    for word in ['saygı', 'arz', 'takdir']) else 'informal'

        insights['communication_style_analysis'] = {
            'style': formality,
            'emotional_intensity': emotional['final_momentum'],
            'social_awareness': social['social_confidence'],
            'recommended_response_tone': self._recommend_response_tone(formality, emotional_state)
        }

        # 📊 Predicted Satisfaction Level
        quality_score = validation['quality_score']
        social_engagement = social['inferred_profile'].get('civic_engagement', 'medium')

        satisfaction_prediction = self._predict_satisfaction(quality_score, social_engagement, emotional_state)
        insights['predicted_satisfaction_level'] = satisfaction_prediction

        # 🏛️ Institutional Response Recommendation
        insights['institutional_response_recommendation'] = self._generate_response_recommendation(
            extraction, emotional, social
        )

        # ⚠️ Risk Assessment
        insights['risk_assessment'] = self._assess_escalation_risk(
            urgency_level, emotional_state, social_engagement, quality_score
        )

        return insights

    def _recommend_response_tone(self, citizen_formality: str, emotional_state: str) -> str:
        """Yanıt tonu önerisi"""

        tone_matrix = {
            ('formal', 'anger'): 'Formal ve sakinleştirici',
            ('formal', 'desperation'): 'Formal ve destekleyici',
            ('formal', 'politeness'): 'Formal ve takdir edici',
            ('informal', 'anger'): 'Samimi ve empati kuran',
            ('informal', 'desperation'): 'Sıcak ve çözüm odaklı',
            ('informal', 'politeness'): 'Samimi ve teşekkür eden'
        }

        return tone_matrix.get((citizen_formality, emotional_state), 'Profesyonel ve anlayışlı')

    def _predict_satisfaction(self, quality_score: float, engagement_level: str, emotional_state: str) -> Dict:
        """Memnuniyet tahmini"""

        base_satisfaction = quality_score * 0.6

        # Engagement bonus/penalty
        engagement_modifier = {
            'high': 0.2, 'medium': 0.0, 'low': -0.1
        }.get(engagement_level, 0.0)

        # Emotional state modifier
        emotional_modifier = {
            'anger': -0.3, 'desperation': -0.2, 'frustration': -0.15,
            'politeness': 0.1, 'neutral': 0.0
        }.get(emotional_state, 0.0)

        final_satisfaction = max(0.1, min(1.0, base_satisfaction + engagement_modifier + emotional_modifier))

        return {
            'predicted_score': round(final_satisfaction, 3),
            'satisfaction_level': 'high' if final_satisfaction > 0.7 else
            'medium' if final_satisfaction > 0.4 else 'low',
            'factors': {
                'quality_impact': quality_score * 0.6,
                'engagement_impact': engagement_modifier,
                'emotional_impact': emotional_modifier
            }
        }

    def _generate_response_recommendation(self, extraction: Dict, emotional: Dict, social: Dict) -> Dict:
        """Kurumsal yanıt önerisi"""

        recommendations = {
            'response_priority': 'medium',
            'suggested_timeline': '5-7 işgünü',
            'recommended_actions': [],
            'communication_approach': 'standard'
        }

        # Aciliyet bazlı öncelik
        urgency = extraction.get('urgency_level', 'medium')
        if urgency == 'critical':
            recommendations['response_priority'] = 'critical'
            recommendations['suggested_timeline'] = '24 saat içinde'
            recommendations['recommended_actions'].append('Acil müdahale ekibi ataması')
        elif urgency == 'high':
            recommendations['response_priority'] = 'high'
            recommendations['suggested_timeline'] = '48-72 saat içinde'

        # Duygusal durum bazlı yaklaşım
        emotion = emotional['dominant_overall']
        if emotion == 'anger':
            recommendations['communication_approach'] = 'empathetic_deescalation'
            recommendations['recommended_actions'].append('Kişisel görüşme teklifi')
        elif emotion == 'desperation':
            recommendations['communication_approach'] = 'supportive_solution_focused'
            recommendations['recommended_actions'].append('Ara çözüm önerisi sunma')

        # Sosyal profil bazlı ek öneriler
        civic_engagement = social['inferred_profile'].get('civic_engagement', 'medium')
        if civic_engagement == 'high':
            recommendations['recommended_actions'].append('Detaylı süreç bilgilendirmesi')

        return recommendations

    def _assess_escalation_risk(self, urgency: str, emotion: str, engagement: str, quality: float) -> Dict:
        """Tırmanma riski değerlendirmesi"""

        risk_score = 0.0
        risk_factors = []

        # Aciliyet riski
        urgency_risk = {'critical': 0.4, 'high': 0.3, 'medium': 0.1, 'low': 0.0}.get(urgency, 0.1)
        risk_score += urgency_risk

        # Duygusal risk
        emotion_risk = {'anger': 0.4, 'frustration': 0.3, 'desperation': 0.2}.get(emotion, 0.0)
        risk_score += emotion_risk

        if emotion_risk > 0.2:
            risk_factors.append(f"Yüksek duygusal gerilim: {emotion}")

        # Engagement riski (yüksek engagement = yüksek beklenti)
        if engagement == 'high':
            risk_score += 0.2
            risk_factors.append("Yüksek sivil farkındalık - detaylı yanıt beklentisi")

        # Kalite riski
        if quality < 0.5:
            risk_score += 0.3
            risk_factors.append("Düşük çıkarım kalitesi - yanlış anlama riski")

        risk_level = 'critical' if risk_score > 0.8 else \
            'high' if risk_score > 0.6 else \
                'medium' if risk_score > 0.4 else 'low'

        return {
            'risk_score': round(risk_score, 3),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'mitigation_suggestions': self._suggest_risk_mitigation(risk_level, risk_factors)
        }

    def _suggest_risk_mitigation(self, risk_level: str, factors: List[str]) -> List[str]:
        """Risk azaltma önerileri"""

        suggestions = []

        if risk_level in ['critical', 'high']:
            suggestions.append("Üst yönetim bilgilendirilmeli")
            suggestions.append("24 saat içinde ilk geri bildirim verilmeli")

        if 'duygusal gerilim' in ' '.join(factors):
            suggestions.append("Empati kuran dil kullanılmalı")
            suggestions.append("Kişisel iletişim tercih edilmeli")

        if 'sivil farkındalık' in ' '.join(factors):
            suggestions.append("Detaylı süreç açıklaması yapılmalı")
            suggestions.append("Düzenli güncelleme sağlanmalı")

        if 'yanlış anlama' in ' '.join(factors):
            suggestions.append("Çıkarımlar manuel kontrol edilmeli")
            suggestions.append("Ek bilgi talep edilmeli")

        return suggestions

    def _generate_actionable_recommendations(self, extraction: Dict, emotional: Dict, social: Dict, insights: Dict) -> \
    List[Dict]:
        """Eyleme yönelik öneriler"""

        recommendations = []

        # 1. Aciliyet bazlı eylem önerisi
        urgency = extraction.get('urgency_level', 'medium')
        if urgency in ['critical', 'high']:
            recommendations.append({
                'action': 'immediate_response',
                'priority': 'P1',
                'timeline': '24-48 saat',
                'description': 'Acil müdahale gerekli - öncelikli işlem',
                'responsible_unit': 'İlgili teknik birim + üst yönetim'
            })

        # 2. Duygusal müdahale önerisi
        if emotional['dominant_overall'] == 'anger':
            recommendations.append({
                'action': 'emotional_deescalation',
                'priority': 'P2',
                'timeline': 'İlk yanıtta',
                'description': 'Sakinleştirici ve empati kuran yaklaşım',
                'responsible_unit': 'Vatandaş İlişkileri'
            })

        # 3. Sosyal profil bazlı yaklaşım
        if social['inferred_profile'].get('civic_engagement') == 'high':
            recommendations.append({
                'action': 'detailed_communication',
                'priority': 'P2',
                'timeline': 'Süreç boyunca',
                'description': 'Detaylı bilgilendirme ve düzenli güncelleme',
                'responsible_unit': 'İletişim ve Halkla İlişkiler'
            })

        # 4. Risk bazlı önlem
        risk_level = insights['risk_assessment']['risk_level']
        if risk_level in ['critical', 'high']:
            recommendations.append({
                'action': 'risk_monitoring',
                'priority': 'P1',
                'timeline': 'Sürekli',
                'description': 'Tırmanma riski takibi ve önleme',
                'responsible_unit': 'Koordinasyon Merkezi'
            })

        return recommendations

    def _calculate_overall_confidence(self, extraction: Dict, validation: Dict, emotional: Dict) -> float:
        """Genel güven skoru"""

        # Çıkarım güveni
        extraction_confidence = extraction.get('cross_validation_score', 0.5)

        # Doğrulama güveni
        validation_confidence = validation['quality_score']

        # Duygusal analiz kararlılığı
        emotional_stability = emotional['emotional_stability']

        # Ağırlıklı ortalama
        overall_confidence = (
                extraction_confidence * 0.4 +
                validation_confidence * 0.3 +
                emotional_stability * 0.3
        )

        return round(overall_confidence, 3)

    def _update_performance_metrics(self, processing_time: float, validation: Dict):
        """Performance metriklerini güncelle"""
        self.performance_metrics['total_analyzed'] += 1

        if validation['quality_score'] > 0.7:
            self.performance_metrics['high_confidence_results'] += 1

        if not validation['overall_validity']:
            self.performance_metrics['validation_failures'] += 1

        # Moving average for processing time
        total = self.performance_metrics['total_analyzed']
        current_avg = self.performance_metrics['average_processing_time']
        new_avg = ((current_avg * (total - 1)) + processing_time) / total
        self.performance_metrics['average_processing_time'] = round(new_avg, 4)

    def _predict_citizen_psychological_state(self, emotional_analysis: Dict) -> Dict:
        """Vatandaş psikolojik durum tahmini"""

        momentum = emotional_analysis['final_momentum']
        stability = emotional_analysis['emotional_stability']
        dominant = emotional_analysis['dominant_overall']

        # Psikolojik durum matrisi
        psychological_states = {
            ('anger', 'low'): 'volatile_frustrated',  # Öfkeli + Kararsız
            ('anger', 'high'): 'controlled_dissatisfied',  # Öfkeli + Kararlı
            ('desperation', 'low'): 'crisis_state',  # Çaresiz + Kararsız
            ('desperation', 'high'): 'help_seeking',  # Çaresiz + Kararlı
            ('politeness', 'high'): 'cooperative',  # Kibar + Kararlı
            ('politeness', 'low'): 'uncertain_polite',  # Kibar + Kararsız
        }

        stability_level = 'high' if stability > 0.7 else 'low'
        state_key = (dominant, stability_level)

        psychological_state = psychological_states.get(state_key, 'neutral_citizen')

        # Müdahale önerileri
        intervention_suggestions = {
            'volatile_frustrated': ['Sakinleştirici yaklaşım', 'Hızlı geri bildirim'],
            'controlled_dissatisfied': ['Detaylı açıklama', 'Yapıcı diyalog'],
            'crisis_state': ['Acil destek', 'Çözüm odaklı yaklaşım'],
            'help_seeking': ['Destekleyici tutum', 'Rehberlik sağlama'],
            'cooperative': ['Takdir etme', 'Standart süreç'],
            'uncertain_polite': ['Güven verici yaklaşım', 'Net bilgilendirme']
        }

        return {
            'psychological_state': psychological_state,
            'confidence': round(max(momentum.values()), 3),
            'stability_level': stability_level,
            'intervention_suggestions': intervention_suggestions.get(psychological_state, ['Standart yaklaşım'])
        }

    def _calculate_engagement_level(self, social_analysis: Dict) -> str:
        """Vatandaş katılım seviyesi"""

        profile = social_analysis['inferred_profile']
        confidence = social_analysis['social_confidence']

        engagement_score = 0

        # Sivil katılım göstergeleri
        if profile.get('civic_engagement') == 'high':
            engagement_score += 3
        elif profile.get('civic_engagement') == 'medium':
            engagement_score += 2

        # Eğitim seviyesi etkisi
        if profile.get('education_level') == 'high':
            engagement_score += 2
        elif profile.get('education_level') == 'medium':
            engagement_score += 1

        # Sosyal analiz güven skoru etkisi
        engagement_score += confidence * 2

        if engagement_score >= 6:
            return 'highly_engaged'
        elif engagement_score >= 4:
            return 'moderately_engaged'
        elif engagement_score >= 2:
            return 'basic_engaged'
        else:
            return 'passive_citizen'

    def get_system_statistics(self) -> Dict:
        """Sistem istatistikleri"""
        return {
            'performance_metrics': self.performance_metrics,
            'analysis_history_count': len(self.analysis_history),
            'average_confidence': round(
                sum(analysis['metadata']['confidence_level']
                    for analysis in self.analysis_history) /
                max(len(self.analysis_history), 1), 3
            ) if self.analysis_history else 0.0,
            'success_rate': round(
                (1 - self.performance_metrics['validation_failures'] /
                 max(self.performance_metrics['total_analyzed'], 1)) * 100, 1
            )
        }

    def generate_detailed_report(self, analysis_result: Dict) -> str:
        """Detaylı analiz raporu üretimi"""

        report_lines = []
        report_lines.append("🧠 ÇKŞÇM - Çok Katmanlı Şüpheci Çıkarım Motoru Raporu")
        report_lines.append("=" * 70)
        report_lines.append("")

        # Metadata
        meta = analysis_result['metadata']
        report_lines.append(f"📊 Analiz Bilgileri:")
        report_lines.append(f"  • İşlem Süresi: {meta['processing_time_seconds']} saniye")
        report_lines.append(f"  • Güven Seviyesi: %{meta['confidence_level'] * 100:.1f}")
        report_lines.append(f"  • Algoritma: {meta['algorithm_version']}")
        report_lines.append("")

        # Çıkarılan bilgiler
        extracted = analysis_result['extracted_information']
        report_lines.append(f"📋 Çıkarılan Bilgiler:")
        report_lines.append(f"  • İsim: {extracted.get('person_name', 'Tespit edilemedi')}")
        report_lines.append(f"  • Adres: {extracted.get('address_info', 'Tespit edilemedi')}")
        report_lines.append(f"  • Kurum: {extracted.get('institution', 'Tespit edilemedi')}")
        report_lines.append(f"  • Konu: {extracted.get('subject_category', 'Belirsiz')}")
        report_lines.append(f"  • Aciliyet: {extracted.get('urgency_level', 'Orta')}")
        report_lines.append(f"  • Talep Türü: {extracted.get('request_type', 'Genel')}")
        report_lines.append("")

        # Duygusal zeka
        emotional = analysis_result['emotional_intelligence']
        report_lines.append(f"🎭 Duygusal Analiz:")
        report_lines.append(f"  • Baskın Duygu: {emotional['dominant_emotion']}")
        report_lines.append(f"  • Duygusal Kararlılık: %{emotional['emotional_stability'] * 100:.1f}")
        report_lines.append(f"  • Psikolojik Durum: {emotional['predicted_citizen_state']['psychological_state']}")
        report_lines.append("")

        # Sosyal zeka
        social = analysis_result['social_intelligence']
        citizen_profile = social['citizen_profile']
        report_lines.append(f"👤 Sosyal Profil:")
        report_lines.append(f"  • Yaş Grubu: {citizen_profile.get('age_group', 'Bilinmiyor')}")
        report_lines.append(f"  • Eğitim Seviyesi: {citizen_profile.get('education_level', 'Bilinmiyor')}")
        report_lines.append(f"  • Katılım Seviyesi: {social['engagement_level']}")
        report_lines.append("")

        # Doğrulama raporu
        validation = analysis_result['validation_report']
        report_lines.append(f"✅ Doğrulama Sonuçları:")
        report_lines.append(f"  • Genel Geçerlilik: {'✓ Geçerli' if validation['overall_validity'] else '✗ Şüpheli'}")
        report_lines.append(f"  • Kalite Skoru: %{validation['quality_score'] * 100:.1f}")

        if validation['red_flags']:
            report_lines.append(f"  • ⚠️  Uyarılar: {', '.join(validation['red_flags'])}")
        report_lines.append("")

        # Yaratıcı içgörüler
        insights = analysis_result['creative_insights']
        report_lines.append(f"💡 Yaratıcı İçgörüler:")
        report_lines.append(f"  • Vatandaş Profili: {insights['citizen_urgency_profile']}")
        report_lines.append(f"  • Risk Değerlendirmesi: {insights['risk_assessment']['risk_level']} seviye")

        satisfaction = insights['predicted_satisfaction_level']
        report_lines.append(
            f"  • Tahmini Memnuniyet: %{satisfaction['predicted_score'] * 100:.1f} ({satisfaction['satisfaction_level']})")
        report_lines.append("")

        # Eylem önerileri
        recommendations = analysis_result['actionable_recommendations']
        if recommendations:
            report_lines.append(f"🎯 Eylem Önerileri:")
            for i, rec in enumerate(recommendations, 1):
                report_lines.append(f"  {i}. {rec['description']}")
                report_lines.append(f"     • Öncelik: {rec['priority']} | Süre: {rec['timeline']}")
                report_lines.append(f"     • Sorumlu: {rec['responsible_unit']}")
                report_lines.append("")

        return "\n".join(report_lines)