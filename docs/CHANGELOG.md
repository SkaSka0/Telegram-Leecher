# Changelog

Semua perubahan penting pada bot dicatat di sini. Aturan penomoran ada di [VERSIONING.md](VERSIONING.md) (`MAJOR.MINOR.PATCH`). Detail teknis tiap perubahan kode ada di [PATCHES.md](PATCHES.md).

## [Belum dirilis]

Rencana, belum dikerjakan (lihat [PLAN-BATCH-RESILIENCE.md](PLAN-BATCH-RESILIENCE.md)). Akan menjadi **0.2.0** bila selesai:

- Satu link gagal atau tidak valid tidak lagi membatalkan seluruh batch; link bermasalah dilewati dan dilaporkan di akhir.
- File parsial dari link yang gagal dibersihkan.
- Nama kustom hanya diterapkan bila hasil unduhan satu file.

## [0.1.0] - 2026-11-25

Versi pertama fork lokal (Arch Linux), diturunkan dari versi Colab. Patch kode 4.1 sampai 4.15; uji fitur 7.1 sampai 7.7 lolos.

### Ditambahkan

- `run.sh`: skrip untuk menjalankan bot dengan Python dari `.venv`.
- Filter owner pada semua handler pesan dan callback.
- Nama file otomatis untuk media Telegram tanpa `file_name` (foto, voice, video note, dan lainnya), misalnya `photo_<kode>.jpg`.
- Penolakan link Mega dan Terabox di awal dengan pesan yang jelas.
- Gambar hero cadangan bila unduhan `Hero.jpg` gagal.
- Dokumentasi lengkap di folder `docs/` (setup, patch, uji, pemakaian, troubleshooting, backlog, rencana).

### Diubah

- Semua path memakai lokasi lokal: data di `~/.local/share/telegram-leecher/`, hasil `/lcupload` di `~/Downloads/Leecher`.
- `credentials.json` dibaca relatif terhadap root repo; sesi Pyrogram disimpan di root repo.
- Semua mode berjalan lewat satu jalur `Do_Leech`.
- Zona waktu tanggal task menjadi Asia/Jakarta.
- `isLink` mengenali path absolut Linux apa pun yang ada di disk.
- Deteksi GPU memakai `nvidia-smi`; tanpa GPU, konversi video memakai CPU.
- `requirements.txt` disesuaikan untuk lingkungan lokal (Python 3.12, `moviepy<2`, `yt-dlp[default]`).

### Diperbaiki

- Task kini dibatalkan dengan pesan alasan yang jelas saat `aria2c` gagal, bukan melapor selesai dengan 0 file.
- `/drupload` mode Regular tidak lagi mengonversi atau menghapus file asli di folder pengguna.
- Opsi yt-dlp `concurrent_fragment_downloads` sekarang benar-benar berlaku.
- Import `GPUtil` yang rusak di Python 3.12 dihapus.

### Dihapus

- Perintah `/gdupload` (butuh Google Drive ter-mount di Colab).
- Integrasi Mega dan Terabox.
- Fungsi `Do_Mirror` dan `Do_Local_Mirror`.

### Keamanan

- Sebelumnya hanya `/settings` yang memeriksa owner, sehingga orang lain bisa memulai unduhan dan mengunggah file lokal lewat `/drupload`. Sekarang semua handler dibatasi ke `USER_ID`.

### Diketahui belum selesai

- Download Google Drive: kode ada, token belum dibuat (uji 7.5 ditunda).
- Uji 7.8 (`/lcupload`), 7.9 (`/drupload`), dan 7.10 (Cancel) belum dikerjakan.
- Satu link yang gagal masih membatalkan seluruh task.
