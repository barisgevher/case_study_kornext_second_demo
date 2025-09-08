import os
import re
from src.petition_analyzer import PetitionAnalyzer
import pandas as pd

def process_data(file_path):
    """
    Belirtilen formattaki metin dosyasını okur ve her bir dilekçeyi
    yapısal bir şekilde (dosya adı, tarih, metin olarak) ayırır. ve kayıt eder

    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            full_text = f.read()
    except FileNotFoundError:
        print(f"Hata: '{file_path}' dosyası bulunamadı.")
        return []

    pattern = re.compile(
        r"Dosya: (.+?)\n"
        r"Tarih: (.+?)\n"
        r"={50}\n"
        r"(.*?)"
        r"(?=\n={50}|$)", re.DOTALL
    )
    matches = pattern.findall(full_text)

    documents = []
    for match in matches:
        if match[2].strip():
            documents.append({
                "dosya": match[0].strip(),
                "tarih": match[1].strip(),
                "metin": match[2].strip()
            })
    return documents


def create_training_dataset(folder_path: str, output_filename: str):
    """
    Ham metin dosyasını okur, her bir metni analiz eder ve makine öğrenmesi
    modellerini eğitmek için yapısal bir veri seti (DataFrame) oluşturur.
    """
    train_data_path = os.path.join(folder_path, "train_data.txt")

    # verileri yapısal olarak oku ve ayır
    documents = process_data(train_data_path)

    if not documents:
        print("İşlenecek dilekçe bulunamadı.")
        return None

    print(f"Toplam {len(documents)} dilekçe bulundu ve yapısal olarak ayrıştırıldı.")

    # PetitionAnalyzer'dan bir nesne oluştur
    analyzer = PetitionAnalyzer()

    labeled_data = []

    # her dilekçeyi analiz et ve sonuçları orijinal veriyle birleştir
    for i, doc in enumerate(documents, 1):
        print(f"Analiz ediliyor: {i}/{len(documents)} ({doc['dosya']})")

        analysis_result = analyzer.analyze_petition_creative(doc['metin'])

        # orijinal metin ve analiz sonucunu birleştirerek tam bir kayıt oluştur
        final_record = {
            'dosya_adi': doc['dosya'],
            'tarih': doc['tarih'],
            'ham_metin': doc['metin'],   # makine öğrenmesi için girdi - feature
            **analysis_result           # makine öğrenmesi için çıktılar - labels
        }
        labeled_data.append(final_record)

    # etiketli veri setini dataframe dönüştür
    df = pd.DataFrame(labeled_data)
    df.to_excel(output_filename, index=False)
    print(f"\nAnaliz tamamlandı! Eğitim veri seti '{output_filename}' dosyasına kaydedildi.")

    return df



if __name__ == "__main__":
    TRAINING_FILES_FOLDER = "data"
    OUTPUT_EXCEL_FILE = "data/train_dataset.xlsx"

    training_df = create_training_dataset(
        folder_path=TRAINING_FILES_FOLDER,
        output_filename=OUTPUT_EXCEL_FILE
    )

    # head
    if training_df is not None:
        print("\n--- veri seti ön izlemesi ---")
        print(training_df.head())