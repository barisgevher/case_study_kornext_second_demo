import re
from typing import Dict, List
from dataclasses import dataclass

from src.emotional_momentum_tracker import EmotionalMomentumTracker
from src.validator import SkepticalValidator
from social_analyzer import SocialSignalAnalyzer


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
    Ana Algoritma Sınıfı
    """

    def __init__(self):
        # 1.katman :  temel pattern kütüphanesi
        self.core_patterns = self._initialize_core_patterns()

        # 2. katman: bağlamsal ağırlıklar
        self.contextual_weights = self._initialize_contextual_weights()

        # 3. katman: duygusal momentum takibi
        self.emotional_momentum = EmotionalMomentumTracker()

        # 4. katman: sosyal sinyal analizi
        self.social_analyzer = SocialSignalAnalyzer()

        # 5. katman : şüpheci doğrulayıcı
        self.skeptical_validator = SkepticalValidator()


        self.analysis_stats = {
            'confidence_scores': [],
            'validation_failures': 0,
            'cross_validation_success': 0
        }

    def  _initialize_core_patterns(self) -> Dict:
        """çekirdek pattern kütüphanesi """
        return {
            'person_identity': {
                'signature_patterns': [

                    r'saygılarım(?:la|ızla)[,\s]*([A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]{3,50})$',
                    r'saygılarımla[,\s\n]+([A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]{3,50})$',
                    r'hürmetlerimi\s+sunarım[,\s]*([A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]{3,50})$',
                    r'iyi\s+çalışmalar\s+dilerim[,\s]*([A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]{3,50})$',

                    r'(?:ben|adım|ismim)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+(?:\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)+)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)(?:\s+olarak|\s+adına)',
                    r'(?:adım|ismim|ben)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                    r'benim\s+adım\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s*/\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+/\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s*-\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:yaşıyorum|ikamet|oturuyorum)',
                    r'(?:yaşadığım|oturduğum|ikametgahım).*?([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:vatandaşınız|sakiniyim)',
                    r'vatandaşınız\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s*$',
                    r'^([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)$',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+tc:?\s*\d{11}',
                    r'tc:?\s*\d{11}\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:tel|telefon|gsm):?\s*[\d\s\-\(\)]+',

                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:emekli|öğretmen|memur|işçi|esnaf|doktor)',
                    r'(?:emekli|öğretmen|memur|işçi|esnaf|doktor)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                ],

                'context_clues': [
                    'vatandaşınız', 'sakiniyim', 'mukim', 'ikamet', 'adına', 'ben', 'benim',
                    'yaşıyorum', 'oturuyorum', 'adım', 'ismim', 'tc', 'kimlik', 'telefon'
                ],

                'validation_patterns': [
                    r'[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][A-Z]*[a-zçğıöşü]+',
                ],

                # pozisyonel ağırlıklar
                'position_weights': {
                    'document_start': 1.2,  # dokümanın başı
                    'document_end': 1.5,    # dokümanın sonu - imza
                    'after_greeting': 1.3,  # selamlamadan sonra
                    'before_signature': 1.4 # imzadan önce
                }
            },

            #  konum analizi
            'location_hierarchy': {
                'district_patterns': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:ilçesi|İlçesi)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:ilçesi|İlçesi|ilçesine|ilçemiz)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+/[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+merkez\s+ilçe',
                ],

                'neighborhood_patterns': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:mahallesi|Mahallesi|mah\.|mh\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:köyü|Köyü|kasabası)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:beldesi|Beldesi)',
                ],

                'street_patterns': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:caddesi|Caddesi|cad\.|cd\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:sokağı|Sokağı|sok\.|sk\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:bulvarı|Bulvarı|blv\.)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:meydanı|Meydanı)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:apartmanı|Apartmanı|sitesi|Sitesi)',
                    r'(\d+\.?\s+sokak)',
                    r'(\d+\.\s+cadde)',
                ],

                'address_indicators': [
                    'yaşadığım', 'ikamet', 'oturduğum', 'evim', 'adresim', 'ikametgah',
                    'mukim', 'yaşıyor', 'bulunan', 'meskun'
                ]
            },

            # kurum kuruluş tespiti
            'authority_recognition': {
                'primary_authorities': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:belediyesi|Belediyesi)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:büyükşehir|Büyükşehir)\s+(?:belediyesi|Belediyesi)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:Valiliği|Valiliğine|valiliği)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:Kaymakamlığı|Kaymakamlığına|kaymakamlığı)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:İl\s+Özel\s+İdaresi|il\s+özel\s+idaresi)',

                ],

                'secondary_authorities': [
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:müdürlüğü|Müdürlüğü)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:başkanlığı|Başkanlığı)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:Daire\s+Başkanlığı|daire\s+başkanlığı)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:Şube\s+Müdürlüğü|şube\s+müdürlüğü)',
                ],

                'authority_titles': [
                    r'sayın\s+([^,\n]{5,50})(?:,|\n)',
                    r'muhterem\s+([^,\n]{5,50})(?:,|\n)',
                    r'değerli\s+([^,\n]{5,50})(?:,|\n)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:belediye\s+başkanı|mayor)',
                    r'([A-ZÇĞİÖŞÜ][a-zçğıöşü\s]+)\s+(?:vali|kaymakam|müdür|başkan)',
                ]
            },

            # konu kategorileri
            'subject_categories': {

                'yol_ulasim': {
                    'primary_keywords': [
                        'yol', 'asfalt', 'kaldırım', 'çukur', 'bozuk', 'tamir',
                        'parke', 'kaya', 'toprak', 'stabilize', 'macadam'
                    ],
                    'secondary_keywords': [
                        'trafik', 'kavşak', 'işaret', 'geçit', 'otobüs', 'durak',
                        'park', 'otopark', 'araç', 'bisiklet', 'yürüyüş', 'kaza',
                        'tehlike', 'güvenlik', 'ışık', 'sinyal', 'rampa', 'köprü'
                    ],
                    'context_keywords': [
                        'geçiş', 'ulaşım', 'yürüme', 'araç', 'trafik', 'güzergah',
                        'rota', 'mesafe', 'erişim', 'bağlantı', 'kavşak'
                    ],
                    'problem_keywords': [
                        'çökme', 'çatlak', 'delik', 'kaygan', 'tehlikeli', 'dar',
                        'kapali', 'engelli', 'tıkalı', 'bozuk', 'yamuk', 'trafik kazası', 'trafik ışığı'
                    ]
                },


                'su_kanalizasyon': {
                    'primary_keywords': [
                        'su', 'kanalizasyon', 'atık', 'pis', 'tıkanık', 'akıt',
                        'sızıntı', 'taşma', 'koku', 'pis', 'kirli'
                    ],
                    'secondary_keywords': [
                        'içme suyu', 'şebeke', 'kesinti', 'basınç', 'kaçak',
                        'rögar', 'menhol', 'boru', 'vana', 'sayaç', 'fatura'
                    ],
                    'context_keywords': [
                        'musluk', 'lavabo', 'banyo', 'mutfak', 'tuvalet',
                        'bahçe', 'sokak', 'kanal', 'drenaj', 'yağmur'
                    ],
                    'problem_keywords': [
                        'kesik', 'akmıyor', 'gelmıyor', 'düşük', 'yüksek',
                        'bulanık', 'kokulu', 'sıcak', 'soğuk', 'donmuş'
                    ]
                },


                'cevre_temizlik': {
                    'primary_keywords': [
                        'çöp', 'atık', 'temizlik', 'hijyen', 'kirli', 'pis',
                        'koku', 'böcek', 'fare', 'haşere', 'bakterı', 'kaldırım', 'su birikintisi'
                    ],
                    'secondary_keywords': [
                        'konteyner', 'çöp kutusu', 'toplama', 'süpürme', 'yıkama',
                        'dezenfekte', 'ilaçlama', 'fumigasyon', 'temizleme'
                    ],
                    'context_keywords': [
                        'sokak', 'cadde', 'park', 'bahçe', 'meydan', 'pazar',
                        'okul', 'hastane', 'market', 'ev', 'apartman'
                    ],
                    'problem_keywords': [
                        'dolu', 'taşan', 'saçılmış', 'kokulu', 'yanık',
                        'çürük', 'leş', 'pislik', 'berbat', 'iğrenç'
                    ]
                },


                'gurultu_rahatsizlik': {
                    'primary_keywords': [
                        'gürültü', 'ses', 'bağırma', 'çığlık', 'patırtı',
                        'müzik', 'hoparlör', 'megafon', 'davul', 'zurna', 'güvensiz ortam', 'tedirgin'
                    ],
                    'secondary_keywords': [
                        'rahatsız', 'uyku', 'dinlenme', 'huzur', 'sessizlik',
                        'konser', 'düğün', 'eğlence', 'parti', 'kutlama'
                    ],
                    'context_keywords': [
                        'gece', 'sabah', 'öğle', 'akşam', 'hafta sonu',
                        'tatil', 'bayram', 'festival', 'şenlik', 'organizasyon'
                    ],
                    'problem_keywords': [
                        'yüksek', 'aşırı', 'dayanılmaz', 'sürekli', 'devamlı',
                        'saatlerce', 'geç', 'erken', 'uygunsuz', 'yasak','güvensiz ortam', 'tedirgin'
                    ]
                },


                'aydinlatma': {
                    'primary_keywords': [
                        'ışık', 'lamba', 'aydınlatma', 'karanlık', 'loş',
                        'ampul', 'projektör', 'reflektör', 'led', 'neon'
                    ],
                    'secondary_keywords': [
                        'sokak lambası', 'park lambası', 'güvenlik', 'aydınlık',
                        'parlaklık', 'enerji', 'elektrik', 'kablo', 'direk'
                    ],
                    'context_keywords': [
                        'sokak', 'cadde', 'park', 'meydan', 'köprü', 'alt geçit',
                        'otopark', 'bahçe', 'yol', 'kaldırım', 'merdiven'
                    ],
                    'problem_keywords': [
                        'yanmıyor', 'söndü', 'bozuk', 'kırık', 'eksik',
                        'yetersiz', 'zayıf', 'titrek', 'kesiyor', 'gidiyor'
                    ]
                },


                'park_yesil_alan': {
                    'primary_keywords': [
                        'park', 'bahçe', 'yeşil', 'ağaç', 'çiçek', 'çimen',
                        'çim', 'peyzaj', 'bitki', 'fidanlık', 'orman'
                    ],
                    'secondary_keywords': [
                        'oyun alanı', 'çocuk parkı', 'bank', 'oturma', 'gölge',
                        'sulama', 'budama', 'bakım', 'düzenleme', 'çevre'
                    ],
                    'context_keywords': [
                        'dinlenme', 'spor', 'yürüyüş', 'koşu', 'bisiklet',
                        'çocuk', 'aile', 'rekreasyon', 'piknik', 'doğa'
                    ],
                    'problem_keywords': [
                        'kurumuş', 'ölmüş', 'kesilmiş', 'harap', 'bakımsız',
                        'kirli', 'pislik', 'zarar', 'tahrip', 'yıkım'
                    ]
                },


                'guvenlik': {
                    'primary_keywords': [
                        'güvenlik', 'suç', 'hırsızlık', 'saldırı', 'tehdit',
                        'korku', 'emniyet', 'polis', 'bekçi', 'kamera'
                    ],
                    'secondary_keywords': [
                        'uyuşturucu', 'sarhoş', 'kavga', 'bıçak', 'silah',
                        'yaralama', 'darp', 'gasp', 'kapkaç', 'dolandırıcılık'
                    ],
                    'context_keywords': [
                        'sokak', 'park', 'otopark', 'alt geçit', 'köprü',
                        'meydan', 'pazar', 'okul', 'hastane', 'terminal'
                    ],
                    'problem_keywords': [
                        'tehlikeli', 'riskli', 'güvensiz', 'korkutucu',
                        'şüpheli', 'suçlu', 'zararlı', 'yasaklı', 'illegal',
                    ]
                },


                'yapim_insaat': {
                    'primary_keywords': [
                        'inşaat', 'yapım', 'inşa', 'bina', 'yapı', 'köprü',
                        'yol', 'beton', 'çimento', 'demir', 'tuğla', 'taş'
                    ],
                    'secondary_keywords': [
                        'proje', 'planlama', 'tasarım', 'mimar', 'mühendis',
                        'müteahhit', 'işçi', 'makine', 'vinç', 'kamyon'
                    ],
                    'context_keywords': [
                        'gecikmeli', 'yarıda', 'durmuş', 'tamamlanmamış',
                        'eksik', 'hatalı', 'kusurlu', 'standart', 'kalite'
                    ],
                    'problem_keywords': [
                        'duran', 'terk edilmiş', 'yarım', 'hatalı', 'çöken',
                        'çatlayan', 'zarar', 'tehlike', 'risk', 'sorunlu'
                    ]
                },


                'saglik_hijyen': {
                    'primary_keywords': [
                        'sağlık', 'hijyen', 'temizlik', 'dezenfekte', 'steril',
                        'mikrop', 'bakteri', 'virüs', 'hastalık', 'bulaşıcı'
                    ],
                    'secondary_keywords': [
                        'hastane', 'sağlık ocağı', 'eczane', 'ambulans',
                        'doktor', 'hemşire', 'tıbbi', 'tedavi', 'ilaç'
                    ],
                    'context_keywords': [
                        'acil', 'hasta', 'yaralı', 'rahatsız', 'ağrı',
                        'enfeksiyon', 'zehirlenme', 'alerji', 'grip', 'ateş'
                    ],
                    'problem_keywords': [
                        'kirli', 'pis', 'kokulu', 'tehlikeli', 'zararlı',
                        'bulaşık', 'enfekte', 'toksik', 'zehirli', 'riskli'
                    ]
                },


                'egitim': {
                    'primary_keywords': [
                        'okul', 'eğitim', 'öğretim', 'öğrenci', 'öğretmen',
                        'müdür', 'dersane', 'kurs', 'anaokulu', 'kreş'
                    ],
                    'secondary_keywords': [
                        'sınıf', 'ders', 'kitap', 'defter', 'kalem', 'tahta',
                        'projeksiyon', 'laboratuvar'
                    ]
            },

                'elektrik-ariza': {
                    'primary_keywords': [
                        'elektrik kesintisi', 'kesinti', 'elektrikler yok', 'karanlıkta oturuyoruz', 'elektirkli cihaz',
                        'elektrik', 'televizyon', 'buzdolabı', 'makinalar çalışmıyor', 'kreş', 'şarj', 'telefon şarjı',
                    ],
                    'secondary_keywords': [
                         'çocukar ödevini yapamıyor', 'telefon şarjı', 'ışık ihtiyacı', 'cihazlar çalışmıyor', 'elektrikli',

                    ]
                },
                'internet-sorunu': {
                    'primary_keywords': [
                        'internet', 'bağlantı', 'hız', 'mbps', 'internet yavaş',
                        'internet altyapısı'
                    ],
                    'secondary_keywords': [
                         'whatsapp', 'instagram', 'mobil uygulama', 'twitter', 'x uygulaması'
                    ]
                },
                'telefon-sorunu': {
                    'primary_keywords': [
                         'şebeke', 'telefon çekmiyor', 'ulaşamıyorum', 'sesini alamıyorum','çekmiyor'
                        , 'arama', 'arayamıyorum'
                    ],
                    'secondary_keywords': [
                        'arama yapma', 'baz istasyonu'
                    ]
                },
                'arıza': {
                    'primary_keywords': [
                        'asansör arızalı', 'yürüyen merdiven çalışmıyor', 'bozuk', 'aktif değil', 'arıza', 'bozuk'
                    ],
                    'secondary_keywords': [
                        'arama yapma', 'baz istasyonu', 'aramam ulaşmıyor'
                    ]
                },
                'faturalandırma_sorunu': {
                    'primary_keywords': [
                        'olağandışı artış', 'haksız ödeme', 'vergi kaçırma', 'yüksek mebla', 'servis bedeli', 'kullanımsal olmayan'
                    ],
                    'secondary_keywords': [
                        'yeniden ölçüm', 'yeniden faturalandırma', 'tekrar inceleme', 'soruşturma', 'kaçak kullanım'
                    ]
                },
                'okul_sorunu': {
                    'primary_keywords': [
                        'kaloriferler yanmıyor', 'montla ders işliyor', 'sınıflar soğuk', 'sınıflar kirli', 'sınıflar kalabalık',
                        'kış ayları', 'şiddet', 'psikolojik şiddet'
                    ],
                    'secondary_keywords': [
                        'tramvatik davranışlar', 'zorbalığa uğrama', 'öğretmen zorbalığı', 'akran zorbalığı', 'uyum sağlayamama'
                    ]
                },
                'kargo_sorunu': {
                    'primary_keywords': [
                        'kargo', 'elime ulaşmadı', 'kargo takip sistemi', 'yolda', 'ptt','yurtiçi kargo', 'mng', 'ups','sürat kargo'
                        , 'kurye'
                    ],
                    'secondary_keywords': [
                        'hala yolda', 'kargo şubesi', 'kargo şubesine ulaşamıyorum', 'kurye kargoma zarar', 'kargo hasarı', 'kargom hasarlı'
                    ]
                },
                'pazaryeri_sorunu': {
                    'primary_keywords': [
                        'hafta sonları kurulan', 'pazar yeri', 'sebze meyve pazarı', 'pazaryeri düzenlemesi', 'pazaryeri taşıması',
                        'kullanımsal olmayan'
                    ]
                }
        },
    }

    def extract_names_comprehensive(self, text: str) -> Dict:
        """kapsamlı isim çıkarma """

        name_candidates = []
        extraction_methods = {}


        lines = text.split('\n')
        sentences = re.split(r'[.!?]+', text)


        signature_names = []
        for pattern in self.core_patterns['person_identity']['signature_patterns']:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                if matches and isinstance(matches[0], tuple):
                    # Grup yakalama durumu
                    for match in matches:
                        for group in match:
                            if group and len(group.strip()) > 2:
                                signature_names.append(group.strip())
                else:
                    signature_names.extend([m.strip() for m in matches if len(m.strip()) > 2])

        name_candidates.extend(signature_names)
        extraction_methods['signature_patterns'] = signature_names


        positional_names = []


        for line in lines[-3:]:
            line = line.strip()
            if line and not any(word in line.lower() for word in ['telefon', 'tel:', 'gsm:', 'e-mail', '@', 'http']):
                # İsim benzeri pattern ara
                potential_names = re.findall(r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\b', line)
                positional_names.extend(potential_names)


        for line in lines[:3]:
            line = line.strip()
            if 'sayın' in line.lower() or 'muhterem' in line.lower():
                potential_names = re.findall(r'(?:sayın|muhterem)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşüA-ZÇĞİÖŞÜ\s]+?)(?:[,\n]|$)',
                                             line, re.IGNORECASE)
                positional_names.extend(potential_names)

        name_candidates.extend(positional_names)
        extraction_methods['positional_analysis'] = positional_names


        context_names = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(clue in sentence.lower() for clue in self.core_patterns['person_identity']['context_clues']):

                potential_names = re.findall(r'\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\b', sentence)
                context_names.extend(potential_names)

        name_candidates.extend(context_names)
        extraction_methods['context_based'] = context_names


        address_names = []

        # "isim / lokasyon"  şeklinde  formatları yakalama
        slash_patterns = [
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s*/\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s*-\s*([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)',
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+/[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)'
        ]

        for pattern in slash_patterns:
            matches = re.findall(pattern, text)
            for match in matches:

                if len(match[0]) > 3:
                    address_names.append(match[0])

        name_candidates.extend(address_names)
        extraction_methods['address_combined'] = address_names


        contact_names = []


        tc_patterns = [
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:tc|TC|T\.C\.):?\s*\d{11}',
            r'(?:tc|TC|T\.C\.):?\s*\d{11}\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)'
        ]

        for pattern in tc_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            contact_names.extend(matches)


        phone_patterns = [
            r'([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+(?:tel|telefon|gsm|cep):?\s*[\d\s\-\(\)]+',
            r'(?:tel|telefon|gsm|cep):?\s*[\d\s\-\(\)]+\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ][a-zçğıöşü]+)'
        ]

        for pattern in phone_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            contact_names.extend(matches)

        name_candidates.extend(contact_names)
        extraction_methods['contact_combined'] = contact_names

        # skorlama
        cleaned_candidates = []
        for name in name_candidates:
            name = name.strip()
            if len(name) > 3 and len(name) < 50:

                turkish_chars = sum(1 for char in name if char in 'çğıöşüÇĞIİÖŞÜ')
                score = 1.0 + (turkish_chars * 0.1)
                cleaned_candidates.append((name, score))


        if cleaned_candidates:
            from collections import Counter
            name_scores = Counter([name for name, score in cleaned_candidates])

            # frekans skoru ile kalite skorlarını bileşitr
            final_scores = {}
            for name, score in cleaned_candidates:
                frequency = name_scores[name]
                final_scores[name] = frequency * score

            best_name = max(final_scores, key=final_scores.get)
            confidence = min(final_scores[best_name] / 10.0, 1.0)

            return {
                'extracted_name': best_name,
                'confidence': confidence,
                'all_candidates': list(set([name for name, _ in cleaned_candidates])),
                'extraction_methods': extraction_methods,
                'method_scores': final_scores
            }

        return {
            'extracted_name': None,
            'confidence': 0.0,
            'all_candidates': [],
            'extraction_methods': extraction_methods,
            'method_scores': {}
        }

    def _initialize_contextual_weights(self) -> Dict:
        """bağlamsal ağırlık matrisi - kelimelerin konumsal takibi için"""
        return {
            'position_multipliers': {
                'document_start': 1.5,  # İlk %20'lik kısım
                'document_middle': 1.0,  # Orta %60'lık kısım
                'document_end': 1.3,  # Son %20'lik kısım
                'sentence_start': 1.2,  # Cümle başları
                'after_punctuation': 1.1  # Noktalama sonrası
            },

            'semantic_proximity': {
                'same_sentence': 2.0,
                'adjacent_sentence': 1.5,  # bitişik cümleler
                'same_paragraph': 1.2,
                'document_wide': 1.0  # genel doküman
            },

            'urgency_amplifiers': {
                'exclamation_nearby': 1.4,  # yakında ünlem
                'caps_lock_context': 1.6,  # büyük harf bağlamı
                'repetition_pattern': 1.3,  # tekrarlanan ifadeler
                'temporal_pressure': 1.8  # time pressure kelimeleri
            }
        }

