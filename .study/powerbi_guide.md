# Panduan Implementasi Dashboard Power BI - PT Voltec Indonesia
## Analisis Produksi Elektronik H2 2024

Panduan ini menjelaskan langkah-langkah untuk membangun dashboard interaktif di Power BI menggunakan dataset bersih yang telah kita siapkan di folder `data/cleaned/`.

---

## 1. Persiapan & Sumber Data (Data Connection)

1. Buka aplikasi **Power BI Desktop**.
2. Pilih **Get Data** > **Text/CSV**.
3. Hubungkan ke 5 file CSV bersih berikut dari folder `data/cleaned/`:
   * `production_fact_cleaned.csv`
   * `line_dim_cleaned.csv`
   * `machine_dim_cleaned.csv`
   * `product_dim_cleaned.csv`
   * `shift_dim_cleaned.csv`
4. Klik **Transform Data** untuk masuk ke **Power Query Editor** guna memastikan tipe data sudah sesuai.

---

## 2. Pemodelan Data (Data Modeling)

Masuk ke tab **Model View** di sebelah kiri Power BI. Susun hubungan antar tabel membentuk **Star Schema** dengan relasi *1-to-many (1:*)* dan arah filter *Single* dari tabel dimensi ke tabel fakta:

* `line_dim_cleaned(line_id)` $\rightarrow$ `production_fact_cleaned(line_id)`
* `machine_dim_cleaned(machine_id)` $\rightarrow$ `production_fact_cleaned(machine_id)`
* `product_dim_cleaned(product_id)` $\rightarrow$ `production_fact_cleaned(product_id)`
* `shift_dim_cleaned(shift_id)` $\rightarrow$ `production_fact_cleaned(shift_id)`

*(Catatan: Buat tabel kalender/tanggal tambahan jika ingin analisis time-intelligence yang lebih kaya, atau gunakan kolom `production_date` bawaan).*

---

## 3. Rumus DAX (Measure & Calculated Columns)

Buat tabel khusus bernama `_Measures` untuk menyimpan rumus-rumus berikut agar dashboard lebih rapi dan dinamis:

### A. Output & Target Qty
```dax
Total Output = SUM(production_fact_cleaned[output_qty])
```
```dax
Total Target = SUM(production_fact_cleaned[target_qty])
```

### B. Achievement Rate (%)
```dax
Achievement Rate = 
DIVIDE(
    [Total Output],
    [Total Target],
    0
)
```

### C. Defect Rate (%)
```dax
Total Defect = SUM(production_fact_cleaned[defect_qty])
```
```dax
Defect Rate = 
DIVIDE(
    [Total Defect],
    [Total Output],
    0
)
```

### D. Downtime Metrics
```dax
Total Downtime (Min) = SUM(production_fact_cleaned[downtime_minutes])
```
```dax
Avg Downtime per Batch = AVERAGE(production_fact_cleaned[downtime_minutes])
```

---

## 4. Struktur & Layout Visualisasi (Dashboard Layout)

Rancang layout dashboard menjadi **2 halaman utama** dengan tema **Sleek Dark Mode** atau **Clean White & Blue** untuk kesan premium.

### Halaman 1: Executive Production Summary
* **Tujuan**: Memberikan gambaran performa produksi bagi manajemen level C.
* **Elemen Visual**:
  1. **KPI Cards (Baris Atas)**:
     * Card 1: Total Output (Format: Million/Ribuan)
     * Card 2: Achievement Rate (Format: %, target > 90% berwarna Hijau, < 90% Merah)
     * Card 3: Defect Rate (Format: %, target < 3% Hijau, > 4% Merah)
     * Card 4: Total Downtime (Menit/Jam)
  2. **Line & Clustered Column Chart (Tengah-Kiri)**:
     * X-Axis: `production_date` (Trend Harian/Mingguan)
     * Column Value: `Total Output` & `Total Target`
     * Line Value: `Achievement Rate`
  3. **Donut/Pie Chart (Tengah-Kanan)**:
     * Legend: `line_name`
     * Value: `Total Output` (Untuk melihat kontribusi/share tiap line)
  4. **Bar Chart (Bawah-Kiri)**:
     * Y-Axis: `product_name`
     * X-Axis: `Defect Rate` (Dapatkan list produk dengan defect tertinggi)
  5. **Slicer (Filter Panel - Kiri/Atas)**:
     * Filter berdasarkan: `production_date` (Date Slider), `shift_name`, dan `line_name`.

### Halaman 2: Equipment & Shift Performance
* **Tujuan**: Untuk tim operasional pabrik melakukan investigasi bottleneck mesin dan shift kerja.
* **Elemen Visual**:
  1. **Scatter Plot (Kiri-Atas)**:
     * X-Axis: Usia Mesin (`2024 - purchase_year`)
     * Y-Axis: `Avg Downtime per Batch`
     * Bubble Size: `Total Output`
     * Legend: `machine_type`
  2. **Top 10 Downtime Machines (Kanan-Atas - Horizontal Bar Chart)**:
     * Y-Axis: `machine_name`
     * X-Axis: `Total Downtime (Min)`
  3. **Heatmap Matrix (Bawah-Kiri)**:
     * Rows: `line_name`
     * Columns: `shift_name`
     * Value / Conditional Formatting: `Defect Rate` (Warnai gradasi merah untuk defect tertinggi)
  4. **Table Details (Bawah-Kanan)**:
     * Columns: `machine_name`, `supervisor`, `Total Output`, `Total Defect`, `Defect Rate`, `Total Downtime`.

---

## 5. Tips Estetika Visual & Desain Premium

1. **Palet Warna**:
   * Warna Utama (Primary): Dark Blue (`#1B365D`) atau Teal (`#008080`) untuk visualisasi data umum.
   * Warna Kontras (Accent): Red/Coral (`#E74C3C`) untuk highlight defect, Gold/Orange (`#F39C12`) untuk downtime.
2. **Kerapian Layout**: Gunakan fitur *Gridlines* dan *Snap to Grid* di Power BI untuk menyelaraskan setiap chart.
3. **Tooltip**: Aktifkan custom tooltip pada Scatter Plot dan Bar Chart agar ketika kursor diarahkan, muncul nama supervisor, usia mesin, dan detail lainnya.
4. **Conditional Formatting**: Gunakan aturan warna pada tabel dan card agar pembaca langsung tahu KPI mana yang sedang kritis (Merah) atau aman (Hijau).
