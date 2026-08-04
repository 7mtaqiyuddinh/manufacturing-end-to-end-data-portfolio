# Solusi: Slicer Tanggal Tidak Berubah Menjadi Date Slider

Jika setelah Anda menarik kolom `production_date` ke visual Slicer tampilannya tetap berupa daftar teks vertikal (bukan slider geser), hal ini disebabkan oleh salah satu dari dua alasan berikut:
1. **Power BI memecah tanggal menjadi hierarki** (Tahun, Kuartal, Bulan, Hari).
2. **Tipe data kolom `production_date` dibaca sebagai Teks (Text)**, bukan Tanggal (Date).

Berikut adalah solusi langkah-demi-langkah untuk memperbaikinya:

---

## Solusi 1: Matikan Fitur "Date Hierarchy" pada Slicer
Ini adalah penyebab paling umum. Power BI secara otomatis memilah tanggal menjadi struktur bertingkat, yang memaksa slicer berbentuk daftar centang.

### Cara Memperbaikinya:
1. Klik visual slicer yang bermasalah tersebut.
2. Di panel **Visualizations** sebelah kanan, lihat ke bagian kotak input **Field** (tempat Anda meletakkan kolom `production_date`).
3. Klik ikon **tanda panah kecil ke bawah** di sebelah kanan nama `production_date` pada kotak Field tersebut.
4. Anda akan melihat dua pilihan centang:
   * *Date Hierarchy* (saat ini tercentang).
   * **`production_date`** (nama kolom asli Anda).
5. Klik pada nama **`production_date`** untuk menggantinya dari hierarki ke data tanggal mentah.
6. Slicer Anda akan langsung berubah menjadi **Date Slider** (Between) seketika.

---

## Solusi 2: Ubah Tipe Data Kolom Menjadi "Date"
Jika setelah melakukan Solusi 1 Anda tidak melihat opsi tersebut, berarti Power BI membaca kolom tersebut sebagai teks biasa saat mengimpor file CSV.

### Cara Memperbaikinya:
1. Pada panel **Data** di paling kanan layar, klik pada nama kolom **`production_date`**.
2. Menu **Column tools** di bagian atas layar Power BI akan otomatis menyala.
3. Cari opsi **Data type** (yang mungkin saat ini bertuliskan *Text*).
4. Klik dropdown tersebut dan ubah menjadi **Date**.
5. Jika muncul jendela konfirmasi peringatan perubahan tipe data, klik **Yes/OK**.
6. Sekarang, ulangi langkah pembuatan slicer. Slicer akan mengenali data tersebut sebagai tanggal dan berubah menjadi slider.

---

## Solusi 3: Ubah Style Slicer secara Manual ke "Between"
Pada versi Power BI Desktop terbaru, Anda bisa memaksa visual slicer berubah format lewat pengaturan desain visual:

1. Klik visual slicer tersebut.
2. Masuk ke panel **Format Visual** (ikon kuas lukis 🖌️).
3. Buka menu **Slicer settings** > tab **Options**.
4. Di bagian dropdown **Style**, pilih opsi **Between** (Between adalah istilah teknis Power BI untuk Date Slider).
