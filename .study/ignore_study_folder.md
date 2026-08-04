# Studi Mandiri: Mengabaikan Folder ".study" di Git/GitHub

Folder `.study` berisi file catatan belajar pribadi Anda. Agar folder ini tidak ikut terunggah (push) ke repositori publik GitHub Anda, kita harus mendaftarkannya di dalam file konfigurasi `.gitignore`.

---

## 1. Menambahkan Folder ke `.gitignore`

File `.gitignore` adalah file khusus yang memberi tahu Git berkas atau direktori mana yang harus diabaikan.

### Cara Mengabaikannya:
Tambahkan baris berikut di baris paling bawah file `.gitignore` Anda:

```text
# Study/learning notes
.study/
```

---

## 2. Bagaimana jika Folder ".study" Sudah Terlanjur Terlacak (Tracked)?

Jika sebelumnya Anda sudah pernah melakukan `git commit` untuk file di dalam folder `.study`, hanya menambahkan namanya ke `.gitignore` **tidak akan langsung menghapusnya** dari pelacakan Git. 

Anda harus menghapus cache pelacakan Git secara manual menggunakan perintah terminal berikut tanpa menghapus file fisiknya:

```bash
# Menghapus cache pelacakan folder .study secara rekursif
git rm -r --cached .study/

# Lakukan commit untuk perubahan tersebut
git commit -m "Remove .study folder from git tracking"
```

Setelah itu, folder `.study` akan sepenuhnya diabaikan dan tidak akan muncul di GitHub saat Anda melakukan `git push` berikutnya.
