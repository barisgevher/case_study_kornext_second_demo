import os
import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from datetime import datetime

# Yeni yapıya göre doğru importlar
# Projenizin 'src' klasörünü Python'un tanıması için yola ekliyoruz
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.petition_analyzer import PetitionAnalyzer
from src.utils import pdf_to_text  # PDF okuyucuyu utils'e taşıdık

# --- Ayarlar ve Sabitler ---
DATA_FOLDER = "data"
TRAIN_DATA_FILE = os.path.join(DATA_FOLDER, "train_data.txt")
JSON_RESULTS_FILE = os.path.join(DATA_FOLDER, "petition_analyze_results.json")


def setup_project_structure():
    """Gerekli klasörlerin var olduğundan emin olur."""
    os.makedirs(DATA_FOLDER, exist_ok=True)


def save_to_json(result: dict):
    """Analiz sonucunu JSON dosyasına kaydeder/günceller."""
    if os.path.exists(JSON_RESULTS_FILE):
        with open(JSON_RESULTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    data.append(result)
    with open(JSON_RESULTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_to_training_data(text: str, base_filename: str):
    """Metni, başlık bilgileriyle birlikte train_data.txt'ye ekler."""
    with open(TRAIN_DATA_FILE, "a", encoding="utf-8") as f_train:
        f_train.write(f"\n\n{'=' * 50}\n")
        f_train.write(f"Dosya: {base_filename}\n")
        f_train.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f_train.write(f"{'=' * 50}\n")
        f_train.write(text.strip())
        f_train.write("\n")


def process_text_and_update_ui(text: str, source_name: str):
    """Verilen metni analiz eder, kaydeder ve arayüzü günceller."""
    if not text.strip():
        messagebox.showwarning("Uyarı", "İşlenecek metin bulunamadı.")
        return

    # 1. Analiz
    analyzer = PetitionAnalyzer()
    result = analyzer.analyze_petition_creative(text)
    result["kaynak_dosya"] = source_name

    # 2. Sonuçları JSON olarak kaydet
    save_to_json(result)

    # 3. Eğitim verisine ekle
    save_to_training_data(text, source_name)

    # 4. Arayüzü güncelle
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    pretty_result = json.dumps(result, indent=4, ensure_ascii=False)
    result_text.insert(tk.END, pretty_result)
    result_text.config(state=tk.DISABLED)

    status_label.config(
        text=f"✅ Başarılı: '{source_name}' işlendi ve kaydedildi.",
        fg="green"
    )


def handle_pdf_selection():
    """PDF seçme ve işleme mantığı."""
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
    """Metin kutusundan veri işleme mantığı."""
    text = input_text.get("1.0", tk.END)
    # Metin girişi için benzersiz bir isim oluştur
    source_name = f"metin_girdisi_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    process_text_and_update_ui(text, source_name)


# --- Arayüz Kurulumu ---
if __name__ == "__main__":
    setup_project_structure()

    root = tk.Tk()
    root.title("Dilekçe Analiz Aracı")
    root.geometry("800x600")

    main_frame = tk.Frame(root, padx=10, pady=10)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Sol Taraf: Girdi Alanları
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

    # Sağ Taraf: Sonuç Ekranı
    right_frame = tk.Frame(main_frame, width=380)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

    tk.Label(right_frame, text="Analiz Sonucu:", font=("Helvetica", 10, "bold")).pack(anchor="w")
    result_text = scrolledtext.ScrolledText(right_frame, height=20, wrap=tk.WORD, state=tk.DISABLED)
    result_text.pack(fill=tk.BOTH, expand=True, pady=5)

    # Alt Taraf: Durum Etiketi
    status_label = tk.Label(root, text="İşlem için bir dosya seçin veya metin girin.", bd=1, relief=tk.SUNKEN, anchor="w")
    status_label.pack(side=tk.BOTTOM, fill=tk.X)

    root.mainloop()