import re
from collections import defaultdict, Counter
from typing import Dict, List

from src.emotional_momentum_tracker import EmotionalMomentumTracker
from src.enhanced_skeptical_validator import EnhancedSkepticalValidator
from src.semantic_signal import SkepticalInferenceEngine
from src.validator import SkepticalValidator
from src.social_analyzer import SocialSignalAnalyzer


class PetitionAnalyzer:
    """
     Ana Yaratıcı Dilekçe Analizörü
    tüm alhoritmaları süpheci yaklaşımları birleştiren master sınıf

    """

    def __init__(self):
        self.inference_engine = SkepticalInferenceEngine()
        self.emotional_tracker = EmotionalMomentumTracker()
        self.social_analyzer = SocialSignalAnalyzer()
        self.validator = SkepticalValidator()
        self.enhanced_validator = EnhancedSkepticalValidator()

        # Analiz istatistikleri
        self.analysis_history = []
        self.performance_metrics = {
            'total_analyzed': 0,
            'high_confidence_results': 0,
            'validation_failures': 0,
            'average_processing_time': 0.0,
            'successful_name_extractions': 0,
            'successful_subject_extractions': 0
        }

    def analyze_petition_creative(self, text: str) -> Dict:
        """
        ana yaratıcı analiz fonksiyonu

        iş akışı :
        1. bilgi çıkarımı
        2. Duygusal momentum takibi
        3. Sosyal sinyal analizi
        4. Çifte şüpheci doğrulama
        5. Sonuçları birleştirme ve güvenilirlik skoru
        """
        import time
        start_time = time.time()

        # ileri seviye ön işleme
        sentences = self._smart_sentence_split(text)

        # 1. katman : çoklu yöntem ile bilgi çıkarımı
        extraction_results = self._ultra_comprehensive_extraction(text, sentences)

        # 2. katman : duygusal momentum analizi
        emotional_analysis = self.emotional_tracker.calculate_emotional_flow(sentences)

        # 3. katman : sosyal profilleme
        social_analysis = self.social_analyzer.analyze_social_profile(text)

        # 4. katman: ilk şüpheci doğrulama
        validation_results = self.validator.validate_extraction(extraction_results, text)

        # 5. katman : gelişmiş ikinci Şüpheci Doğrulama
        enhanced_validation = self.enhanced_validator.validate_extraction(extraction_results, text)

        # 6.katman : yaratıcı sentez ve çıkarım
        creative_insights = self._generate_creative_insights(
            extraction_results, emotional_analysis, social_analysis, enhanced_validation
        )

        #  performans izleme
        processing_time = time.time() - start_time
        self._update_performance_metrics(processing_time, enhanced_validation, extraction_results)

        #  final sonucu birleştirme
        final_result = {
            "metadata": {
                "analysis_timestamp": time.time(),
                "processing_time_seconds": round(processing_time, 4),
                "algorithm_version": "rbcd-v2.0_ULTRA",
                "confidence_level": self._calculate_overall_confidence(
                    extraction_results, enhanced_validation, emotional_analysis
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
                "primary_validation": validation_results,
                "enhanced_validation": enhanced_validation,
                "overall_validity": enhanced_validation['overall_validity'],
                "quality_score": enhanced_validation['quality_score'],
                "red_flags": enhanced_validation['red_flags'],
                "confidence_adjustment": enhanced_validation['confidence_adjustment']
            },

            "creative_insights": creative_insights,

            "actionable_recommendations": self._generate_actionable_recommendations(
                extraction_results, emotional_analysis, social_analysis, creative_insights
            )
        }

        # kayıt et
        self.analysis_history.append(final_result)

        return final_result

    def _ultra_comprehensive_extraction(self, text: str, sentences: List[str]) -> Dict:
        """ kapsamlı çoklu yöntemle bilgi çıkarımı"""

        results = {
            'person_name': None,
            'address_info': None,
            'institution': None,
            'subject_category': None,
            'urgency_level': None,
            'request_type': None,
            'extraction_methods': {},
            'cross_validation_score': 0.0,
            'extraction_details': {}
        }

        # isim çıkarımı
        name_extraction = self.inference_engine.extract_names_comprehensive(text)
        if name_extraction['extracted_name']:
            results['person_name'] = name_extraction['extracted_name']
            results['extraction_methods']['name'] = name_extraction
            results['extraction_details']['name_confidence'] = name_extraction['confidence']

        # adres Bilgisi
        address_components = {}
        address_extraction = self._extract_comprehensive_address(text)

        if address_extraction['full_address']:
            results['address_info'] = address_extraction['full_address']
            results['extraction_methods']['address'] = address_extraction
            results['extraction_details']['address_confidence'] = address_extraction['confidence']

        # kurum kuruluş tespiti
        institution_extraction = self._extract_comprehensive_institution(text)
        if institution_extraction['institution']:
            results['institution'] = institution_extraction['institution']
            results['extraction_methods']['institution'] = institution_extraction

        # konu kategorisi sınıflandırması
        category_analysis = self._ultra_comprehensive_category_classification(text, sentences)
        if category_analysis['primary_category']:
            results['subject_category'] = category_analysis['primary_category']
            results['extraction_methods']['category'] = category_analysis
            results['extraction_details']['category_confidence'] = category_analysis['confidence']

        # aciliyet seviyesi  duygu analizi momentum ile
        urgency_analysis = self._analyze_urgency_with_momentum(text, sentences)
        results['urgency_level'] = urgency_analysis['level']
        results['extraction_methods']['urgency'] = urgency_analysis

        # detaylı talep türü analizi
        request_analysis = self._classify_request_type_detailed(text)
        results['request_type'] = request_analysis['type']
        results['extraction_methods']['request_type'] = request_analysis

        # cross validation skoru
        results['cross_validation_score'] = self._calculate_cross_validation_score(results)

        return results

    def _extract_comprehensive_address(self, text: str) -> Dict:
        """Kapsamlı adres çıkarımı"""

        address_components = {
            'street': None,
            'neighborhood': None,
            'district': None,
            'city': None,
            'full_address': None,
            'confidence': 0.0,
            'extraction_method': None
        }

        #  adres bileşenlerinin çıkarımı
        for level, patterns in self.inference_engine.core_patterns['location_hierarchy'].items():
            if level != 'address_indicators':
                matches = []
                for pattern in patterns:
                    found = re.findall(pattern, text, re.IGNORECASE)
                    matches.extend(found)

                if matches:
                    # en uzun ve en detaylı eşleşmeyi al
                    best_match = max(matches, key=lambda x: len(str(x)) if isinstance(x, str) else len(str(x[0])))
                    if isinstance(best_match, tuple):
                        best_match = best_match[0]

                    address_components[level.replace('_patterns', '')] = best_match.strip()

        # adresi birleştir
        address_parts = []
        priority_order = ['street', 'neighborhood', 'district', 'city']

        for component in priority_order:
            if address_components.get(component):
                address_parts.append(address_components[component])

        if address_parts:
            address_components['full_address'] = ' / '.join(address_parts)
            address_components['confidence'] = min(len(address_parts) / 4.0, 1.0)
            address_components['extraction_method'] = 'hierarchical_pattern_matching'

        # bağlamsal adres arama
        if not address_components['full_address']:
            context_address = self._extract_contextual_address(text)
            if context_address:
                address_components.update(context_address)

        return address_components

    def _extract_contextual_address(self, text: str) -> Dict:
        """bağlamsal adres çıkarımı"""

        address_indicators = self.inference_engine.core_patterns['location_hierarchy']['address_indicators']

        for indicator in address_indicators:
            if indicator in text.lower():
                pattern = rf'{indicator}.*?([A-ZÇĞİÖŞÜ][a-zçğıöşü\s/,-]+(?:mahallesi|sokağı|caddesi|bulvarı|ilçesi).*?)(?:\.|,|$)'
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

                if matches:
                    return {
                        'full_address': matches[0].strip(),
                        'confidence': 0.6,
                        'extraction_method': 'contextual_indicator'
                    }

        return {}

    def _extract_comprehensive_institution(self, text: str) -> Dict:
        """ kurum kuruluş çıkarımı"""

        institution_candidates = []
        extraction_details = {
            'institution': None,
            'confidence': 0.0,
            'authority_level': None,
            'extraction_method': None
        }

        # yetkili çıkarımı
        for authority_type, patterns in self.inference_engine.core_patterns['authority_recognition'].items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0]

                        institution_candidates.append({
                            'name': match.strip(),
                            'level': authority_type,
                            'confidence': 0.9 if authority_type == 'primary_authorities' else 0.7
                        })

        if institution_candidates:
            # en yüksek confiadance skoruna sahip olanı seç
            best_institution = max(institution_candidates, key=lambda x: x['confidence'])
            extraction_details = {
                'institution': best_institution['name'],
                'confidence': best_institution['confidence'],
                'authority_level': best_institution['level'],
                'extraction_method': 'pattern_matching',
                'all_candidates': institution_candidates
            }

        return extraction_details

    def _ultra_comprehensive_category_classification(self, text: str, sentences: List[str]) -> Dict:
        """konu sınıflandırması"""

        text_lower = text.lower()
        category_scores = defaultdict(float)
        category_details = {}

        #  kategoriler için puanlama yapma
        for category, keywords_dict in self.inference_engine.core_patterns['subject_categories'].items():

            score_details = {
                'primary_matches': [],
                'secondary_matches': [],
                'context_matches': [],
                'problem_matches': [],
                'total_score': 0.0
            }

            total_score = 0.0

            # birincil keywordler  en yüksek puana sahip olanlar
            for keyword in keywords_dict.get('primary_keywords', []):
                count = text_lower.count(keyword)
                if count > 0:
                    score_details['primary_matches'].append((keyword, count))
                    total_score += count * 3.0

            # ikincil keywordler orta ağırlıktakiler
            for keyword in keywords_dict.get('secondary_keywords', []):
                count = text_lower.count(keyword)
                if count > 0:
                    score_details['secondary_matches'].append((keyword, count))
                    total_score += count * 2.0

            # bağlamsal bonus hesabı
            context_score = 0
            for keyword in keywords_dict.get('context_keywords', []):
                if keyword in text_lower:
                    context_score += 1
                    score_details['context_matches'].append(keyword)

            # problem keywordleri özel bonus hesabı
            problem_score = 0
            for keyword in keywords_dict.get('problem_keywords', []):
                if keyword in text_lower:
                    problem_score += 1
                    score_details['problem_matches'].append(keyword)

            # bağlamsal ve problem bonusları
            if total_score > 0:
                if context_score > 0:
                    total_score *= (1 + context_score * 0.2)
                if problem_score > 0:
                    total_score *= (1 + problem_score * 0.15)

            # cümle içi yakınlık bonusu
            proximity_bonus = self._calculate_keyword_proximity_bonus(sentences, keywords_dict)
            total_score += proximity_bonus

            if total_score > 0:
                score_details['total_score'] = total_score
                category_scores[category] = total_score
                category_details[category] = score_details

        # en yüksek skorlu kategoriyi belirle
        result = {
            'primary_category': None,
            'confidence': 0.0,
            'all_categories': dict(category_scores),
            'category_details': category_details,
            'classification_method': 'ultra_comprehensive'
        }

        if category_scores:
            primary_category = max(category_scores, key=category_scores.get)
            max_score = category_scores[primary_category]
            total_all_scores = sum(category_scores.values())

            result.update({
                'primary_category': primary_category,
                'confidence': min(max_score / max(total_all_scores, 1), 1.0),
                'score_distribution': {cat: score / total_all_scores for cat, score in category_scores.items()}
            })

        return result

    def _calculate_keyword_proximity_bonus(self, sentences: List[str], keywords_dict: Dict) -> float:
        """anahtar kelime yakınlık bonusu hesaplama"""

        bonus = 0.0
        all_keywords = []

        for keyword_list in keywords_dict.values():
            if isinstance(keyword_list, list):
                all_keywords.extend(keyword_list)

        # her cümlede birden fazla anahtar kelime varsa
        for sentence in sentences:
            sentence_lower = sentence.lower()
            found_keywords = [kw for kw in all_keywords if kw in sentence_lower]

            if len(found_keywords) > 1:
                # Çoklu anahtar kelime bonusu
                bonus += len(found_keywords) * 0.5

                # özel kombinasyon bonusları
                if any(kw in sentence_lower for kw in ['bozuk', 'tamir', 'onar']):
                    bonus += 1.0
                if any(kw in sentence_lower for kw in ['kirli', 'temiz', 'hijyen']):
                    bonus += 1.0

        return bonus

    def _classify_request_type_detailed(self, text: str) -> Dict:
        """detaylı talep türü sınıflandırması"""

        request_patterns = {
            'acil_cozum_talebi': {
                'keywords': ['acil', 'hemen', 'derhal', 'çözülmesini', 'giderilmesini', 'yapılmasını'],
                'weight': 3.0
            },
            'normal_cozum_talebi': {
                'keywords': ['çözülmesini', 'giderilmesini', 'yapılmasını', 'düzeltilmesini', 'tamir'],
                'weight': 2.0
            },
            'bilgi_talebi': {
                'keywords': ['bilgi', 'açıklama', 'ne zaman', 'nasıl', 'neden', 'öğrenmek', 'soruyorum'],
                'weight': 2.0
            },
            'denetim_talebi': {
                'keywords': ['denetim', 'kontrol', 'inceleme', 'araştırma', 'müfettiş'],
                'weight': 2.5
            },
            'sikayet': {
                'keywords': ['şikayetim', 'şikayet', 'rahatsızım', 'memnun değilim', 'eleştirim'],
                'weight': 2.0
            },
            'oneri': {
                'keywords': ['önerim', 'öneriyorum', 'teklif', 'öneri', 'fikrim', 'tavsiye'],
                'weight': 1.5
            },
            'tesekkur_takdir': {
                'keywords': ['teşekkür', 'sağ ol', 'minnettarım', 'takdir', 'memnunum', 'övgü'],
                'weight': 1.0
            },
            'hukuki_tehdit': {
                'keywords': ['hukuki', 'yasal', 'mahkeme', 'dava', 'avukat', 'hakkımı arayacağım'],
                'weight': 3.0
            }
        }

        text_lower = text.lower()
        request_scores = {}
        detailed_matches = {}

        for req_type, config in request_patterns.items():
            matches = []
            score = 0

            for keyword in config['keywords']:
                if keyword in text_lower:
                    count = text_lower.count(keyword)
                    matches.append((keyword, count))
                    score += count * config['weight']

            if score > 0:
                request_scores[req_type] = score
                detailed_matches[req_type] = {
                    'matches': matches,
                    'score': score,
                    'weight': config['weight']
                }

        # en yüksek skorlu tipi belirle
        if request_scores:
            primary_type = max(request_scores, key=request_scores.get)
            max_score = request_scores[primary_type]
            confidence = min(max_score / 10.0, 1.0)
        else:
            primary_type = 'genel_basvuru'
            confidence = 0.3

        return {
            'type': primary_type,
            'confidence': confidence,
            'all_scores': request_scores,
            'detailed_matches': detailed_matches,
            'classification_method': 'weighted_keyword_analysis'
        }

    def _update_performance_metrics(self, processing_time: float, validation: Dict, extraction: Dict):
        """gelişmiş peformans metrikleri güncelleme"""

        self.performance_metrics['total_analyzed'] += 1

        if validation['quality_score'] > 0.7:
            self.performance_metrics['high_confidence_results'] += 1

        if not validation['overall_validity']:
            self.performance_metrics['validation_failures'] += 1

        # isim çıkarım performansı
        if extraction.get('person_name'):
            self.performance_metrics['successful_name_extractions'] += 1

        # konu çıkarım peformansı
        if extraction.get('subject_category'):
            self.performance_metrics['successful_subject_extractions'] += 1

        # ortalama çalışma zamanı
        total = self.performance_metrics['total_analyzed']
        current_avg = self.performance_metrics['average_processing_time']
        new_avg = ((current_avg * (total - 1)) + processing_time) / total
        self.performance_metrics['average_processing_time'] = round(new_avg, 4)

    def get_enhanced_system_statistics(self) -> Dict:
        """gelişmiş sistem istatistikleri"""
        total = self.performance_metrics['total_analyzed']

        return {
            'performance_metrics': self.performance_metrics,
            'analysis_history_count': len(self.analysis_history),
            'success_rates': {
                'name_extraction': round(
                    self.performance_metrics['successful_name_extractions'] / max(total, 1) * 100, 1
                ),
                'subject_extraction': round(
                    self.performance_metrics['successful_subject_extractions'] / max(total, 1) * 100, 1
                ),
                'overall_validation': round(
                    (1 - self.performance_metrics['validation_failures'] / max(total, 1)) * 100, 1
                )
            },
            'average_confidence': round(
                sum(analysis['metadata']['confidence_level']
                    for analysis in self.analysis_history) /
                max(len(self.analysis_history), 1), 3
            ) if self.analysis_history else 0.0,
            'category_distribution': self._get_category_distribution(),
            'extraction_method_performance': self._get_extraction_method_stats()
        }

    def _get_category_distribution(self) -> Dict:
        """kategori dağılımı istatistikleri"""

        categories = []
        for analysis in self.analysis_history:
            category = analysis['extracted_information'].get('subject_category')
            if category:
                categories.append(category)

        if not categories:
            return {}

        from collections import Counter
        category_counts = Counter(categories)
        total = len(categories)

        return {
            category: {
                'count': count,
                'percentage': round(count / total * 100, 1)
            }
            for category, count in category_counts.most_common()
        }

    def _get_extraction_method_stats(self) -> Dict:
        """Çıkarım yöntemleri performans istatistikleri"""

        method_stats = {
            'name_extraction_methods': defaultdict(int),
            'address_extraction_methods': defaultdict(int),
            'category_extraction_methods': defaultdict(int)
        }

        for analysis in self.analysis_history:
            extraction_methods = analysis['extracted_information'].get('extraction_methods', {})

            # isim çıkarım yöntemleri
            if 'name' in extraction_methods:
                name_methods = extraction_methods['name'].get('extraction_methods', {})
                for method, candidates in name_methods.items():
                    if candidates:
                        method_stats['name_extraction_methods'][method] += 1

            # kategori çıkarım yöntemleri
            if 'category' in extraction_methods:
                method = extraction_methods['category'].get('classification_method', 'unknown')
                method_stats['category_extraction_methods'][method] += 1

        return {key: dict(value) for key, value in method_stats.items()}


    def _smart_sentence_split(self, text: str) -> List[str]:
        """akıllı cümle ayırma """
        sentences = re.split(r'[.!?]+', text)
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if len(sentence.split()) < 5 and cleaned_sentences:
                    cleaned_sentences[-1] += ". " + sentence
                else:
                    cleaned_sentences.append(sentence)
        return cleaned_sentences

    def _analyze_urgency_with_momentum(self, text: str, sentences: List[str]) -> Dict:
        """momentum bazlı aciliyet analizi"""
        urgency_keywords = {
            'critical': ['acil', 'hemen', 'derhal', 'ivedi', 'can', 'tehlike', 'ölüm'],
            'high': ['bir an önce', 'çok önemli', 'yakın zamanda', 'mümkün olan'],
            'medium': ['uygun gördüğünüzde', 'zamanınız olduğunda', 'müsait'],
            'low': ['fırsat bulduğunuzda', 'boş vakit', 'acele yok']
        }

        text_lower = text.lower()
        urgency_scores = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}

        for level, keywords in urgency_keywords.items():
            for keyword in keywords:
                count = text_lower.count(keyword)
                urgency_scores[level] += count

        # tekrarlama  etkisi
        repetition_patterns = ['tekrar', 'yine', 'gene', 'defalarca', 'sürekli']
        repetition_score = sum(1 for pattern in repetition_patterns if pattern in text_lower)

        if repetition_score > 0:
            max_urgency = max(urgency_scores, key=urgency_scores.get)
            urgency_scores[max_urgency] *= (1 + repetition_score * 0.3)

        # büyük harf ve ünlem  etkisi
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text) if text else 0
        exclamation_count = text.count('!')
        emotional_amplifier = 1 + (caps_ratio * 2) + (exclamation_count * 0.2)

        max_urgency = max(urgency_scores, key=urgency_scores.get)
        urgency_scores[max_urgency] *= emotional_amplifier

        final_level = max_urgency if any(urgency_scores.values()) else 'medium'

        return {
            'level': final_level,
            'scores': urgency_scores,
            'repetition_score': repetition_score,
            'emotional_amplifier': round(emotional_amplifier, 2),
            'confidence': min(max(urgency_scores.values()) / 10.0, 1.0)
        }

    def _calculate_cross_validation_score(self, results: Dict) -> float:
        """çapraz doğrulama skoru"""
        extracted_fields = sum(1 for key, value in results.items()
                               if key not in ['extraction_methods', 'extraction_details']
                               and value and isinstance(value, str))

        # metodların skorlarının ortalaması
        method_confidences = []
        if 'extraction_details' in results:
            for key, value in results['extraction_details'].items():
                if 'confidence' in str(key) and isinstance(value, (int, float)):
                    method_confidences.append(value)

        avg_method_confidence = sum(method_confidences) / len(method_confidences) if method_confidences else 0.5
        field_coverage = extracted_fields / 6.0  # 6 ana alan var
        cross_val_score = (avg_method_confidence * 0.6) + (field_coverage * 0.4)
        return round(cross_val_score, 3)


    def _generate_creative_insights(self, extraction: Dict, emotional: Dict, social: Dict, validation: Dict) -> Dict:
        return {
            'citizen_urgency_profile': self._determine_urgency_profile(extraction, emotional),
            'communication_style_analysis': self._analyze_communication_style(extraction, emotional, social),
            'predicted_satisfaction_level': self._predict_satisfaction_level(validation, social, emotional),
            'institutional_response_recommendation': self._generate_response_recommendation(extraction, emotional,
                                                                                            social),
            'risk_assessment': self._assess_escalation_risk(extraction, emotional, social, validation)
        }

    def _determine_urgency_profile(self, extraction: Dict, emotional: Dict) -> str:
        urgency_level = extraction.get('urgency_level', 'medium')
        emotional_state = emotional['dominant_overall']

        if urgency_level == 'critical' and emotional_state == 'anger':
            return "Yüksek riskli acil müdahale gerektiren profil"
        elif urgency_level == 'high' and emotional_state == 'desperation':
            return "Çaresizlik gösteren öncelikli müdahale profili"
        else:
            return "Standart işlem sırası uygun profil"

    def _analyze_communication_style(self, extraction: Dict, emotional: Dict, social: Dict) -> Dict:
        return {
            'style': 'formal' if 'saygı' in str(extraction.get('person_name', '')).lower() else 'informal',
            'emotional_intensity': emotional['final_momentum'],
            'social_awareness': social['social_confidence'],
            'recommended_response_tone': 'Profesyonel ve anlayışlı'
        }

    def _predict_satisfaction_level(self, validation: Dict, social: Dict, emotional: Dict) -> Dict:
        base_satisfaction = validation['quality_score'] * 0.6
        final_satisfaction = max(0.1, min(1.0, base_satisfaction))

        return {
            'predicted_score': round(final_satisfaction, 3),
            'satisfaction_level': 'high' if final_satisfaction > 0.7 else 'medium' if final_satisfaction > 0.4 else 'low'
        }

    def _generate_response_recommendation(self, extraction: Dict, emotional: Dict, social: Dict) -> Dict:
        urgency = extraction.get('urgency_level', 'medium')

        return {
            'response_priority': 'critical' if urgency == 'critical' else 'medium',
            'suggested_timeline': '24 saat içinde' if urgency == 'critical' else '5-7 işgünü',
            'communication_approach': 'empathetic_deescalation' if emotional[
                                                                       'dominant_overall'] == 'anger' else 'standard'
        }

    def _assess_escalation_risk(self, extraction: Dict, emotional: Dict, social: Dict, validation: Dict) -> Dict:
        risk_score = 0.0
        urgency = extraction.get('urgency_level', 'medium')
        emotion = emotional['dominant_overall']

        risk_score += {'critical': 0.4, 'high': 0.3, 'medium': 0.1, 'low': 0.0}.get(urgency, 0.1)
        risk_score += {'anger': 0.4, 'frustration': 0.3, 'desperation': 0.2}.get(emotion, 0.0)

        risk_level = 'critical' if risk_score > 0.8 else 'high' if risk_score > 0.6 else 'medium' if risk_score > 0.4 else 'low'

        return {
            'risk_score': round(risk_score, 3),
            'risk_level': risk_level,
            'risk_factors': [],
            'mitigation_suggestions': ['Standart prosedür uygulanmalı']
        }

    def _generate_actionable_recommendations(self, extraction: Dict, emotional: Dict, social: Dict, insights: Dict) -> \
    List[Dict]:
        recommendations = []
        urgency = extraction.get('urgency_level', 'medium')

        if urgency in ['critical', 'high']:
            recommendations.append({
                'action': 'immediate_response',
                'priority': 'P1',
                'timeline': '24-48 saat',
                'description': 'Acil müdahale gerekli - öncelikli işlem',
                'responsible_unit': 'İlgili teknik birim + üst yönetim'
            })

        return recommendations

    def _calculate_overall_confidence(self, extraction: Dict, validation: Dict, emotional: Dict) -> float:
        extraction_confidence = extraction.get('cross_validation_score', 0.5)
        validation_confidence = validation['quality_score']
        emotional_stability = emotional['emotional_stability']

        overall_confidence = (
                extraction_confidence * 0.4 +
                validation_confidence * 0.3 +
                emotional_stability * 0.3
        )
        return round(overall_confidence, 3)

    def _predict_citizen_psychological_state(self, emotional_analysis: Dict) -> Dict:
        return {
            'psychological_state': 'neutral_citizen',
            'confidence': 0.5,
            'stability_level': 'medium',
            'intervention_suggestions': ['Standart yaklaşım']
        }

    def _calculate_engagement_level(self, social_analysis: Dict) -> str:
        return 'moderately_engaged'