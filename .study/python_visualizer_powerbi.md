# Studi Mandiri: Menggunakan Python Visualizer di Power BI
Dokumen ini menjelaskan cara menggunakan fitur **Python Visual** di Power BI Desktop untuk menggambar grafik dan menampilkan data tanpa perlu pusing mencari menu format Power BI yang sering berubah atau tersembunyi.

---

## 1. Apa itu Python Visual di Power BI?

Power BI memiliki komponen visual bawaan bernama **Python visual** (ikon berlogo `Py`). Komponen ini memungkinkan Anda menulis skrip Python (menggunakan pustaka seperti `matplotlib` atau `seaborn`) untuk menggambar visualisasi secara langsung di kanvas dashboard Anda.

Setiap data dari kolom yang Anda seret ke dalam komponen ini akan otomatis dibaca oleh Python sebagai sebuah objek **Pandas DataFrame** bernama `dataset`.

---

## 2. Cara Menggunakan Python Visual (Langkah Demi Langkah)

1. Buka Power BI Desktop.
2. Di panel **Visualizations** sebelah kanan, cari dan klik ikon **Python visual** (ikon berlogo `Py`).
3. Jika muncul pop-up peringatan *"Enable script visuals"*, klik **Enable**.
4. Seret kolom data atau Measure yang ingin Anda visualisasikan ke dalam area **Values** di bawah panel visualisasi.
   * Contoh: Seret kolom `production_date` dan Measure `Total Output`.
5. Di bagian bawah layar, panel **Python script editor** akan otomatis terbuka.
6. Tulis kode Python Anda di bawah teks komentar bawaan, lalu klik tombol **Run** (ikon segitiga/play di kanan atas editor script).

---

## 3. Contoh Script Python untuk Menggambar Visualisasi

Berikut adalah beberapa contoh skrip yang bisa Anda salin ke editor skrip Power BI untuk menghasilkan visualisasi yang bersih dan tanpa penyingkatan angka otomatis (tanpa huruf K/M):

### Contoh A: Bar Chart Output per Lini (Menggunakan Seaborn)
Menampilkan grafik batang total output untuk setiap lini dengan label angka penuh di atas batangnya.

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Ambil data dari Power BI (otomatis tersimpan di variabel 'dataset')
# dataset berisi kolom 'line_name' dan 'Total Output'

fig, ax = plt.subplots(figsize=(6, 4))

# Gambar Bar Chart
sns.barplot(data=dataset, x='line_name', y='Total Output', ax=ax, palette='Blues_d')

# Tambahkan label angka penuh di atas setiap batang
for p in ax.patches:
    # Ambil nilai tinggi batang dan format menjadi ribuan dengan koma
    val = f"{int(p.get_height()):,}"
    ax.annotate(val, 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 8), 
                textcoords='offset points', 
                fontsize=9, fontweight='bold')

ax.set_title("Total Output per Lini Produksi", fontsize=12, fontweight='bold')
ax.set_xlabel("Lini Produksi")
ax.set_ylabel("Total Output (unit)")

# Hilangkan garis tepi atas dan kanan agar rapi
sns.despine()

plt.tight_layout()
plt.show()
```

### Contoh B: Menampilkan Kartu Angka Tunggal (KPI Card Custom)
Jika Anda hanya ingin menampilkan satu angka besar secara penuh tanpa singkatan "K" di dashboard.

```python
import matplotlib.pyplot as plt

# dataset hanya berisi satu kolom berisi nilai tunggal dari Measure 'Total Output'
total_value = dataset['Total Output'].iloc[0]

fig, ax = plt.subplots(figsize=(4, 2))

# Tulis angka secara penuh dengan format pemisah ribuan koma
formatted_text = f"{int(total_value):,}"

# Tampilkan teks di tengah kanvas kosong
ax.text(0.5, 0.5, formatted_text, 
        fontsize=24, fontweight='bold', 
        ha='center', va='center', 
        color='#1B365D')

# Hilangkan seluruh sumbu koordinat agar terlihat seperti KPI Card bersih
ax.axis('off')

plt.show()
```

---

## 4. Keuntungan & Kekurangan Python Visual

| Kelebihan | Kekurangan |
|---|---|
| **Kontrol Penuh:** Format teks, label, warna, dan jenis grafik bisa diatur 100% via kode tanpa batasan menu Power BI. | **Performa:** Waktu rendering sedikit lebih lambat dibanding visual asli Power BI saat memuat halaman pertama kali. |
| **Bebas Masalah Versi:** Tidak perlu khawatir menu hilang karena perubahan update UI Power BI. | **Interaktivitas:** Visual Python bersifat statis (tidak memiliki animasi hover bawaan seinteraktif chart asli Power BI). |
