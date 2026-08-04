# Solusi Alternatif: Memaksa Angka Penuh via Custom Format DAX (Tanpa Menu "Display Units")

Jika opsi **Display units** benar-benar tidak muncul di bagian formatting visual Anda, kemungkinan besar Power BI mendeteksi tipe data Measure tersebut sebagai **Teks (Text)** atau **General format**, sehingga Power BI menyembunyikan opsi penyusutan angka tersebut dari menu visual Anda.

Anda tidak perlu mencari menu tersebut di visual. Kita bisa memaksanya menampilkan angka penuh secara absolut langsung dari pengaturan format rumus DAX itu sendiri.

---

## Cara Memaksa Angka Penuh Lewat Custom Format String

Langkah ini akan memaksa Power BI menampilkan angka penuh (lengkap dengan pemisah ribuan) di visualisasi mana pun secara otomatis:

1. Pada panel data di sebelah kanan, **klik nama Measure** yang ingin diubah (misalnya `Total Output`).
2. Di menu bagian atas Power BI Desktop, klik tab **Measure tools**.
3. Lihat bagian **Formatting**:
   * Pada dropdown **Format**, klik dan scroll ke paling bawah, lalu pilih **Custom**.
4. Setelah memilih *Custom*, akan muncul kolom baru di bawahnya bernama **Format string**.
5. Hapus isi kolom tersebut dan ketik kode format berikut:
   * **`#,##0`** (untuk angka bulat tanpa desimal, contoh: `1,250,000`)
   * **`#,##0.0`** (jika butuh 1 desimal di belakang koma)
6. Tekan **Enter**.

Visualisasi kartu Anda sekarang akan langsung terpaksa menampilkan angka penuh tanpa disingkat menjadi "K" atau "M".

---

## Mengapa Pengaturan Format DAX Lebih Kuat?

Mengatur format melalui *Custom Format String* di DAX adalah metode paling aman karena:
1. **Berlaku Global:** Format ini akan melekat pada Measure tersebut di visual mana pun Anda meletakkannya (baik tabel, kartu, grafik, maupun tooltip).
2. **Mengatasi Bug UI:** Terkadang Power BI menyembunyikan menu *Display units* karena masalah deteksi tipe data otomatis pada file CSV. Dengan format kustom, kita memaksa tipe data tersebut dibaca sebagai numerik terformat secara kaku.
