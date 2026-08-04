# Solusi: Menu "Display Units" Tidak Ditemukan di Power BI

Jika Anda tidak menemukan opsi **Display units** di menu formatting Power BI, hal tersebut terjadi karena perbedaan jenis visualisasi yang Anda gunakan di lembar kerja atau perbedaan versi Power BI Desktop Anda.

Berikut adalah panduan solusi berdasarkan visualisasi yang Anda pilih:

---

## Kasus 1: Anda Menggunakan Visual "Card (Klasik)" (Kartu Lama)
Jika Anda menggunakan visualisasi kartu versi lama (ikon berlogo angka `123` tunggal di panel visualisasi):

### Cara Mengatasinya:
1. Klik visual kartu tersebut.
2. Pergi ke panel **Format Visual** (ikon kuas lukis 🖌️).
3. Cari menu **Data label** (bukan *Callout value*). Perluas menu tersebut.
4. Di dalam menu *Data label*, Anda akan menemukan opsi **Display units**.
5. Ubah nilainya dari **Auto** menjadi **None**.

---

## Kasus 2: Anda Menggunakan Visual "Card (New)" (Kartu Baru)
Jika Anda menggunakan tipe visualisasi kartu multi-data terbaru (ikon berlogo angka `123` dengan garis bingkai di sekelilingnya):

### Cara Mengatasinya:
1. Klik visual kartu tersebut.
2. Pergi ke panel **Format Visual** (ikon kuas lukis 🖌️).
3. Cari dan perluas menu **Callout**.
4. Di bawah menu *Callout*, cari dan perluas sub-menu **Values**.
5. Di dalam sub-menu *Values*, Anda akan menemukan opsi **Display units**.
6. Ubah nilainya dari **Auto** menjadi **None**.

---

## Kasus 3: Anda Menggunakan Visual "Table" atau "Matrix"
Pada tabel atau matriks, Power BI secara *default* **tidak akan menyingkat angka** (tidak menampilkan huruf K) dan tidak memiliki menu *Display units*. 

Jika tabel Anda tetap menampilkan huruf "K", itu berarti format angka pada **rumus DAX (Measure)** Anda yang perlu diperbaiki:

### Cara Mengatasinya:
1. Klik nama Measure Anda (misal: `Total Output`) di panel data sebelah kanan.
2. Menu atas **Measure tools** akan aktif otomatis.
3. Lihat ke bagian **Formatting**:
   * Pastikan dropdown **Format** diatur ke **Whole number** atau **Decimal number**.
   * Klik tombol **`,` (Comma)** untuk memastikan pemisah ribuan aktif.
   * Pastikan kolom **Data type** adalah tipe numerik (*Decimal* atau *Whole number*), bukan *Text*.
