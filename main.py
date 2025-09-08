import os
import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from datetime import datetime
import pandas as pd
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.petition_analyzer import PetitionAnalyzer
from src.utils import pdf_to_text, format_result_summary

# ayarlar ve sabit değerler
DATA_FOLDER = "data"
TRAIN_DATA_FILE = os.path.join(DATA_FOLDER, "train_data.txt")
JSON_RESULTS_FILE = os.path.join(DATA_FOLDER, "petition_analyze_results.json")


def setup_project_structure():
    """klasör kontolü."""
    os.makedirs(DATA_FOLDER, exist_ok=True)


def save_to_json(result: dict):
    """sonucu json olarak kayıt eder."""
    if os.path.exists(JSON_RESULTS_FILE):
        with open(JSON_RESULTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    data.append(result)
    with open(JSON_RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_to_training_data(text: str, base_filename: str):
    """çıkarılan metni txt dosyasına kayıt eder"""
    with open(TRAIN_DATA_FILE, "a", encoding="utf-8") as f_train:
        f_train.write(f"\n\n{'=' * 50}\n")
        f_train.write(f"Dosya: {base_filename}\n")
        f_train.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f_train.write(f"{'=' * 50}\n")
        f_train.write(text.strip())
        f_train.write("\n")


def process_text_and_update_ui(text: str, source_name: str):
    """analiz ve kayıt işlemleri"""
    if not text.strip():
        messagebox.showwarning("Uyarı", "İşlenecek metin bulunamadı.")
        return

    # analiz
    analyzer = PetitionAnalyzer()
    result = analyzer.analyze_petition_creative(text)
    result["kaynak_dosya"] = source_name

    # sonuçları json olarak kayıt etme
    save_to_json(result)

    #eğitim verisine ekle
    save_to_training_data(text, source_name)

    append_to_excel_dataset(result, text, source_name)

    # arayüzü güncelle
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    summary_output = format_result_summary(result)
    # print(result)
    result_text.insert(tk.END, summary_output)
    result_text.config(state=tk.DISABLED)

    status_label.config(
        text=f"işlem başarılı: '{source_name}' işlendi ve kaydedildi.",
        fg="green"
    )


def handle_pdf_selection():
    """Pdf seçme ve işleme mantığı."""
    path = filedialog.askopenfilename(filetypes=[("PDF Dosyaları", "*.pdf")])
    if not path:
        return
    try:
        text = pdf_to_text(path)
        base_filename = os.path.splitext(os.path.basename(path))[0]
        process_text_and_update_ui(text, base_filename)
    except Exception as e:
        messagebox.showerror("Hata", f"PDF okunurken bir hata oluştu:\n{e}")


def handle_text_input():
    """metin kutusundan veri işleme mantığı."""
    text = input_text.get("1.0", tk.END)
    # metin girdisi için benzersiz bir isim oluştur
    source_name = f"metin_girdisi_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    process_text_and_update_ui(text, source_name)

def append_to_excel_dataset(result: dict, text: str, source_name: str):
    """
    Yeni analiz sonucunu 'training_dataset.xlsx' dosyasına yeni bir satır olarak ekler.
    Dosya yoksa oluşturur.
    """
    excel_path = os.path.join(DATA_FOLDER, "training_dataset.xlsx")

    # yeni kayıt verisini hazırla
    new_record = {
        'dosya_adi': source_name,
        'tarih': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ham_metin': text.strip(),
        **result  # analiz sonucundaki tüm anahtarları ayrı sütunlar olarak aç
    }
    new_row_df = pd.DataFrame([new_record])

    # mevcut excel dosyasını oku ve yeni satırı ekle
    try:
        if os.path.exists(excel_path):
            # Dosya varsa, oku ve sonuna ekle
            existing_df = pd.read_excel(excel_path)
            updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)
        else:
            # dosya yoksa, bu yeni satır ilk veri olarak yazılacak
            updated_df = new_row_df

        # güncellenmiş dataframei tekrar excele yaz
        updated_df.to_excel(excel_path, index=False)

    except Exception as e:
        # dosya başka bir programda açıksa veya başka bir hata olursa hata göster
        messagebox.showerror("Excel Yazma Hatası", f"Eğitim veriseti güncellenemedi:\n{e}")



if __name__ == "__main__":
    setup_project_structure()

    root = tk.Tk()
    root.title("Dilekçe Analiz Aracı")
    root.geometry("800x600")

    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # sol taraf: girdi alanları
    left_frame = tk.Frame(main_frame, width=380)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    tk.Label(left_frame, text="1. PDF Dosyası Seçin:", font=("Helvetica", 10, "bold")).pack(anchor="w")
    pdf_button = tk.Button(left_frame, text="PDF Seç ve İşle", command=handle_pdf_selection)
    pdf_button.pack(fill=tk.X, pady=(5, 20))

    tk.Label(left_frame, text="2. Veya Metni Buraya Yapıştırın:", font=("Helvetica", 10, "bold")).pack(anchor="w")
    input_text = scrolledtext.ScrolledText(left_frame, height=15, wrap=tk.WORD)
    input_text.pack(fill=tk.BOTH, expand=True, pady=5)

    text_button = tk.Button(left_frame, text="Metni İşle", command=handle_text_input)
    text_button.pack(fill=tk.X, pady=(5, 0))

    # sonuç Ekranı
    right_frame = tk.Frame(main_frame, width=380)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    tk.Label(right_frame, text="Analiz Sonucu:", font=("Helvetica", 10, "bold")).pack(anchor="w")
    result_text = scrolledtext.ScrolledText(right_frame, height=20, wrap=tk.WORD, state=tk.DISABLED)
    result_text.pack(fill=tk.BOTH, expand=True, pady=5)

    # alt taraf durum etiketi
    status_label = tk.Label(root, text="İşlem için bir dosya seçin veya metin girin.", bd=1, relief=tk.SUNKEN, anchor="w")
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()