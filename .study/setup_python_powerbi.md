# Solusi: Error "No module named matplotlib" di Power BI

Jika Power BI memunculkan error bahwa library `matplotlib` tidak ditemukan, hal ini disebabkan karena lingkungan (*environment*) Python yang dibaca oleh Power BI Desktop belum terpasang pustaka untuk visualisasi data tersebut.

Berikut adalah langkah cepat untuk mendeteksi dan memasang `matplotlib` pada lingkungan Python yang tepat.

---

## Langkah 1: Deteksi Lokasi Python yang Digunakan Power BI

Sebelum menjalankan perintah instalasi, Anda harus memastikan lingkungan Python mana yang sedang dibaca oleh Power BI:

1. Buka **Power BI Desktop**.
2. Pilih menu **File** > **Options and settings** > **Options**.
3. Di panel sebelah kiri, pilih menu **Python scripting**.
4. Perhatikan kolom **Detected Python home directories**:
   * Jika kolom tersebut mengarah ke folder **Anaconda** atau **Miniconda** (contoh: `C:\Users\Username\anaconda3\`), maka Power BI menggunakan environment Anaconda Anda.
   * Jika mengarah ke folder **Python standar** (contoh: `C:\Users\Username\AppData\Local\Programs\Python\Python310\`), maka Power BI menggunakan Python bawaan Windows.

---

## Langkah 2: Instalasi Matplotlib & Pandas

Buka terminal/CMD di komputer Anda (atau gunakan terminal VS Code) dan jalankan perintah instalasi sesuai dengan tipe Python yang terdeteksi di Langkah 1:

### Opsi A: Jika Terdeteksi Python Standar (Bawaan Windows)
Buka Command Prompt (CMD) atau PowerShell, lalu ketik perintah berikut dan tekan **Enter**:
```bash
pip install matplotlib pandas seaborn
```

### Opsi B: Jika Terdeteksi Lingkungan Anaconda / Miniconda
Buka aplikasi **Anaconda Prompt** dari menu start Windows Anda, kemudian jalankan perintah:
```bash
conda install matplotlib pandas seaborn -y
```
*Atau, jika Anda ingin menggunakan pip di dalam Anaconda:*
```bash
pip install matplotlib pandas seaborn
```

---

## Langkah 3: Muat Ulang Power BI
1. Setelah proses instalasi di terminal selesai dengan sukses, kembali ke **Power BI Desktop**.
2. Klik tombol **Run** (ikon segitiga/play) di kanan atas editor skrip Python visual Anda kembali.
3. Visualisasi kartu KPI kustom Anda sekarang akan ter-render dengan sempurna tanpa memunculkan error modul lagi.
