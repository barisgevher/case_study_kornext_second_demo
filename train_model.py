import pandas as pd
import ast  # String'i güvenli bir şekilde dictionary'e çevirmek için
from typing import List

# train_classification_model fonksiyonunuzun burada olduğunu varsayalım.
# Eğer başka bir dosyadaysa, onu import etmeniz gerekir.
# Örnek: from your_file import train_classification_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_classification_model(texts: List[str], labels: List[str], model_type: str = "svm"):
    """Sınıflandırma modeli eğit"""
    # ... (fonksiyonunuzun içeriği buraya gelecek, hiç değiştirmeyin)
    # TF-IDF vektörleştirme
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42, stratify=labels
    ) # stratify eklemek dengeli dağılım için iyidir

    # Model seçimi
    if model_type == "nb":
        model = MultinomialNB()
    elif model_type == "svm":
        model = SVC(kernel='linear', probability=True)
    elif model_type == "rf":
        model = RandomForestClassifier(n_estimators=100)
    else:
        raise ValueError("Geçersiz model tipi")

    # Eğitim
    model.fit(X_train, y_train)

    # Değerlendirme
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"Eğitim Doğruluğu: {train_score:.2%}")
    print(f"Test Doğruluğu: {test_score:.2%}")

    # Modeli kaydet
    joblib.dump(model, f"model_{model_type}.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

    return model, vectorizer


def extract_label_from_analysis(analysis_str: str, label_key: str = 'action'):
    """
    Karmaşık analiz string'inden istenen etiketi (action, priority vb.) güvenli bir şekilde çıkarır.
    """
    try:
        # String'i Python dictionary nesnesine dönüştür
        data = ast.literal_eval(analysis_str)
        # İç içe geçmiş yapıdan etiketi çıkar
        label_list = data['analysis_']['person_']['moment']['citizen_g']['overall_']['citizen_u']
        # Eğer liste boş değilse, ilk elemandaki etiketi al
        if label_list:
            return label_list[0].get(label_key, None)
    except (ValueError, SyntaxError, KeyError, IndexError):
        # Hatalı format, eksik anahtar veya boş liste durumunda None döndür
        return None
    return None


# --- ANA SÜREÇ ---
if __name__ == "__main__":
    # 1. AYARLAR: Dosya ve sütun adlarını buradan değiştirin
    EXCEL_FILE_PATH = "egitim_veriseti.xlsx"  # Excel dosyanızın adı
    TEXT_COLUMN = "ham_metin"                # Metinleri içeren sütun
    ANALYSIS_COLUMN = "analiz_sonucu"        # Analiz sonucunu içeren sütun
    TARGET_LABEL = "action"                  # Tahmin etmek istediğimiz etiket ('action', 'priority', 'timeline' olabilir)

    # 2. VERİYİ YÜKLEME
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
    except FileNotFoundError:
        print(f"HATA: '{EXCEL_FILE_PATH}' dosyası bulunamadı!")
        exit()

    print(f"Excel'den {len(df)} satır veri okundu.")

    # 3. ETİKETLERİ AYIKLAMA
    # 'analiz_sonucu' sütunundaki her satır için extract_label_from_analysis fonksiyonunu uygula
    df[TARGET_LABEL] = df[ANALYSIS_COLUMN].apply(lambda x: extract_label_from_analysis(x, TARGET_LABEL))

    # 4. VERİYİ TEMİZLEME
    # Etiketi olmayan (None) veya metni olmayan satırları kaldır
    df_clean = df.dropna(subset=[TEXT_COLUMN, TARGET_LABEL]).copy()
    print(f"Temizleme sonrası eğitim için {len(df_clean)} uygun satır kaldı.")

    # 5. EĞİTİM VERİLERİNİ HAZIRLAMA
    # Fonksiyonun istediği format olan listelere dönüştür
    texts_to_train = df_clean[TEXT_COLUMN].tolist()
    labels_to_train = df_clean[TARGET_LABEL].tolist()

    # 6. MODELİ EĞİTME
    if texts_to_train and labels_to_train:
        print(f"\n'{TARGET_LABEL}' etiketini tahmin etmek için SVM modeli eğitiliyor...")
        train_classification_model(
            texts=texts_to_train,
            labels=labels_to_train,
            model_type="svm"  # "nb" veya "rf" olarak değiştirebilirsiniz
        )
    else:
        print("Modeli eğitmek için yeterli veri bulunamadı.")