from datetime import datetime
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import json
import os

from PetitionAnalyzer import PetitionAnalyzer


# 🔍 PDF'den metni oku
def pdf_to_text(path):
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text


# 📥 JSON'a kaydet
def save_to_json(result, file_name="petition_analyze_results.json"):
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []

    data.append(result)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 📌 Ana işlem
def process_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not path:
        return

    text = pdf_to_text(path)
    analyzer = PetitionAnalyzer()
    result = analyzer.analyze_petition_creative(text)
    result["dosya_adi"] = os.path.basename(path)

    # PDF'den çıkarılan metni kaydet
    base_filename = os.path.splitext(os.path.basename(path))[0]
    txt_filename = f"{base_filename}.txt"

    # text_files klasörünü oluştur
    txt_folder = "text_files"
    os.makedirs(txt_folder, exist_ok=True)

    # train_data.txt dosyasının yolu
    train_data_path = os.path.join(txt_folder, "train_data.txt")

    # Eğitim verisine ekle (append modunda)
    with open(train_data_path, "a", encoding="utf-8") as f_train:
        f_train.write(f"\n\n{'=' * 50}\n")
        f_train.write(f"Dosya: {base_filename}\n")
        f_train.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f_train.write(f"{'=' * 50}\n")
        f_train.write(text)
        f_train.write("\n")


    # JSON veritabanına kaydet
    save_to_json(result)

    status_label.config(text=f"✅ PDF işlendi: {base_filename} -> train_data.txt'ye eklendi")

# 🖥️ Basit Arayüz
root = tk.Tk()
root.title("PDF İşleyici")
root.geometry("400x200")

select_button = tk.Button(root, text="PDF Seç ve İşle", command=process_pdf)
select_button.pack(pady=20)

status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()
