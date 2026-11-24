# Backlog

Perbaikan yang sudah teridentifikasi tetapi belum dikerjakan. Urutan prioritas ada di [PROGRESS.md](PROGRESS.md). Fitur besar punya dokumen rencana sendiri.

## Direncanakan (dokumen terpisah)

| Item | Dokumen |
|---|---|
| Satu link gagal atau tidak valid tidak menghentikan batch | [PLAN-BATCH-RESILIENCE.md](PLAN-BATCH-RESILIENCE.md) |

## Kebersihan repo

- Hapus `main.py` (launcher Colab, sudah digantikan `run.sh`): `git rm main.py`, commit `chore: remove the Colab launcher`.
- Ganti `google_auth.py` dengan `gdrive_token.py` saat Tahap Google Drive dikerjakan ([GDRIVE.md](GDRIVE.md)).
- Perbarui `README.md` utama ke cara pakai lokal (instalasi, `run.sh`, daftar fitur final) dan tautkan folder `docs/`.
- Hapus sisa teks Colab: label "Colab Usage" di status bot, tombol repo/channel asli, dan teks `/help` yang menyebut `/colabxr`.

## Perbaikan perilaku

- `media_Identifier` (`downlader/telegram.py`) mengembalikan `None` bila pesan tidak berisi media (misalnya link ke pesan teks), lalu pemanggil crash dengan `TypeError: cannot unpack`. Seharusnya gagal dengan pesan jelas. Bila `get_messages` gagal, `message` juga `None` dan memicu `AttributeError`. (Ditangani sebagai bagian dari rencana batch.)
- Pesan error Google Drive masih menyebut "Run the Google Drive Cell" (sisa Colab).
- Nama file hasil YouTube berupa ID video. Bisa diubah ke judul dengan mengganti template `%(id)s` di `downlader/ytdl.py`.
- `/setname`, `/zipaswd`, `/unzipaswd` di-reset oleh `handle_url`, sehingga hanya berlaku bila dikirim setelah link. Bisa diperbaiki agar pengaturan itu bertahan.
- `applyCustomName` mengganti nama semua file ke satu nama (saling menimpa bila ada banyak file). (Ditangani sebagai bagian dari rencana batch.)

## Keamanan dan ketahanan

- `converters.py` memakai `shell=True` dengan nama file dan password zip dari input pengguna. Karakter khusus (misalnya tanda kutip tunggal pada nama file) bisa merusak perintah `ffmpeg`, `unrar`, atau `7z`. Risikonya rendah karena bot hanya melayani owner, tetapi layak dirapikan dengan `subprocess` berbentuk daftar argumen.
- `/drupload` menerima path absolut apa pun yang ada di disk. Pertimbangkan daftar folder yang diizinkan.
- Pesan status memotong teks di batas 4096 karakter Telegram; banyak link pada satu pesan perlu diuji.

## Opsional

- Layanan systemd untuk menjalankan bot otomatis ([SETUP.md](SETUP.md)).
- Token Google Drive dan uji 7.5 ([GDRIVE.md](GDRIVE.md)).
