Agar Anda benar-benar **menguasai, memahami, dan berhak mengakui** portofolio ini sebagai hasil karya Anda sendiri di hadapan recruiter, Anda harus memahami setiap bagian dari proses berpikir (*logical flow*) di balik pembuatannya. Portofolio yang bagus bukanlah tentang siapa yang mengetik kodenya, melainkan tentang bagaimana Anda **menjelaskan proses penyelesaian masalahnya**.

Berikut adalah langkah-langkah nyata yang harus Anda lakukan agar portofolio ini layak Anda akui sepenuhnya:

---

### Langkah 1: Pahami Alur Pemikiran Bisnis (The "Why")
Recruiter tidak hanya mencari orang yang bisa coding, tapi orang yang paham tujuan bisnis. Anda harus bisa menjelaskan:
1. **Masalah Utamanya:** PT Voltec Indonesia mengalami penurunan output produksi dan peningkatan defect di Semester 2 (H2) tahun 2024.
2. **Pertanyaan Bisnis yang Anda Ajukan:** Mengapa target tidak tercapai? Apakah karena downtime mesin? Mengapa defect meningkat? Apakah dipengaruhi oleh shift kerja?
3. **Penyebab Utama (Insight):** 
   * Mesin tua (>5 tahun) menyumbang 65% downtime.
   * Shift malam memiliki defect rate tertinggi (kelelahan/fatigue operator).
   * Produk *Control Board* menyumbang defect terbesar karena kompleksitasnya.

---

### Langkah 2: Bedah dan Jalankan Ulang Jupyter Notebook (The "How - Python")
Buka VS Code atau Jupyter Lab, lalu telusuri kedua notebook kita:
1. **[data_cleaning.ipynb](file:///q:/Data%20Science/Production/python/data_cleaning.ipynb)**:
   * **Pahami mengapa kita menggunakan Median Imputation:** Karena data tidak berdistribusi normal (terkena pencemaran outlier), sehingga median lebih stabil dibanding mean.
   * **Pahami IQR Clipping:** Mengapa kita tidak menghapus outlier? Karena di manufaktur, downtime panjang atau defect tinggi adalah informasi penting (bukan error input). Maka kita batasi (*clip*) nilainya ke batas atas IQR agar tidak merusak visualisasi boxplot tanpa kehilangan baris data.
2. **[eda.ipynb](file:///q:/Data%20Science/Production/python/eda.ipynb)**:
   * **Pelajari cara pembuatan grafik:** Perhatikan bagaimana visualisasi Pareto Chart dibuat untuk mendeteksi 80% defect disumbangkan oleh produk apa saja (Hukum Pareto).
   * **Analisis Korelasi:** Pahami bahwa nilai korelasi negatif menunjukkan bahwa semakin tinggi downtime, semakin rendah output yang dihasilkan.

---

### Langkah 3: Kuasai Logika Query SQL (The "How - SQL")
Buka file **[analysis.sql](file:///q:/Data%20Science/Production/sql/analysis.sql)**. Pilih 3-4 query kompleks yang paling sering ditanyakan saat technical interview dan pahami cara kerjanya:
* **Common Table Expression (CTE) & Window Function (`RANK`):** Lihat *Query 12*. Pahami bagaimana kita mengelompokkan kombinasi Line-Shift terlebih dahulu menggunakan CTE, lalu merangkingnya berdasarkan total output.
* **Month-on-Month (MoM) Growth dengan `LAG`:** Lihat *Query 10*. Pahami bagaimana fungsi `LAG()` mengambil data output dari bulan sebelumnya untuk menghitung persentase kenaikan atau penurunan performa bulanan.

---

### Langkah 4: Bangun Sendiri Dashboard Power BI (The "Presentation")
Jangan biarkan dashboard ini hanya berupa konsep. Ikuti **[powerbi_guide.md](file:///q:/Data%20Science/Production/powerbi/powerbi_guide.md)** secara manual:
1. Impor data `.csv` dari folder `data/cleaned/`.
2. Buat relasi tabel di Model View (pastikan Anda bisa menjelaskan apa itu *Star Schema* dan *Fact-Dimension tables*).
3. Ketik sendiri rumus DAX (seperti `Achievement Rate` dan `Defect Rate`).
4. Desain visualisasinya sesuai panduan. Proses membangun visualisasi ini akan memberikan Anda *muscle memory* dan pengalaman hands-on yang nyata.

---

### Langkah 5: Latihan Menjelaskan Portofolio (The "Storytelling")
Cobalah rekam diri Anda sendiri atau jelaskan kepada cermin menggunakan teknik **STAR (Situation, Task, Action, Result)**:
* **S (Situation):** PT Voltec Indonesia mengalami masalah penurunan produktivitas dan kualitas pada H2 2024.
* **T (Task):** Saya ditugaskan menganalisis data produksi harian sebanyak ~25 ribu baris untuk mencari akar penyebab masalah (bottleneck).
* **A (Action):** Saya membersihkan data menggunakan Python (handling missing values & IQR clipping), melakukan EDA, merancang database relasional di SQL, serta menganalisis performa mesin dan shift kerja menggunakan CTE dan Window Functions. Terakhir, saya memvisualisasikannya ke dalam Power BI dashboard.
* **R (Result):** Saya menemukan bahwa mesin tua (>5 tahun) dan shift malam menjadi bottleneck utama. Saya merekomendasikan program *Preventive Maintenance* terjadwal dan optimalisasi *Quality Control* di shift malam yang berpotensi memulihkan output sebesar 8-12%.