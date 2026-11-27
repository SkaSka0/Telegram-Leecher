# Progress Refactor

Daftar centang untuk pekerjaan **refactor** setelah konversi Colab ke lokal. Alasan dan urutan ada di [docs/plans/002_refactor-roadmap.md](docs/plans/002_refactor-roadmap.md). Pelacak per item ada di [docs/007_ISSUES.md](docs/007_ISSUES.md). Status konversi lokal dan hasil uji fitur ada di [docs/001_PROGRESS.md](docs/001_PROGRESS.md).

> Centang item hanya setelah perbaikannya ter-commit di kode, bukan saat baru dibahas atau direncanakan.

---

## Prasyarat (kerjakan lebih dulu)

- [ ] Uji 7.8 `/lcupload`, 7.9 `/drupload`, 7.10 tombol Cancel lolos
      ([docs/005_TESTING.md](docs/005_TESTING.md))
- [ ] [Batch resilience](docs/plans/001_batch-resilience.md) selesai (BUG-001).
      Ini juga menutup item lama "ganti `except Exception: pass` / bare
      `logging.error` dengan propagasi atau notifikasi ke pengguna"
- [ ] `git status --short` bersih

---

## Patch yang sudah di kode, menunggu verifikasi

Belum boleh dianggap selesai sebelum diuji.

- [ ] `gDownloadFile` menghapus file lama sebelum menulis (`gdrive.py`)
      **[DIPATCH, BELUM DIUJI]**. Diuji lewat 7.5 (Drive ditunda): retry dengan
      nama sama, bandingkan ukuran/checksum dengan sumber
- [ ] `cancelTask()` memanggil `BOT.TASK.cancel()` paling akhir (`handler.py`)
      **[DIPATCH, BELUM DIUJI]**. Diuji lewat 7.10
- [ ] Penjagaan `BOT.State.task_going` di `Leech()` untuk race saat Cancel
      **[DIPATCH, BELUM DIUJI]**. Diuji lewat 7.10; tidak boleh ada
      `FileNotFoundError` di `os.stat`
- [ ] Refresh otomatis `token.pickle` (`gdrive.py` → `build_service`)
      **[DIPATCH; SKENARIO VALID DAN KEDALUWARSA PERNAH LOLOS]**. Skenario token
      dicabut, format lama, dan berkas hilang menunggu 7.5 dan 7.10

---

## A. Keamanan dan kebenaran

- [ ] SEC-003: `get_Aria2c_Name` memakai `shell=True` dengan link pengguna
      (`downlader/aria2.py`); ganti ke daftar argumen
- [ ] BUG-006: saring shortcut Google Docs/Sheets di `gDownloadFolder`
      (`downlader/gdrive.py`), dikerjakan bersama FEAT-004 (token Drive)

---

## B. Struktur

- [ ] CHORE-005: pecah `Leech()` (`handler.py`)
- [ ] CHORE-005: pecah `taskScheduler()` (`task_manager.py`)
- [ ] CHORE-005: sederhanakan `YouTubeDL()` (`ytdl.py`)
- [ ] FEAT-005: ganti dua kali `aria2c` di `get_Aria2c_Name` dengan satu
      permintaan `HEAD` (dengan fallback nama dari URL)
- [ ] Keputusan: dukungan multi-task. Default tidak dikerjakan

---

## C. Keandalan dan observabilitas

- [ ] CHORE-006: ganti sisa `print()` dengan `logging`
      (`manager.py`, `task_manager.py`, `helper.py`)
- [ ] TEST-004: uji unit fungsi murni (`sizeUnit`, `getTime`, `speedETA`,
      `fileType`, `shortFileName`, `getIDFromURL`, `media_Name`); butuh fixture
      `credentials.json` palsu
- [ ] FEAT-006: retry untuk downloader Drive dan Telegram, setelah batch
      resilience

---

## Ad-hoc

- [ ] Rancang format caption tetap untuk upload video (data dari JSON eksternal,
      bukan dari berkas video). Belum ada entri di 007_ISSUES.md; tambahkan sebagai
      FEAT baru bila dikerjakan
