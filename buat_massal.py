import os
import csv

if not os.path.exists("template.html"):
    print("Error: Berkas template.html tidak ditemukan!")
    exit()

if not os.path.exists("database.csv"):
    print("Error: Berkas database.csv tidak ditemukan!")
    exit()

with open("template.html", "r", encoding="utf-8") as f:
    html_template = f.read()

print("Membaca database Excel (CSV)...")

# Mencari tahu apakah komputer menggunakan pemisah koma (,) atau titik koma (;)
with open("database.csv", "r", encoding="utf-8-sig") as f:
    sample = f.read(2048)
    if ';' in sample:
        pemisah = ';'
    else:
        pemisah = ','

with open("database.csv", "r", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=pemisah)
    
    index = 1
    for row in reader:
        # Membersihkan nama kolom dari spasi atau karakter aneh jika ada
        cleaned_row = {k.strip() if k else '': v for k, v in row.items()}
        
        # Mencari kolom berdasarkan kata kunci kemiripan teks
        link_1 = next((v for k, v in cleaned_row.items() if 'tombol1' in k.lower()), '').strip()
        link_2 = next((v for k, v in cleaned_row.items() if 'tombol2' in k.lower()), '').strip()
        link_3 = next((v for k, v in cleaned_row.items() if 'tombol3' in k.lower()), '').strip()
        
        if not link_1 or not link_2 or not link_3:
            continue
            
        nama_folder = f"iklan{index}"
        os.makedirs(nama_folder, exist_ok=True)
        
        html_baru = html_template.replace("PLACEHOLDER_TOMBOL_1", link_1)
        html_baru = html_baru.replace("PLACEHOLDER_TOMBOL_2", link_2)
        html_baru = html_baru.replace("PLACEHOLDER_TOMBOL_3", link_3)
        
        path_file = os.path.join(nama_folder, "index.html")
        with open(path_file, "w", encoding="utf-8") as file_out:
            file_out.write(html_baru)
            
        index += 1

print(f"Sukses Besar! Berhasil membuat {index - 1} folder iklan otomatis dari Excel.")