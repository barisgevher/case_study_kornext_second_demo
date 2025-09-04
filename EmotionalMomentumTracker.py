from typing import List, Dict


class EmotionalMomentumTracker:
    """
    Duygusal Momentum Takibi -> momentum = Bir cümledeki öfke bir sonrakini etkiler
    """

    def __init__(self):
        self.emotional_patterns = {
            'anger_escalation': [
                'artık', 'yeter', 'bıktım', 'dayanamıyorum', 'sınırım', 'öfke'
            ],
            'desperation_signals': [
                'çaresiz', 'yardım', 'rica', 'lutfen', 'yapalım', 'umut'
            ],
            'politeness_markers': [
                'saygı', 'nazik', 'kibarca', 'mümkün', 'uygun', 'teşekkür'
            ],
            'frustration_buildup': [
                'tekrar', 'yine', 'gene', 'defalarca', 'kaçıncı', 'sürekli'
            ]
        }

        self.momentum_weights = {
            'anger': {'decay': 0.8, 'amplify': 1.4},
            'desperation': {'decay': 0.9, 'amplify': 1.2},
            'politeness': {'decay': 0.95, 'amplify': 1.1},
            'frustration': {'decay': 0.85, 'amplify': 1.3}
        }

    def calculate_emotional_flow(self, sentences: List[str]) -> Dict:
        """Cümle bazında duygusal momentum hesaplama"""
        emotional_flow = []
        current_momentum = {'anger': 0.0, 'desperation': 0.0, 'politeness': 0.0, 'frustration': 0.0}

        for i, sentence in enumerate(sentences):
            sentence_lower = sentence.lower()
            sentence_emotions = {'anger': 0.0, 'desperation': 0.0, 'politeness': 0.0, 'frustration': 0.0}

            # Her duygu için kelimeleri say
            for emotion, keywords in self.emotional_patterns.items():
                emotion_key = emotion.split('_')[0]
                count = sum(1 for keyword in keywords if keyword in sentence_lower)

                if count > 0:
                    # Momentum katsayısıyla çarp
                    momentum_effect = current_momentum.get(emotion_key, 0) * self.momentum_weights[emotion_key][
                        'amplify']
                    sentence_emotions[emotion_key] = count + momentum_effect

            # Momentumu güncelleme
            for emotion in current_momentum:
                current_momentum[emotion] = (
                        current_momentum[emotion] * self.momentum_weights[emotion]['decay'] +
                        sentence_emotions[emotion]
                )

            emotional_flow.append({
                'sentence_index': i,
                'emotions': sentence_emotions.copy(),
                'cumulative_momentum': current_momentum.copy(),
                'dominant_emotion': max(sentence_emotions, key=sentence_emotions.get)
            })

        return {
            'sentence_flow': emotional_flow,
            'final_momentum': current_momentum,
            'dominant_overall': max(current_momentum, key=current_momentum.get),
            'emotional_stability': self._calculate_stability(emotional_flow)
        }

    def _calculate_stability(self, flow: List[Dict]) -> float:
        """durgunluk skoru ne kadar fazlaysa o kadar durgun"""
        if len(flow) < 2:
            return 1.0

        variations = []
        for i in range(1, len(flow)):
            prev_emotions = flow[i - 1]['emotions']
            curr_emotions = flow[i]['emotions']

            # Cümleler arası değişim miktarı
            variation = sum(abs(curr_emotions[e] - prev_emotions[e]) for e in curr_emotions) / len(curr_emotions)
            variations.append(variation)

        avg_variation = sum(variations) / len(variations)
        stability = max(0, 1 - (avg_variation / 5))

        return round(stability, 3)