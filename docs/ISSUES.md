# Issues

Pelacak tunggal untuk **bug**, **fitur**, dan **perbaikan** yang sudah teridentifikasi tetapi belum dikerjakan. Gantinya `BACKLOG.md`. Urutan kerja secara umum ada di [PROGRESS.md](PROGRESS.md); rencana panjang disimpan di folder [plans/](plans/) dan ditautkan dari entri terkait.

## Cara memakai

**Prefiks ID** (nomor naik terus per prefiks, jangan dipakai ulang):

| Prefiks | Arti |
|---|---|
| `BUG` | Perilaku yang salah |
| `FEAT` | Fitur atau peningkatan baru |
| `CHORE` | Kebersihan repo, dokumentasi, tanpa perubahan perilaku |
| `SEC` | Keamanan dan ketahanan |
| `TEST` | Uji yang tertunda ([TESTING.md](TESTING.md)) |

**Status:** `ide` → `perlu-uji` (belum pasti ada) → `direncanakan` (sudah jelas, belum jalan) → `dikerjakan` → `selesai`.

**Prioritas:** `tinggi`, `sedang`, `rendah`.

**Template entri baru** (salin ke bagian "Terbuka"):

```markdown
### TIPE-NNN · Judul singkat
- Status: ide
- Prioritas: sedang
- Area: berkas atau modul terkait
- Detail: satu sampai tiga kalimat (gejala atau tujuan)
- Rencana: [plans/nama.md](plans/nama.md)   <!-- hanya bila ada -->
```

**Saat selesai:** pindahkan entri ke bagian "Selesai", ubah status menjadi `selesai`, dan tambahkan hash commit penyelesaiannya (`git log --oneline`).

---

## Terbuka

