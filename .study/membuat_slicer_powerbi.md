# Studi Mandiri: Panduan Membuat Slicer (Filter Panel) di Power BI

**Slicer** adalah komponen visual interaktif di Power BI yang digunakan untuk menyaring (filter) seluruh visualisasi data yang ada pada halaman laporan secara instan.

Berikut adalah langkah-langkah nyata untuk membuat slicer berdasarkan `production_date` (Slider), serta `shift_name` dan `line_name` (Tombol Pilihan).

---

## 1. Membuat Slicer Rentang Tanggal (`production_date`)
Tipe slicer ini akan berbentuk slider rentang waktu yang bisa digeser oleh pengguna.

### Langkah-langkah:
1. Pada panel **Visualizations** (sebelah kanan), cari dan klik ikon **Slicer** (ikon bergambar corong filter kecil di dalam persegi). Sebuah kotak kosong akan muncul di kanvas Anda.
2. Pada panel **Data** (paling kanan), buka tabel `production_fact_cleaned`.
3. Tarik kolom **`production_date`** dan letakkan ke dalam kolom **Field** di panel visualisasi Anda.
4. Visual secara otomatis akan berubah menjadi **Date Slider** (garis rentang waktu dengan dua tombol geser bulat).
5. **Pengaturan Desain (Opsional):** Jika Anda ingin mengubah tipenya menjadi dropdown atau input teks, klik ikon tanda panah kecil ke bawah di sudut kanan atas visual slicer tersebut saat kursor diarahkan ke atasnya, lalu pilih opsi seperti *Between* (Slider bawaan), *Before*, *After*, atau *List*.

---

## 2. Membuat Slicer Pilihan Kategori (`shift_name` dan `line_name`)
Kita akan membuat slicer kategori yang berbentuk daftar pilihan (list), menu tarik-turun (dropdown), atau berbentuk tombol-tombol modern (*Tiles*).

### Langkah-langkah untuk `shift_name`:
1. Klik area kosong di kanvas Anda (agar tidak menimpa visual sebelumnya).
2. Klik ikon **Slicer** di panel *Visualizations*.
3. Pada panel **Data**, buka tabel dimensi `shift_dim_cleaned` (atau cari di tabel fakta jika tidak menggunakan relasi).
4. Tarik kolom **`shift_name`** ke dalam kotak **Field** slicer.
5. Secara *default*, ini akan tampil berupa daftar vertikal dengan kotak centang (*checkboxes*).

### Mengubah Tampilan Menjadi Tombol Pilihan (Tiles) yang Modern:
Tombol *Tile* sangat cocok untuk pilihan kategori pendek seperti nama shift (Pagi, Siang, Malam).
1. Klik visual slicer `shift_name` yang baru dibuat.
2. Masuk ke panel **Format Visual** (ikon kuas lukis 🖌️).
3. Cari dan perluas menu **Slicer settings** > tab **Options**.
4. Di bagian dropdown **Style**, ubah dari *Vertical list* menjadi **Tile**.
5. Slicer akan langsung berubah dari daftar centang menjadi tombol-tombol kotak horizontal yang interaktif dan mudah diklik.

*(Lakukan hal yang sama untuk membuat slicer `line_name` menggunakan kolom dari tabel `line_dim_cleaned`)*.

---

## 3. Best Practice Menata Panel Filter (Slicer)
* **Letakkan di Atas atau di Sisi Kiri:** Slicer adalah hal pertama yang dicari pengguna saat membaca laporan. Letakkan di posisi strategis.
* **Gunakan Judul yang Jelas:** Pastikan label judul slicer mudah dipahami (misal: "Pilih Tanggal Produksi" atau "Pilih Shift").
* **Atur Interaksi (Edit Interactions):** Secara bawaan, slicer akan memfilter semua visual di halaman tersebut. Jika ada visual tertentu yang tidak ingin Anda ikut terfilter (misalnya tabel target statis), Anda bisa mematikannya lewat menu **Format** (atas) > **Edit Interactions** > klik ikon larangan/lingkaran coret pada visual yang ingin dibebaskan dari filter.
