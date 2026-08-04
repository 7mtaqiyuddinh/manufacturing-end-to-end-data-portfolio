# Studi Mandiri: Penjelasan Relasi Pemodelan Data di Power BI
Dokumen ini mengklarifikasi simbol relasi data modeling dalam panduan implementasi Power BI dan menjelaskan pentingnya hubungan relasi ini.

---

## 1. Klarifikasi Simbol Relasi (`$\dots$` vs `$\rightarrow$`)

### Pertanyaan
*Kenapa pada baris 29 tertulis `$\dots$` sedangkan baris di atasnya menggunakan `$\rightarrow$`? Apakah ada makna khusus?*

### Jawaban
**Tidak ada makna khusus.** Penulisan `$\dots$` tersebut murni merupakan **kesalahan ketik (typo)** saat penulisan dokumen markdown. Simbol yang benar dan seharusnya digunakan di sana adalah `$\rightarrow$` (simbol panah kanan). 

Hubungan relasi yang benar untuk seluruh dimensi ke tabel fakta adalah sama:

* `line_dim_cleaned(line_id)` $\rightarrow$ `production_fact_cleaned(line_id)`
* `machine_dim_cleaned(machine_id)` $\rightarrow$ `production_fact_cleaned(machine_id)`
* `product_dim_cleaned(product_id)` $\rightarrow$ `production_fact_cleaned(product_id)`
* `shift_dim_cleaned(shift_id)` $\rightarrow$ `production_fact_cleaned(shift_id)`

---

## 2. Esensi Arah Panah (`$\rightarrow$`) dalam Pemodelan Power BI

Dalam pemodelan data di Power BI (*Model View*), simbol panah `$\rightarrow$` memiliki arti yang sangat penting terkait **arah filter data (Cross-Filter Direction)**:

1. **Arah Hubungan (One-to-Many / $1:*$):**
   * Sisi `1` berada pada tabel dimensi (karena kode ID seperti `shift_id` bersifat unik di tabel dimensi).
   * Sisi `*` (Many) berada pada tabel fakta `production_fact` (karena satu shift yang sama dijalankan berulang kali pada tanggal yang berbeda-beda).

2. **Arah Filter (Single Direction):**
   * Panah menunjuk dari tabel dimensi ke tabel fakta (`Dimensi` $\rightarrow$ `Fakta`).
   * Ini berarti, jika Anda memfilter atau memilih nama shift tertentu (misal: "Shift Malam") pada filter/slicer di dashboard, filter tersebut akan otomatis mengalir ke bawah untuk menyaring baris data di tabel fakta.
   * Sebaliknya, filter di tabel fakta secara *default* tidak akan menyaring baris di tabel dimensi.
