from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import joblib
import pandas as pd
import ast


def train_classification_model(texts: List[str], labels: List[str], model_type: str = "svm"):
    """Sınıflandırma modeli eğit"""

    # TF-IDF vektörleştirme
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(texts)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

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
       String formatındaki bir "liste içindeki sözlük" yapısından istenen anahtarın değerini çıkarır.
    Örnek: analysis_str = "[{'action': 'immediate_response', 'priority': 'P1'}]"
           label_key = 'priority'
           Dönen Değer => 'P1'.
    """
    try:
        data_list = ast.literal_eval(str(analysis_str))
        if isinstance(data_list, list) and data_list:
            data_dict = data_list[0]

            if isinstance(data_dict, dict):
                return data_dict.get(label_key, None)
    except(ValueError, SyntaxError, IndexError):
        return None
    return None





# --- ANA SÜREÇ ---
if __name__ == "__main__":
    # 1. AYARLAR: Dosya ve sütun adlarını buradan değiştirin
    EXCEL_FILE_PATH = "egitim_veriseti.xlsx"  # Excel dosyanızın adı
    TEXT_COLUMN = "ham_metin"                # Metinleri içeren sütun
    ANALYSIS_COLUMN = "actionable_recommendations"        # Analiz sonucunu içeren sütun
    TARGET_LABEL = "priority"                  # Tahmin etmek istediğimiz etiket ('action', 'priority', 'timeline' olabilir)

    # 2. VERİYİ YÜKLEME
    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
    except FileNotFoundError:
        print(f"HATA: '{EXCEL_FILE_PATH}' dosyası bulunamadı!")
        exit()

    print("Excel'den okunan sütun adları:", df.columns)
    print(f"Excel'den {len(df)} satır veri okundu.")

    print("\n'actionable_recommendations' Sütununun İçeriğinin İlk 5 Satırı:")
    print(df['actionable_recommendations'].head())

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