# Studi Mandiri: Membuat Kartu KPI (Card) Menggunakan Python di Power BI

Dokumen ini berisi panduan dan kode script siap pakai untuk membuat kartu KPI kustom menggunakan **Python Visual** di Power BI, khusus untuk menampilkan metrik `Total Output`, `Total Target`, dan `Defect Rate` dalam format angka penuh (lengkap dengan label judul dan dekorasi).

---

## 1. Persiapan di Power BI Desktop
1. Klik ikon **Python visual** (`Py`) di panel visualisasi Anda.
2. Seret Measure yang ingin ditampilkan ke panel **Values**.
   * Misal: Seret Measure `Total Output` ke dalam panel Values.
3. Buka editor skrip Python di bagian bawah.

---

## 2. Kode Script Python untuk Kartu KPI (Card Visual)

Berikut adalah beberapa script template yang didesain agar terlihat modern, bersih, memiliki judul, serta menampilkan angka secara penuh:

### Template A: Kartu KPI "Total Output" (Angka Penuh dengan Ribuan Koma)

```python
import matplotlib.pyplot as plt

# 1. Mengambil data dari Power BI (dataset)
# dataset otomatis memuat baris data dari Measure 'Total Output'
total_val = dataset['Total Output'].iloc[0]

# Penanganan jika data kosong (Null/NaN)
if total_val is None or str(total_val) == 'nan':
    total_val = 0

# 2. Mengatur Canvas Grafik (Fig size: Lebar 4 inci, Tinggi 2 inci)
fig, ax = plt.subplots(figsize=(4, 2))

# 3. Format angka bulat penuh dengan pemisah ribuan (contoh: 24,840)
formatted_number = f"{int(total_val):,}"

# 4. Menambahkan teks judul di atas angka
ax.text(0.5, 0.75, "TOTAL OUTPUT", 
        fontsize=10, fontweight='bold', color='#7F8C8D', 
        ha='center', va='center')

# 5. Menambahkan teks angka utama di tengah
ax.text(0.5, 0.4, formatted_number, 
        fontsize=28, fontweight='bold', color='#1B365D', 
        ha='center', va='center')

# 6. Menghilangkan frame sumbu koordinat agar bersih seperti kartu
ax.axis('off')

# 7. Tampilkan visualisasi
plt.tight_layout()
plt.show()
```

---

### Template B: Kartu KPI "Defect Rate" (Angka Persentase Cantik)

Untuk persentase, kita perlu mengalikan dengan 100 jika nilainya desimal kecil (misal `0.035` menjadi `3.50%`).

```python
import matplotlib.pyplot as plt

# Ambil data dari Power BI (dataset)
defect_rate = dataset['Defect Rate'].iloc[0]

if defect_rate is None or str(defect_rate) == 'nan':
    defect_rate = 0

# Jika Power BI mengirimkan nilai dalam format desimal murni (misal 0.035), ubah ke persen
if defect_rate < 1.0:
    defect_rate_pct = defect_rate * 100
else:
    defect_rate_pct = defect_rate

fig, ax = plt.subplots(figsize=(4, 2))

# Format dengan 2 angka di belakang koma (contoh: 3.42%)
formatted_number = f"{defect_rate_pct:.2f}%"

# Pilih warna teks: jika defect rate > 4% (merah), jika tidak (hijau/biru)
text_color = '#E74C3C' if defect_rate_pct > 4 else '#27AE60'

# Judul
ax.text(0.5, 0.75, "DEFECT RATE", 
        fontsize=10, fontweight='bold', color='#7F8C8D', 
        ha='center', va='center')

# Nilai Utama
ax.text(0.5, 0.4, formatted_number, 
        fontsize=28, fontweight='bold', color=text_color, 
        ha='center', va='center')

ax.axis('off')

plt.tight_layout()
plt.show()
```

---

## 3. Cara Mengatur Ukuran dan Background Visual
Agar visual Python ini menyatu dengan dashboard Power BI Anda:
1. Klik visual Python di kanvas.
2. Pergi ke tab **Format Visual** (ikon kuas lukis 🖌️) > pilih **General** (Umum).
3. Matikan opsi **Background** (atur ke *Off*) agar background visual transparan dan mengikuti tema dashboard utama Anda.
4. Matikan opsi **Title** (Judul visual bawaan Power BI) karena kita sudah menulis judulnya secara langsung menggunakan kode Python.
