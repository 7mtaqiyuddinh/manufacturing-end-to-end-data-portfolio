# Tutorial Belajar DAX Power BI untuk Pemula

Panduan ini dirancang khusus untuk Anda yang baru pertama kali mengenal **Power BI** dan **DAX (Data Analysis Expressions)**. Kita akan membedah konsep dasar, cara penerapannya di Power BI Desktop langkah demi langkah, dan penjelasan logika di balik setiap rumus yang kita gunakan.

---

## 1. Apa itu DAX? (Konsep Dasar)

**DAX (Data Analysis Expressions)** adalah bahasa formula yang digunakan di Power BI untuk melakukan perhitungan kustom. Jika Anda terbiasa dengan rumus Excel (seperti `SUM`, `AVERAGE`, `IF`), DAX memiliki kemiripan, tetapi bekerja dengan cara yang berbeda karena berorientasi pada **kolom dan tabel (Data Model)**, bukan sel individu.

Di Power BI, ada dua cara utama membuat perhitungan dengan DAX:

| Fitur | Calculated Column (Kolom Turunan) | Measure (Ukuran Dinamis) |
|---|---|---|
| **Cara Kerja** | Dihitung baris demi baris secara statis dan langsung disimpan di dalam memori. | Hanya dihitung secara dinamis saat visualisasi dimuat (bergantung filter/slicer yang Anda pilih). |
| **Kapan Digunakan?**| Jika nilainya ingin dijadikan filter/slicer (misal: kategori usia mesin, nama bulan). | Jika nilainya adalah perhitungan agregasi angka (misal: total output, defect rate, rata-rata). |
| **Beban Memori** | Mengonsumsi penyimpanan RAM & File karena data disimpan fisik. | Sangat hemat memori karena dihitung "on-the-fly" (saat itu juga). |

> [!TIP]
> **Aturan Emas Data Analyst:** Selalu gunakan **Measure** kecuali Anda benar-benar butuh membuat kolom baru untuk keperluan filter/slicer.

---

## 2. Cara Membuat Tabel Khusus `_Measures` (Best Practice)

Secara bawaan, Power BI akan meletakkan Measure baru di dalam tabel tempat Anda klik kanan. Untuk proyek profesional, kita sebaiknya membuat tabel kosong khusus bernama `_Measures` untuk menampung seluruh rumus DAX agar mudah dicari.

### Langkah-langkah:
1. Buka **Power BI Desktop**.
2. Pada menu atas (Ribbon), pilih tab **Home** > klik **Enter Data**.
3. Di jendela yang muncul:
   * Ubah nama tabel (*Table Name*) di bagian bawah menjadi: `_Measures`.
   * Biarkan kolom tabelnya kosong (tidak perlu diisi apa-apa).
   * Klik **Load**.
4. Sekarang Anda memiliki tabel baru bernama `_Measures` di panel kanan (fields).

---

## 3. Langkah Demi Langkah Membuat Measure Baru

Setiap kali Anda ingin mengetikkan rumus DAX:
1. Klik kanan pada tabel `_Measures` di panel kanan.
2. Pilih **New Measure**.
3. Di kolom rumus (*Formula Bar*) yang muncul di atas halaman, ketikkan rumusnya.
4. Klik tombol centang ($\checkmark$) di sebelah kiri formula bar atau tekan **Enter** untuk menyimpan.

---

## 4. Penjelasan Logika Rumus DAX Portofolio Kita

Mari kita bedah rumus-rumus DAX yang kita gunakan satu per satu:

### Kelompok A: Agregasi Dasar

#### 1. Total Output
```dax
Total Output = SUM(production_fact_cleaned[output_qty])
```
* **Cara kerja:** Menjumlahkan seluruh angka di kolom `output_qty` pada tabel fakta. Jika di halaman visualisasi Anda memfilter "Line A", rumus ini akan otomatis menyesuaikan hanya menjumlahkan output dari Line A.

#### 2. Total Target
```dax
Total Target = SUM(production_fact_cleaned[target_qty])
```
* **Cara kerja:** Menjumlahkan total target produksi yang seharusnya dicapai.

#### 3. Total Defect
```dax
Total Defect = SUM(production_fact_cleaned[defect_qty])
```
* **Cara kerja:** Menjumlahkan total unit produk yang rusak (defect).

---

### Kelompok B: Rasio dan Persentase

#### 4. Achievement Rate (%)
```dax
Achievement Rate = 
DIVIDE(
    [Total Output],
    [Total Target],
    0
)
```
* **Mengapa memakai `DIVIDE` bukan pembagian biasa (`/`)?**
  Di dalam matematika, pembagian dengan angka nol ($X / 0$) akan menghasilkan error (*division by zero*). Fungsi `DIVIDE` di DAX memiliki pengaman otomatis. Jika `Total Target` bernilai 0 (misalnya pada hari libur pabrik), maka secara otomatis rumus ini akan menghasilkan nilai alternatif `0` (parameter ketiga), tanpa merusak visualisasi dashboard Anda.

#### 5. Defect Rate (%)
```dax
Defect Rate = 
DIVIDE(
    [Total Defect],
    [Total Output],
    0
)
```
* **Cara kerja:** Membagi jumlah produk defect dengan total produk yang berhasil diproduksi untuk mengetahui tingkat kerusakan kualitas.

---

### Kelompok C: Metrik Downtime

#### 6. Total Downtime (Min)
```dax
Total Downtime (Min) = SUM(production_fact_cleaned[downtime_minutes])
```
* **Cara kerja:** Akumulasi total waktu breakdown mesin dalam satuan menit.

#### 7. Avg Downtime per Batch
```dax
Avg Downtime per Batch = AVERAGE(production_fact_cleaned[downtime_minutes])
```
* **Cara kerja:** Menghitung rata-rata durasi downtime mesin pada setiap batch shift produksi.

---

## 5. Cara Mengubah Format Angka (Formatting)

Setelah membuat Measure, angkanya mungkin akan terlihat kasar (misalnya `0.0456` bukannya `4.56%`). Anda harus mengatur tampilannya agar cantik di dashboard.

### Langkah-langkah:
1. Klik Measure yang baru Anda buat (misal: `Defect Rate`) di panel kanan.
2. Di menu atas, tab **Measure tools** akan otomatis aktif.
3. Di bagian **Formatting**:
   * Untuk `Defect Rate` & `Achievement Rate`: Klik simbol **`%` (Percentage)** dan atur desimalnya menjadi `2` atau `1`.
   * Untuk `Total Output` & `Total Target`: Klik simbol **, (Comma)** untuk memberikan pemisah ribuan (misal: `1,250,000`).
