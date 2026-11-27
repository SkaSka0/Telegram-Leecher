# Dokumentasi Fork Lokal (Arch Linux)

Dokumentasi untuk menjalankan Telegram Leecher di PC Arch Linux (bukan Google Colab). Dokumen ini dipecah per fungsi supaya singkat dan fokus.

## Daftar berkas

| Berkas | Isi | Kapan dibaca |
|---|---|---|
| [001_PROGRESS.md](001_PROGRESS.md) | Status terkini, hasil uji, langkah berikutnya, log keputusan, riwayat commit | **Mulai dari sini** |
| [002_DEPENDENCIES.md](002_DEPENDENCIES.md) | Paket sistem Arch Linux yang harus terpasang (wajib dan opsional), plus cara memverifikasi | Sebelum instalasi |
| [003_SETUP.md](003_SETUP.md) | Memasang dan menjalankan bot dari nol | Instalasi baru |
| [004_USAGE.md](004_USAGE.md) | Cara memakai bot: perintah, nama file kustom, perilaku normal | Pemakaian sehari-hari |
| [005_TESTING.md](005_TESTING.md) | Prosedur uji fitur dengan file uji lokal | Menguji setelah perubahan |
| [006_TROUBLESHOOTING.md](006_TROUBLESHOOTING.md) | Gejala dan solusinya | Ada error |
| [007_ISSUES.md](007_ISSUES.md) | Pelacak tunggal bug, fitur, dan perbaikan yang belum dikerjakan (pengganti `BACKLOG.md`) | Memilih pekerjaan berikutnya |
| [008_VERSIONING.md](008_VERSIONING.md) | Aturan penomoran `MAJOR.MINOR.PATCH`, cara merilis, cara melihat versi | Sebelum merilis versi baru |
| [009_CHANGELOG.md](009_CHANGELOG.md) | Ringkasan fitur dan perbaikan per versi | Mengecek apa yang berubah |
| [010_PATCHES.md](010_PATCHES.md) | Semua perubahan kode dari versi Colab, lengkap dengan commit | Mengerjakan dari branch `main`, atau memahami kenapa kode berbeda |
| [011_GDRIVE.md](011_GDRIVE.md) | Token Google Drive (ditunda) | Kalau butuh download dari Drive |

### Rencana (`plans/`)

| Berkas | Isi | Kapan dibaca |
|---|---|---|
| [plans/001_batch-resilience.md](plans/001_batch-resilience.md) | Satu link gagal tidak menghentikan batch (BUG-001) | Sebelum mengerjakan fitur itu |
| [plans/002_refactor-roadmap.md](plans/002_refactor-roadmap.md) | Alasan dan urutan refactor setelah konversi lokal | Sebelum mulai refactor |

Daftar centang refactor ada di [../PROGRESS.md](../PROGRESS.md) (root repo).

## Konvensi

- **Shell:** fish. Tidak ada heredoc `<<'EOF'`. Aktifkan venv dengan `source .venv/bin/activate.fish`, atau panggil `.venv/bin/python` langsung.
- **Commit:** bahasa Inggris, gaya Conventional Commits (`fix(scope): ringkasan`), satu commit per langkah, `git add <file-spesifik>`.
- **Versi dan tag:** penomoran `MAJOR.MINOR.PATCH` ([008_VERSIONING.md](008_VERSIONING.md)), ditulis hanya di `colab_leecher/_version.py`. Setiap perubahan kode diakhiri `git tag -a vX.Y.Z` setelah commit dan dicatat di [009_CHANGELOG.md](009_CHANGELOG.md). Perubahan dokumentasi saja tidak diberi tag. Cek versi dengan `./run.sh --version` atau `/version` di Telegram.
- **Pelacak pekerjaan:** bug, fitur, dan perbaikan baru dicatat di [007_ISSUES.md](007_ISSUES.md) dengan prefiks ID (`BUG`, `FEAT`, `CHORE`, `SEC`, `TEST`). Rencana panjang disimpan di `plans/`.
- **Branch kerja:** `lokal`. Branch `main` tetap sebagai cadangan versi Colab.
- **Data lokal:** repo di `~/Projects/Telegram-Leecher`, data dan folder kerja di `~/.local/share/telegram-leecher/`, hasil `/lcupload` di `~/Downloads/Leecher`.

## Ruang lingkup

**Dipertahankan:** direct link (aria2), YouTube (yt-dlp), link pesan Telegram, download Google Drive (kode ada, token ditunda), Compress/Extract/UnDoubleZip, konversi dan split video, `/lcupload`, `/drupload`, pengaturan (thumbnail, prefix, suffix, caption), `/version`.

**Dibuang:** `/gdupload`, integrasi Mega, integrasi Terabox, launcher Colab (digantikan `run.sh`).

**Tidak dijamin:** magnet/torrent (lewat aria2, deteksi nama file tidak akurat).

## Lisensi

Proyek ini turunan dari [XronTrix10/Telegram-Leecher](https://github.com/XronTrix10/Telegram-Leecher) dan tetap berlisensi GPL-3.0.
