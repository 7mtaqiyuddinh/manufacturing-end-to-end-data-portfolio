# 🧠 Proses Berpikir Seorang Data Analyst: Dari Masalah Bisnis ke Insight & Rekomendasi

> Dokumen ini menjelaskan **bagaimana seorang Data Analyst berpikir secara sistematis** — dari pertama kali menerima masalah bisnis hingga menghasilkan insight yang bisa ditindaklanjuti (*actionable insights*). Semua contoh mengacu pada proyek **PT Voltec Indonesia**.

---

## 📋 Daftar Isi

1. [Gambaran Besar: Alur Berpikir End-to-End](#1-gambaran-besar-alur-berpikir-end-to-end)
2. [Fase 1: Memahami Masalah Bisnis (Business Understanding)](#2-fase-1-memahami-masalah-bisnis)
3. [Fase 2: Menerjemahkan ke Pertanyaan Data (Question Framing)](#3-fase-2-menerjemahkan-ke-pertanyaan-data)
4. [Fase 3: Mengumpulkan & Membersihkan Data (Data Wrangling)](#4-fase-3-mengumpulkan--membersihkan-data)
5. [Fase 4: Eksplorasi & Analisis (EDA + SQL Analysis)](#5-fase-4-eksplorasi--analisis)
6. [Fase 5: Menyintesis Temuan Menjadi Insight](#6-fase-5-menyintesis-temuan-menjadi-insight)
7. [Fase 6: Merumuskan Rekomendasi Bisnis](#7-fase-6-merumuskan-rekomendasi-bisnis)
8. [Fase 7: Menyajikan Hasil (Storytelling & Dashboard)](#8-fase-7-menyajikan-hasil)
9. [Pola Pikir Kritis: Yang Membedakan Analyst Biasa dan Analyst Hebat](#9-pola-pikir-kritis)
10. [Checklist Proses Berpikir](#10-checklist)

---

## 1. Gambaran Besar: Alur Berpikir End-to-End

Berikut adalah keseluruhan proses berpikir seorang Data Analyst yang terjadi secara **iteratif** (bukan linear):

```mermaid
flowchart TD
    A["🏭 <b>MASALAH BISNIS</b><br/>Manajemen melaporkan:<br/>Output turun & Defect naik"] --> B

    B["🤔 <b>BUSINESS UNDERSTANDING</b><br/>Pahami konteks:<br/>Siapa stakeholder?<br/>Apa KPI-nya?<br/>Sejak kapan masalahnya?"] --> C

    C["❓ <b>QUESTION FRAMING</b><br/>Terjemahkan masalah bisnis<br/>menjadi 6 pertanyaan data<br/>yang bisa diukur & dijawab"] --> D

    D["🧹 <b>DATA WRANGLING</b><br/>Kumpulkan data mentah<br/>Bersihkan: missing values,<br/>duplikat, outlier, validasi bisnis"] --> E

    E["🔍 <b>EXPLORATORY DATA ANALYSIS</b><br/>Visualisasi pola & tren<br/>Hitung korelasi<br/>Identifikasi anomali"] --> F

    F["⚙️ <b>SQL ANALYSIS</b><br/>Analisis relasional mendalam<br/>Window Functions, CTE, Ranking<br/>Cross-dimensional analysis"] --> G

    G["💡 <b>SINTESIS INSIGHT</b><br/>Gabungkan temuan menjadi<br/>cerita yang koheren<br/>Kuantifikasi dampak bisnis"] --> H

    H["📋 <b>REKOMENDASI</b><br/>Rumuskan tindakan spesifik<br/>Prioritaskan: Impact vs Effort<br/>Buat timeline implementasi"] --> I

    I["📊 <b>STORYTELLING & DASHBOARD</b><br/>Visualisasi interaktif Power BI<br/>Presentasi ke stakeholder<br/>Executive Summary"]

    E -->|"Data tidak cukup<br/>atau pertanyaan baru muncul"| C
    F -->|"Temuan baru memicu<br/>pertanyaan tambahan"| C
    G -->|"Insight membutuhkan<br/>data lebih dalam"| E

    style A fill:#ff6b6b,stroke:#c92a2a,color:#fff
    style B fill:#ffa94d,stroke:#e67700,color:#fff
    style C fill:#ffd43b,stroke:#f08c00,color:#333
    style D fill:#69db7c,stroke:#2b8a3e,color:#333
    style E fill:#4ecdc4,stroke:#0ca678,color:#333
    style F fill:#74c0fc,stroke:#1971c2,color:#333
    style G fill:#b197fc,stroke:#7048e8,color:#fff
    style H fill:#f783ac,stroke:#c2255c,color:#333
    style I fill:#e599f7,stroke:#9c36b5,color:#333
```

> **Poin Penting:** Perhatikan panah yang kembali ke atas. Proses ini **bukan linear satu arah**. Seorang analyst yang baik akan sering kembali ke fase sebelumnya ketika menemukan data baru atau pertanyaan baru muncul dari hasil analisis.

---

## 2. Fase 1: Memahami Masalah Bisnis

### Apa yang terjadi di kepala seorang Analyst?

Ketika manajemen PT Voltec berkata *"Output produksi turun dan defect meningkat"*, seorang analyst **tidak langsung membuka data**. Yang pertama dilakukan adalah **bertanya**:

```mermaid
mindmap
  root(("🏭 Masalah Bisnis:<br/>Output Turun &<br/>Defect Naik"))
    ("👤 Siapa yang terdampak?")
      ("Manajemen Operasional")
      ("Tim Quality Control")
      ("Divisi Keuangan — biaya rework")
    ("📅 Kapan mulai terjadi?")
      ("H2 2024 — Juli sampai Desember")
      ("Apakah mendadak atau gradual?")
    ("📏 Bagaimana mengukurnya?")
      ("Achievement Rate — output vs target")
      ("Defect Rate — defect vs output")
      ("Downtime — menit mesin tidak beroperasi")
    ("🔧 Apa variabel yang mungkin relevan?")
      ("5 Lini produksi — Line A sampai E")
      ("15 Mesin — usia bervariasi")
      ("3 Shift kerja — Pagi, Siang, Malam")
      ("5 Produk — kompleksitas beda-beda")
```

### Proses berpikir konkretnya:

| Pertanyaan Internal Analyst | Jawaban yang Dicari | Sumber Informasi |
|---|---|---|
| "Seberapa parah masalahnya?" | Target achievement turun berapa persen? | Data produksi historis |
| "Apakah semua lini terdampak atau hanya beberapa?" | Perbanding performa antar lini | Data per line |
| "Apakah ada pola waktu?" | Tren bulanan, mingguan, per shift | Data dengan timestamp |
| "Apa faktor yang bisa dikontrol?" | Mesin (maintenance), Shift (rotasi), QC (prosedur) | Domain knowledge manufaktur |

> **Kunci Fase 1:** Jangan langsung koding. Pahami dulu **konteks bisnis** dan **siapa yang akan menggunakan hasil analisis Anda**. Manajemen tidak peduli dengan koefisien korelasi — mereka peduli dengan *"berapa uang yang hilang dan apa yang harus dilakukan?"*

---

## 3. Fase 2: Menerjemahkan ke Pertanyaan Data

### Dari masalah abstrak ke pertanyaan terukur

Ini adalah **keterampilan paling penting** seorang Data Analyst: mengubah keluhan bisnis yang *vague* menjadi pertanyaan yang bisa dijawab dengan data.

```mermaid
flowchart TD
    subgraph BISNIS["🏢 Bahasa Bisnis"]
        direction TB
        B1["Output turun akhir-akhir ini"]
        B2["Banyak produk cacat"]
        B3["Mesin sering rusak"]
    end

    subgraph TRANSISI["🔄 Proses Translasi"]
        direction TB
        T1["Operasionalisasi:<br/>Definisikan metrik"]
        T2["Dekomposisi:<br/>Pecah per dimensi"]
        T3["Temporalisasi:<br/>Tentukan periode"]
    end

    subgraph DATA["📊 Bahasa Data"]
        direction TB
        D1["Q1: Tren output harian & bulanan<br/>— gradual atau mendadak?"]
        D2["Q2: Line mana achievement<br/>rate paling rendah?"]
        D3["Q3: Shift mana defect rate<br/>paling tinggi?"]
        D4["Q4: Mesin mana downtime<br/>terbesar & kaitan usia?"]
        D5["Q5: Korelasi kuantitatif<br/>downtime vs output?"]
        D6["Q6: Produk mana defect<br/>rate tertinggi?"]
    end

    BISNIS --> TRANSISI --> DATA

    style BISNIS fill:#ffebee,stroke:#c62828
    style TRANSISI fill:#fff3e0,stroke:#e65100
    style DATA fill:#e8f5e9,stroke:#2e7d32
```

### Tiga teknik translasi yang digunakan:

**1. Operasionalisasi** — Mengubah kata-kata abstrak menjadi metrik terukur:
- *"Output turun"* → Achievement Rate = `SUM(output_qty) / SUM(target_qty) × 100%`
- *"Banyak cacat"* → Defect Rate = `SUM(defect_qty) / SUM(output_qty) × 100%`
- *"Mesin rusak"* → Total Downtime = `SUM(downtime_minutes)`

**2. Dekomposisi** — Memecah masalah besar menjadi dimensi-dimensi:
- Per **waktu** (bulan, hari, shift)
- Per **lini produksi** (Line A-E)
- Per **mesin** (15 mesin, usia berbeda)
- Per **produk** (5 produk, kompleksitas berbeda)

**3. Temporalisasi** — Menentukan periode dan granularity:
- Periode: H2 2024 (Juli-Desember = 184 hari)
- Granularity: harian untuk tren, bulanan untuk executive report

---

## 4. Fase 3: Mengumpulkan & Membersihkan Data

### Proses berpikir saat Data Wrangling

Seorang analyst tidak membersihkan data secara acak. Ada **logika keputusan** di setiap langkah:

```mermaid
flowchart TD
    A["📥 Data Mentah Masuk<br/>~25.000+ baris"] --> B{"🔍 Cek Kualitas Data"}
    
    B --> C["Missing Values<br/>output_qty: 2%<br/>defect_qty: 1.5%<br/>downtime: 1%<br/>machine_id: 0.5%"]
    B --> D["Duplikat<br/>~80 baris identik"]
    B --> E["Nilai Tidak Valid<br/>20 baris output negatif<br/>18 baris defect > output"]
    B --> F["Outlier<br/>15 baris downtime > 480 menit"]
    
    C --> C1{"Mengapa tidak hapus<br/>baris yang kosong?"}
    C1 --> C2["Karena kehilangan baris = <br/>kehilangan informasi dimensi lain.<br/>→ Solusi: <b>Median Imputation</b><br/>per grup produk/mesin"]

    D --> D1["Hapus duplikat<br/>dengan drop_duplicates()"]

    E --> E1{"Mengapa tidak hapus saja?"}
    E1 --> E2["Output negatif → error input<br/>→ Ubah ke absolute value<br/>Defect > output → tidak logis<br/>→ Clip defect = output"]
    
    F --> F1{"Mengapa IQR Clipping<br/>bukan hapus outlier?"}
    F1 --> F2["Di manufaktur, downtime panjang<br/>adalah <b>informasi penting</b><br/>(bukan noise).<br/>→ Clip ke batas atas IQR<br/>agar distribusi terjaga"]

    C2 --> G["✅ Data Bersih<br/>~25.000 baris valid"]
    D1 --> G
    E2 --> G
    F2 --> G

    style A fill:#ffcdd2,stroke:#c62828
    style G fill:#c8e6c9,stroke:#2e7d32
    style C1 fill:#fff9c4,stroke:#f57f17
    style E1 fill:#fff9c4,stroke:#f57f17
    style F1 fill:#fff9c4,stroke:#f57f17
```

### Poin kritis yang perlu dipahami:

> **Mengapa Median, bukan Mean?**
> Karena data produksi yang tercampur outlier membuat nilai rata-rata (mean) menjadi terdistorsi. Median lebih *robust* — tidak terpengaruh oleh nilai ekstrim. Contoh: jika 10 batch punya downtime [5, 8, 10, 12, 15, 300], mean = 58.3 (tidak representatif), sedangkan median = 11 (lebih akurat).

> **Mengapa IQR Clipping, bukan Remove?**
> Menghapus outlier berarti menghapus seluruh baris data — termasuk informasi tentang line, shift, produk, dan tanggal di baris tersebut. Clipping mempertahankan baris tapi membatasi nilai ekstrimnya.

---

## 5. Fase 4: Eksplorasi & Analisis

### Dua jalur analisis yang saling melengkapi

```mermaid
flowchart TD
    A["✅ Data Bersih"] --> B["🐍 EDA dengan Python"]
    A --> C["🗄️ Analisis dengan SQL"]
    
    subgraph EDA["EDA — Menemukan Pola Visual"]
        B --> B1["📉 Tren Waktu<br/>Line plot output bulanan<br/>→ Temukan: penurunan gradual"]
        B --> B2["📊 Analisis Pareto<br/>Bar chart defect per produk<br/>→ Temukan: Control Board dominan"]
        B --> B3["🔵 Scatter Plot & Korelasi<br/>Downtime vs Output<br/>→ Temukan: r = negatif signifikan"]
        B --> B4["📦 Box Plot per Shift<br/>Distribusi defect rate<br/>→ Temukan: Shift Malam outlier"]
    end
    
    subgraph SQL["SQL — Analisis Relasional Mendalam"]
        C --> C1["🔢 Agregasi Multi-dimensi<br/>GROUP BY line, shift, mesin, bulan<br/>→ Temukan: kombinasi Line-Shift terburuk"]
        C --> C2["📈 Window Functions<br/>LAG untuk MoM Growth<br/>→ Temukan: penurunan semakin curam"]
        C --> C3["🏆 Ranking & CTE<br/>RANK per bulan per line<br/>→ Temukan: Line A turun di Desember"]
        C --> C4["🔧 Maintenance Priority<br/>CASE WHEN usia + downtime<br/>→ Temukan: 4 mesin PRIORITAS TINGGI"]
    end

    B1 & B2 & B3 & B4 --> D["💡 Temuan EDA"]
    C1 & C2 & C3 & C4 --> E["💡 Temuan SQL"]
    D & E --> F["🧩 SINTESIS<br/>Gabungkan semua temuan"]

    style A fill:#c8e6c9,stroke:#2e7d32
    style F fill:#e1bee7,stroke:#7b1fa2
```

### Cara berpikir saat EDA — bukan asal buat grafik!

Setiap visualisasi dibuat untuk **menjawab pertanyaan spesifik**:

| Visualisasi | Pertanyaan yang Dijawab | Apa yang Dicari | Apa yang Ditemukan |
|---|---|---|---|
| Line Plot output bulanan | Q1: Tren output gradual atau mendadak? | Apakah garis menurun secara konsisten? | Ya — turun dari 98% ke 82% secara gradual |
| Box Plot defect per shift | Q3: Shift mana defect tertinggi? | Shift mana yang median-nya paling tinggi? | Shift Malam: ~5.1% vs Pagi: ~3.2% |
| Scatter plot downtime vs output | Q5: Ada korelasi? | Apakah titik-titik membentuk pola diagonal? | Ya — korelasi negatif |
| Bar chart defect per produk | Q6: Produk mana defect tertinggi? | Bar mana yang paling tinggi? | Control Board: 6.45% |

### Mengapa SQL dibutuhkan selain Python?

Python/Pandas kuat untuk visualisasi dan statistik dasar. Tapi SQL unggul untuk:
- **Cross-dimensional analysis**: Menggabungkan data dari beberapa tabel (JOIN line + shift + mesin + produk secara bersamaan)
- **Window Functions**: Menghitung running total, moving average, dan month-on-month growth yang kompleks
- **Reproducibility**: Query SQL bisa langsung dijadikan view untuk Power BI dashboard

---

## 6. Fase 5: Menyintesis Temuan Menjadi Insight

### Insight ≠ Fakta — Inilah yang membedakan analyst dari data entry!

```mermaid
flowchart LR
    subgraph FAKTA["📋 FAKTA<br/>(Apa yang data tunjukkan)"]
        F1["Achievement rate turun<br/>dari 98% ke 82%"]
        F2["Shift Malam defect rate 5.1%"]
        F3["REFLOW-01 downtime 45.2 menit"]
        F4["Control Board defect 6.45%"]
        F5["Korelasi downtime-output = negatif"]
        F6["Line A turun 20% di Desember"]
    end
    
    subgraph INSIGHT["💡 INSIGHT<br/>(Apa artinya bagi bisnis)"]
        I1["Degradasi mesin SISTEMIK<br/>bukan kecelakaan acak.<br/>Jika dibiarkan → kehilangan<br/>15-20% target tahunan"]
        I2["Kelelahan operator malam<br/>+ minim supervisi → biaya<br/>tambahan ~Rp 58 juta/bulan"]
        I3["Mesin > 5 tahun sudah<br/>melewati masa optimal →<br/>100-150 unit hilang/jam downtime"]
        I4["Kompleksitas produk =<br/>biaya kerugian tertinggi<br/>→ Rp 200 juta/semester"]
        I5["Downtime punya efek ganda:<br/>waktu hilang + warm-up<br/>→ Pengurangan 20% = +8-12% output"]
        I6["Penurunan Line A = kehilangan<br/>~4% total output perusahaan<br/>≈ satu line penuh"]
    end

    F1 --> I1
    F2 --> I2
    F3 --> I3
    F4 --> I4
    F5 --> I5
    F6 --> I6

    style FAKTA fill:#e3f2fd,stroke:#1565c0
    style INSIGHT fill:#fce4ec,stroke:#c62828
```

### Tiga komponen sebuah insight yang baik:

Setiap insight dalam `insights_and_recommendations.md` memiliki tiga bagian — dan ini bukan kebetulan:

```mermaid
flowchart TD
    A["💡 INSIGHT"] --> B["📊 <b>FAKTA</b><br/>Apa yang data tunjukkan?<br/><i>'Achievement rate turun dari<br/>98% ke 82% secara konsisten'</i>"]
    A --> C["🧠 <b>INTERPRETASI</b><br/>Mengapa ini terjadi?<br/><i>'Pola terlalu konsisten untuk<br/>fluktuasi musiman — ini degradasi<br/>mesin yang terakumulasi'</i>"]
    A --> D["💰 <b>DAMPAK BISNIS</b><br/>Berapa kerugiannya?<br/><i>'Jika berlanjut, perusahaan<br/>kehilangan 15-20% target<br/>tahunan → dampak revenue'</i>"]

    style A fill:#7c4dff,stroke:#311b92,color:#fff
    style B fill:#e8eaf6,stroke:#283593
    style C fill:#fff3e0,stroke:#e65100
    style D fill:#ffebee,stroke:#b71c1c
```

> **Mengapa ini penting?**
> - **Fakta saja** = laporan otomatis (bisa dihasilkan oleh script)
> - **Fakta + Interpretasi** = analisis (membutuhkan domain knowledge)
> - **Fakta + Interpretasi + Dampak Bisnis** = INSIGHT (membutuhkan business acumen)
>
> Seorang recruiter mencari orang yang bisa sampai di level ketiga.

---

## 7. Fase 6: Merumuskan Rekomendasi Bisnis

### Dari Insight ke Action Plan

Rekomendasi yang baik harus **spesifik, terukur, dan diprioritaskan**:

```mermaid
flowchart TD
    subgraph PRIORITAS["🎯 Priority Matrix: Impact vs Effort"]
        direction TB
        
        P1["<b>P1 - URGENT</b><br/>High Impact + Low/Medium Effort"]
        P2["<b>P2 - PENTING</b><br/>Medium-High Impact + Medium Effort"]
        P3["<b>P3 - QUICK WIN</b><br/>Low Impact + Low Effort"]
    end

    P1 --> R1["🔧 Preventive Maintenance<br/>Mesin Kritis<br/>Target: -30% downtime<br/>Dampak: +8-12% output"]
    P1 --> R2["🌙 QC Shift Malam<br/>Rotasi supervisor + fatigue mgmt<br/>Target: -20-30% defect shift malam<br/>Dampak: hemat ~Rp 58 juta/bulan"]
    
    P2 --> R3["🔬 QC Khusus Control Board<br/>Tim inspeksi + SPC<br/>Dampak: hemat ~Rp 200 juta/semester"]
    P2 --> R4["🏭 Audit Line A<br/>Audit mesin SMT + contingency<br/>Dampak: recovery ~4% total output"]
    
    P3 --> R5["📅 Optimasi Start-up Senin<br/>SOP pre-start + checklist<br/>Dampak: +2-3% output/minggu"]

    style P1 fill:#ff5252,stroke:#b71c1c,color:#fff
    style P2 fill:#ff9800,stroke:#e65100,color:#fff
    style P3 fill:#4caf50,stroke:#2e7d32,color:#fff
```

### Mengapa kita memprioritaskan?

Perusahaan tidak punya sumber daya tak terbatas. Seorang analyst yang baik tidak hanya berkata *"perbaiki semuanya"*, tapi memberikan **urutan tindakan** berdasarkan pertimbangan:

| Kriteria | Pertanyaan | Contoh di Proyek Ini |
|---|---|---|
| **Impact** | Seberapa besar dampak jika dilakukan? | Preventive Maintenance = +8-12% output (TINGGI) |
| **Effort** | Seberapa sulit/mahal implementasinya? | QC Shift Malam = tambah supervisor (RENDAH) |
| **Urgency** | Seberapa cepat harus ditindaklanjuti? | Mesin tua semakin degradasi setiap bulan (URGENT) |
| **Feasibility** | Apakah realistis dilakukan? | SPC untuk Control Board = butuh training (SEDANG) |

---

## 8. Fase 7: Menyajikan Hasil

### Dua audiens, dua cara penyajian

```mermaid
flowchart TD
    A["📊 Hasil Analisis"] --> B["👔 <b>Eksekutif/Manajemen</b>"]
    A --> C["🔧 <b>Tim Teknis/Operasional</b>"]
    
    B --> B1["Dashboard Power BI<br/>- KPI cards besar di atas<br/>- Tren visual yang jelas<br/>- Warna status: Hijau/Kuning/Merah<br/>- Filter interaktif per bulan/line"]
    B --> B2["Executive Summary di README<br/>- 6 temuan kunci (bukan 15)<br/>- Angka dampak bisnis dalam Rupiah<br/>- 3-5 rekomendasi prioritas<br/>- Timeline implementasi"]

    C --> C1["Detail Report<br/>- insights_and_recommendations.md<br/>- 7 temuan lengkap dengan interpretasi<br/>- 5 rekomendasi detail<br/>- Priority Matrix tabel"]
    C --> C2["Dokumentasi Teknis<br/>- SQL queries yang reproducible<br/>- Jupyter notebooks interaktif<br/>- Database schema ERD"]

    style B fill:#e3f2fd,stroke:#1565c0
    style C fill:#e8f5e9,stroke:#2e7d32
```

### Struktur Dashboard Power BI — Ada logika di baliknya:

```mermaid
flowchart TD
    subgraph PAGE1["📄 Halaman 1: Executive Summary"]
        direction TB
        KPI["🎯 KPI Cards di Atas<br/>Total Output | Achievement Rate |<br/>Defect Rate | Avg Downtime"]
        KPI --> TREND["📈 Tren Bulanan<br/>Line chart achievement Juli-Des<br/><i>→ Langsung terlihat masalahnya</i>"]
        KPI --> COMPARE["📊 Perbandingan Line & Shift<br/>Bar chart output per line<br/><i>→ Identifikasi bottleneck</i>"]
    end

    subgraph PAGE2["📄 Halaman 2: Detail Analysis"]
        direction TB
        DOWN["⏱️ Downtime Analysis<br/>Scatter plot downtime vs output<br/>Top mesin bermasalah"]
        DOWN --> DEFECT["🔴 Defect Analysis<br/>Defect rate per produk<br/>Defect cost dalam Rupiah<br/><i>→ Kuantifikasi kerugian</i>"]
    end

    PAGE1 --> PAGE2

    style PAGE1 fill:#e8eaf6,stroke:#283593
    style PAGE2 fill:#fce4ec,stroke:#c62828
```

> **Prinsip Dashboard:** Informasi disusun dari **umum ke spesifik** (*drill-down*). Halaman 1 menjawab *"Ada masalah apa?"*, Halaman 2 menjawab *"Di mana tepatnya dan seberapa parah?"*.

---

## 9. Pola Pikir Kritis: Yang Membedakan Analyst Biasa dan Analyst Hebat

### Diagram Perbandingan

```mermaid
flowchart TD
    subgraph BIASA["😐 Analyst Biasa"]
        direction TB
        AB1["Menerima data → langsung buat grafik"]
        AB2["Melaporkan fakta: <br/><i>'Defect rate Shift Malam 5.1%'</i>"]
        AB3["Menyarankan: <br/><i>'Perlu diperbaiki'</i>"]
        AB4["Menampilkan semua data<br/>tanpa kurasi"]
    end

    subgraph HEBAT["🌟 Analyst Hebat"]
        direction TB
        AH1["Memahami konteks bisnis dulu<br/>→ merumuskan pertanyaan<br/>→ baru membuka data"]
        AH2["Menginterpretasi: <br/><i>'Faktor kelelahan operator malam<br/>menyebabkan kerugian<br/>~Rp 58 juta/bulan'</i>"]
        AH3["Memberikan action plan spesifik:<br/><i>'Rotasi supervisor senior ke<br/>shift malam + fatigue management<br/>→ estimasi -20-30% defect'</i>"]
        AH4["Menyajikan 6 insight terkurasi<br/>dengan priority matrix<br/>dan timeline implementasi"]
    end

    style BIASA fill:#ffcdd2,stroke:#c62828
    style HEBAT fill:#c8e6c9,stroke:#2e7d32
```

### Lima kebiasaan berpikir kritis seorang analyst:

1. **"So What?" Test** — Setelah menemukan fakta, selalu tanyakan *"lalu kenapa ini penting?"* Jika tidak bisa menjawab, fakta itu belum jadi insight.

2. **Triangulasi** — Jangan percaya satu sumber saja. Insight tentang "mesin tua bermasalah" dikonfirmasi oleh tiga sumber: EDA (scatter plot), SQL (Query 4 & 15), dan domain knowledge (mesin > 5 tahun melewati masa optimal).

3. **Kuantifikasi Dampak** — *"Defect tinggi"* tidak bermakna bagi manajemen. *"Defect Control Board menyebabkan kerugian Rp 200 juta/semester"* bermakna.

4. **Berpikir Kontra-faktual** — *"Jika kita TIDAK melakukan maintenance, apa yang terjadi?"* → Tren penurunan output 8% per bulan akan berlanjut → kehilangan 15-20% target tahunan.

5. **Iterasi** — Temuan dari SQL Analysis (misalnya: Line A turun di Desember) bisa memicu pertanyaan baru yang kembali ke EDA (mengapa hanya Line A? apa yang berubah di Desember?).

---

## 10. Checklist Proses Berpikir

Gunakan checklist ini untuk memastikan proses analisis Anda lengkap:

### Fase Pemahaman
- [ ] Saya bisa menjelaskan masalah bisnis dalam 2 kalimat tanpa jargon teknis
- [ ] Saya tahu siapa stakeholder dan apa yang mereka butuhkan
- [ ] Saya sudah mendefinisikan KPI utama (Achievement Rate, Defect Rate, Downtime)

### Fase Pertanyaan
- [ ] Setiap pertanyaan bisa dijawab dengan data yang tersedia
- [ ] Pertanyaan mencakup semua dimensi relevan (waktu, lini, mesin, shift, produk)
- [ ] Tidak ada pertanyaan yang terlalu vague (*"kenapa semuanya jelek?"*)

### Fase Data Wrangling
- [ ] Saya bisa menjelaskan **mengapa** saya memilih metode cleaning tertentu (bukan hanya **bagaimana**)
- [ ] Tidak ada data yang hilang tanpa alasan yang jelas
- [ ] Business rules tervalidasi (defect ≤ output, downtime ≤ 480 menit)

### Fase Analisis
- [ ] Setiap visualisasi menjawab pertanyaan spesifik
- [ ] Temuan dikonfirmasi dari minimal 2 sumber/metode (triangulasi)
- [ ] Saya sudah mencari pola yang *tidak terduga* (seperti Monday Effect)

### Fase Insight & Rekomendasi
- [ ] Setiap insight memiliki: Fakta + Interpretasi + Dampak Bisnis
- [ ] Rekomendasi spesifik (bukan *"perlu diperbaiki"* tapi *"rotasi supervisor + fatigue management"*)
- [ ] Ada prioritas yang jelas (P1/P2/P3) dengan estimasi dampak
- [ ] Ada timeline implementasi yang realistis

### Fase Presentasi
- [ ] Dashboard memiliki alur dari umum ke spesifik (drill-down)
- [ ] Executive summary ringkas (6 temuan, bukan 15)
- [ ] Angka-angka penting dalam konteks bisnis (Rupiah, persentase kehilangan)

---

> **Pesan Penutup:** Portofolio ini bukan tentang seberapa canggih kode Python atau SQL Anda — tapi tentang seberapa jelas Anda bisa menjelaskan **proses berpikir** dari masalah bisnis ke solusi yang terukur. Seorang recruiter akan lebih terkesan dengan analyst yang bisa bercerita *"Saya menemukan bahwa kelelahan operator malam menyebabkan kerugian Rp 58 juta/bulan, dan saya merekomendasikan rotasi supervisor yang bisa menekan angka itu 20-30%"* dibanding yang hanya menunjukkan grafik tanpa konteks.
