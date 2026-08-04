# Studi Mandiri: Konsep Dasar Data Manufaktur & Peran SQL
Dokumen ini dibuat untuk merangkum penjelasan konsep dasar dan peran SQL dalam portofolio analisis produksi PT Voltec Indonesia.

---

## 1. Struktur Data Produksi Harian (Logical Mapping)

### Pertanyaan Bisnis
*Bagaimana menghitung jumlah baris entry data riil setiap hari? Apakah rumusnya langsung mengalikan semua dimensi?*

### Penjelasan Konsep
Secara teoritis, jika semua kombinasi tidak terbatas, jumlah baris adalah perkalian seluruh dimensi. Namun di pabrik nyata (dan data generator kita), ada batasan relasi logis:

1. **Mesin Terikat ke Lini Tertentu:**
   * Total mesin = 15 mesin.
   * Lini produksi = 5 Lini (`Line A` - `Line E`).
   * Setiap lini secara eksklusif memiliki 3 mesin (misal: Line A hanya memiliki `SMT-01`, `SMT-02`, dan `SMT-03`). 
   * Jadi, kombinasi mesin dan lini tetap berjumlah **15 kombinasi unik** per hari (bukan $5 \times 15 = 75$).

2. **Produk Terikat ke Lini Tertentu:**
   * Setiap lini dirancang khusus untuk memproduksi **3 jenis produk** dari total 5 produk yang ada.

### Kalkulasi Riil Jumlah Baris per Hari:
   $$\text{Baris/Hari} = 15\text{ kombinasi (Lini \& Mesin)} \times 3\text{ Shift} \times 3\text{ Produk per Lini} = 135\text{ baris/hari}$$

* **Verifikasi Total Data (H2 2024 - 184 Hari):**
  $$184\text{ Hari} \times 135\text{ baris/hari} = 24.840\text{ baris fakta}$$

---

## 2. Posisi dan Peran SQL dalam Portofolio

Di dunia industri, data besar disimpan di database server (bukan file lokal). Posisi SQL dalam portofolio ini adalah sebagai **mesin analisis utama sebelum visualisasi**.

### Arsitektur Alur Data
1. **Python (Pandas):** Digunakan untuk data cleaning dan preprocessing awal.
2. **SQL Database (DDL & Schema):** Berperan sebagai media penyimpanan terstruktur (*Star Schema*).
3. **SQL Query (DML & Aggregation):** Digunakan untuk melakukan perhitungan bisnis berat secara langsung di database.
4. **Power BI:** Mengimpor data yang sudah di-query/agregasi dari SQL untuk dijadikan dashboard visual interaktif.

### Peta Konteks 15 Query Analisis SQL (`analysis.sql`)

Query di dalam proyek ini dibagi ke dalam 4 kelompok fungsional untuk menjawab kebutuhan bisnis nyata:

| Kelompok Analisis | Deskripsi / Pertanyaan Bisnis | Fitur SQL yang Digunakan |
|---|---|---|
| **A. Laporan Operasional Dasar** | Menghitung KPI utama total output, defect rate, dan performa antar lini produksi. | `SUM`, `COUNT`, `JOIN`, `GROUP BY` |
| **B. Tren & Tren Waktu** | Menganalisis pertumbuhan bulanan dan performa jangka panjang. | `SUM OVER` (Running Total), `AVG OVER ROWS` (Moving Average), `LAG` (Month-on-Month Growth) |
| **C. Investigasi Bottleneck** | Mengidentifikasi mesin rusak, downtime di atas rata-rata standar, dan usulan maintenance. | `Subquery`, `HAVING`, `CASE WHEN` |
| **D. Analisis Kompleks** | Merangking lini terbaik per bulan dan mendeteksi anomali output di luar batas normal. | `RANK()`, `CTE (Common Table Expression)`, `STDDEV` (Standar Deviasi) |
