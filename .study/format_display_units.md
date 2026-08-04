# Studi Mandiri: Mengatasi Angka yang Disingkat "K" atau "M" di Power BI
Dokumen ini menjelaskan mengapa angka pada visualisasi Power BI disingkat menjadi huruf "K" (ribuan) atau "M" (jutaan), serta bagaimana menampilkan angka penuhnya secara detail.

---

## 1. Mengapa Muncul Huruf "K" atau "M"?

Ketika Anda menampilkan angka besar (seperti `125,000` atau `2,500,000`) pada komponen visual seperti **Card** (kartu KPI), grafik batang, atau chart lainnya, Power BI secara bawaan (*default*) akan menyingkat angka tersebut:
* **K (Kilo / Ribuan):** `150,000` diubah menjadi `150K`.
* **M (Million / Jutaan):** `2,500,000` diubah menjadi `2.5M`.

Penyingkatan ini diatur oleh fitur bernama **Display Units** yang diset ke "Auto" agar visualisasi tidak kepenuhan karakter dan tetap terlihat rapi pada layar kecil. Pengaturan format desimal `,` (koma) yang kita lakukan sebelumnya baru akan terlihat penuh saat data dibaca di dalam tabel/matriks, atau ketika fitur penyingkatan ini dinonaktifkan.

---

## 2. Cara Menampilkan Angka Penuh (Menghilangkan "K")

Jika Anda ingin menampilkan angka aslinya secara utuh (misal: `1,057,527` bukannya `1.06M` atau `1,057K`), Anda harus mengubah format display unit pada visual tersebut.

### Langkah-langkah pada Visual "Card" (Kartu KPI):
1. Klik visual **Card** yang menampilkan angka singkatan tersebut di kanvas laporan Anda.
2. Pada panel samping kanan, masuk ke tab **Format Visual** (ikon bergambar kuas lukis di sebelah panel data).
3. Cari dan perluas menu **Callout value**.
4. Cari opsi bernama **Display units** (biasanya diatur ke *Auto*).
5. Klik dropdown *Display units* tersebut dan ganti menjadi **None**.
6. Angka di dalam Card kini akan langsung berubah menampilkan nilai penuh lengkap dengan tanda koma pemisah ribuan (sesuai format yang Anda buat di DAX).

---

## 3. Best Practice dalam Desain Dashboard

Sebagai Data Analyst, kapan sebaiknya kita menggunakan penyingkatan "K" dan kapan harus menggunakan angka penuh?

* **Gunakan Angka Singkat (K / M):** Pada visualisasi grafik tren (line chart atau bar chart). Pembaca grafik hanya butuh melihat tren naik-turun dan estimasi nilai makro dengan cepat. Menampilkan angka penuh di atas grafik batang justru akan membuat visualisasi terlihat penuh sesak (*cluttered*).
* **Gunakan Angka Penuh (None):** Pada visualisasi **Card utama** di atas dashboard atau dalam bentuk **Table/Matrix**. Angka KPI utama dan data baris tabel sering kali membutuhkan akurasi data hingga satuan unit terkecil.