### TEST-001 · Uji `/lcupload` (7.8)
- Status: direncanakan
- Prioritas: tinggi
- Detail: prasyarat untuk mengerjakan BUG-001. Prosedur di [TESTING.md](TESTING.md#78-lcupload--berikutnya).

### TEST-002 · Uji `/drupload` (7.9)
- Status: direncanakan
- Prioritas: tinggi
- Detail: membuktikan patch 4.5 dan 4.7. Prosedur di [TESTING.md](TESTING.md#79-drupload--berikutnya).

### TEST-003 · Uji tombol Cancel (7.10)
- Status: direncanakan
- Prioritas: tinggi
- Detail: harus diulang setelah BUG-001 selesai karena `cancelTask` dipakai di banyak jalur. Prosedur di [TESTING.md](TESTING.md#710-tombol-cancel-).

### BUG-001 · Satu link gagal atau tidak valid membatalkan seluruh batch
- Status: direncanakan
- Prioritas: tinggi
- Area: `downlader/manager.py`, `aria2.py`, `gdrive.py`, `telegram.py`, `ytdl.py`, `utility/handler.py`, `__main__.py`
- Detail: satu link bermasalah membatalkan seluruh task dan menghapus file link yang sudah selesai. Target: link bermasalah dilewati, ada ringkasan di akhir, task dibatalkan hanya bila semua link gagal.
- Rencana: [plans/batch-resilience.md](plans/batch-resilience.md)
- Prasyarat: TEST-001, TEST-002, TEST-003 selesai dan `git status --short` bersih.

### BUG-002 · `media_Identifier` mengembalikan `None` untuk pesan tanpa media
- Status: direncanakan (ditangani BUG-001, langkah 3)
- Prioritas: tinggi
- Area: `downlader/telegram.py`
- Detail: link ke pesan teks membuat pemanggil crash dengan `TypeError: cannot unpack`. Bila `get_messages` gagal, `message` juga `None` dan memicu `AttributeError`. Seharusnya gagal dengan pesan jelas.
- Rencana: [plans/batch-resilience.md](plans/batch-resilience.md)

### BUG-003 · `applyCustomName` menimpa file bila hasil unduhan lebih dari satu
- Status: direncanakan (ditangani BUG-001, langkah 10)
- Prioritas: sedang
- Area: `utility/helper.py`
- Detail: semua file diganti ke satu nama. Target: nama kustom hanya diterapkan bila hasilnya tepat satu file, selain itu dilewati dengan peringatan di laporan akhir. Aturan pemakaian saat ini ada di [USAGE.md](USAGE.md#nama-file-kustom-dan-password).
- Rencana: [plans/batch-resilience.md](plans/batch-resilience.md)

### BUG-004 · Pesan error Google Drive masih menyebut "Run the Google Drive Cell"
- Status: ide
- Prioritas: rendah
- Area: `downlader/gdrive.py` (`build_service`)
- Detail: sisa teks Colab. Ganti dengan petunjuk lokal (jalankan `gdrive_token.py`, lihat [GDRIVE.md](GDRIVE.md)). Sebaiknya dikerjakan bersamaan dengan FEAT-004.

### BUG-005 · Pesan status dengan banyak link belum diuji
- Status: perlu-uji
- Prioritas: rendah
- Area: `utility/task_manager.py` (`dump_task`, `src_text`), `utility/handler.py` (`SendLogs`)
- Detail: teks dipotong di batas 4096 karakter Telegram. Uji dengan batch yang jumlah linknya cukup banyak untuk melewati batas itu.

### FEAT-001 · Nama file YouTube berupa judul, bukan ID video
- Status: ide
- Prioritas: rendah
- Area: `downlader/ytdl.py`
- Detail: saat ini template nama memakai `%(id)s`. Bisa diganti ke `%(title)s`, tetapi perlu diperhatikan nama yang terlalu panjang atau berisi karakter khusus. Perilaku sekarang tercatat di [USAGE.md](USAGE.md#sumber-yang-didukung).

### FEAT-002 · `/setname`, `/zipaswd`, `/unzipaswd` bertahan antar link
- Status: ide
- Prioritas: rendah
- Area: `__main__.py` (`handle_url`)
- Detail: `handle_url` mengosongkan ketiganya setiap kali link dikirim, sehingga perintah itu hanya berlaku bila dikirim setelah link. Perbaikan: biarkan pengaturan bertahan dan reset hanya setelah task selesai. Catatan pemakaian di [USAGE.md](USAGE.md#catatan-setname-zipaswd-unzipaswd).

### FEAT-003 · Layanan systemd untuk menjalankan bot otomatis
- Status: ide
- Prioritas: rendah
- Detail: langkah sudah ditulis di [SETUP.md](SETUP.md#langkah-5-service-systemd-opsional), tinggal dipasang dan diuji.

### FEAT-004 · Token Google Drive dan uji 7.5
- Status: ide
- Prioritas: rendah
- Area: `google_auth.py` → `gdrive_token.py`, `downlader/gdrive.py`
- Detail: ditunda karena jarang dipakai dan butuh intervensi manual di browser. Langkah di [GDRIVE.md](GDRIVE.md); uji 7.5 di [TESTING.md](TESTING.md#75-google-drive-).

### SEC-001 · `converters.py` memakai `shell=True` dengan input pengguna
- Status: ide
- Prioritas: sedang
- Area: `utility/converters.py` (`ffmpeg`, `unrar`, `7z`, `zip`, `tar`)
- Detail: nama file dan password zip dimasukkan ke string perintah. Karakter khusus (misalnya tanda kutip tunggal pada nama file) bisa merusak perintah. Risiko rendah karena bot hanya melayani owner, tetapi layak dirapikan dengan `subprocess` berbentuk daftar argumen.

### SEC-002 · `/drupload` menerima path absolut apa pun
- Status: ide
- Prioritas: rendah
- Area: `utility/helper.py` (`isLink`), `utility/task_manager.py`
- Detail: patch 4.5 sengaja membuka semua path yang ada di disk. Pertimbangkan daftar folder yang diizinkan.

### CHORE-001 · Hapus `main.py` (launcher Colab)
- Status: direncanakan
- Prioritas: rendah
- Detail: sudah digantikan `run.sh`. Perintah: `git rm main.py`, commit `chore: remove the Colab launcher`. Perhatikan: `README.md` masih menyebut `main.py`, jadi kerjakan bersama CHORE-003.

### CHORE-002 · Ganti `google_auth.py` dengan `gdrive_token.py`
- Status: ide
- Prioritas: rendah
- Detail: dikerjakan bersama FEAT-004. Langkah di [GDRIVE.md](GDRIVE.md).

### CHORE-003 · Perbarui `README.md` utama ke cara pakai lokal
- Status: ide
- Prioritas: sedang
- Detail: tulis instalasi, `run.sh`, dan daftar fitur final; tautkan folder `docs/` ([docs/README.md](README.md)). Hapus bagian Colab (tombol notebook, peringatan kebijakan Colab) dan daftar struktur kode yang masih menyebut `main.py`.

### CHORE-004 · Hapus sisa teks Colab di bot
- Status: ide
- Prioritas: rendah
- Area: `utility/helper.py` (`sysINFO`), `utility/handler.py` (`SendLogs`, `cancelTask`), `__main__.py` (`/start`, `/help`)
- Detail: label "Colab Usage" di status bot, tombol repo/channel asli, dan teks `/help` yang menyebut `/colabxr`.


### FEAT-007 · Pindahkan konfigurasi dari `credentials.json` ke `.env`
- Status: direncanakan
- Prioritas: sedang
- Area: `colab_leecher/__init__.py`, `requirements.txt`, `.gitignore`, `.env.example` (baru), `docs/SETUP.md`, `docs/DEPENDENCIES.md`
- Detail: konfigurasi dibaca dari environment (`API_ID`, `API_HASH`, `BOT_TOKEN`, `USER_ID`, `DUMP_ID`) lewat `python-dotenv`. Loader mengubah `API_ID`, `USER_ID`, `DUMP_ID` menjadi `int`, memvalidasi awalan `-100` pada `DUMP_ID`, dan gagal dengan pesan jelas bila ada nilai kosong. `credentials.json` tetap diterima sebagai cadangan selama satu rilis lalu dihapus. Manfaat: TEST-004 tidak butuh `credentials.json` palsu, dan layanan systemd (FEAT-003) bisa memakai `EnvironmentFile=`. Bukan perbaikan keamanan, karena kedua format sama-sama berkas teks yang di-gitignore.
- Catatan: `.env` ditambahkan ke `.gitignore`, `.env.example` berisi placeholder dan di-commit. `my_bot.session` tetap rahasia dan sudah di-gitignore. `_version.py` tidak boleh mengimpor apa pun dari paket, supaya `./run.sh --version` tetap jalan tanpa konfigurasi.
- Prasyarat: TEST-001, TEST-002, TEST-003 selesai. Rilis tersendiri (MINOR), jangan digabung dengan batch resilience (0.2.0).
---

## Selesai

_(belum ada. Format: `ID · judul · hash commit`)_
