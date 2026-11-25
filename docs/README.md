# Dokumentasi Fork Lokal (Arch Linux)

Dokumentasi untuk menjalankan Telegram Leecher di PC Arch Linux (bukan Google Colab). Dokumen ini dipecah per fungsi supaya singkat dan fokus.

## Daftar berkas

| Berkas | Isi | Kapan dibaca |
|---|---|---|
| [PROGRESS.md](PROGRESS.md) | Status terkini, hasil uji, langkah berikutnya, log keputusan, riwayat commit | **Mulai dari sini** |
| [DEPENDENCIES.md](DEPENDENCIES.md) | Paket sistem Arch Linux yang harus terpasang (wajib dan opsional), plus cara memverifikasi | Sebelum instalasi |
| [SETUP.md](SETUP.md) | Memasang dan menjalankan bot dari nol | Instalasi baru |
| [PATCHES.md](PATCHES.md) | Semua perubahan kode dari versi Colab, lengkap dengan commit | Mengerjakan dari branch `main`, atau memahami kenapa kode berbeda |
| [TESTING.md](TESTING.md) | Prosedur uji fitur dengan file uji lokal | Menguji setelah perubahan |
| [USAGE.md](USAGE.md) | Cara memakai bot: perintah, nama file kustom, perilaku normal | Pemakaian sehari-hari |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Gejala dan solusinya | Ada error |
| [GDRIVE.md](GDRIVE.md) | Token Google Drive (ditunda) | Kalau butuh download dari Drive |
| [VERSIONING.md](VERSIONING.md) | Aturan penomoran `MAJOR.MINOR.PATCH`, cara merilis, cara melihat versi | Sebelum merilis versi baru |
| [CHANGELOG.md](CHANGELOG.md) | Ringkasan fitur dan perbaikan per versi | Mengecek apa yang berubah |
| [PLAN-BATCH-RESILIENCE.md](PLAN-BATCH-RESILIENCE.md) | Rencana: satu link gagal tidak menghentikan batch | Sebelum mengerjakan fitur itu |
| [BACKLOG.md](BACKLOG.md) | Perbaikan lain yang belum dikerjakan | Memilih pekerjaan berikutnya |

## Konvensi

- **Shell:** fish. Tidak ada heredoc `<<'EOF'`. Aktifkan venv dengan `source .venv/bin/activate.fish`, atau panggil `.venv/bin/python` langsung.
- **Commit:** bahasa Inggris, gaya Conventional Commits (`fix(scope): ringkasan`), satu commit per langkah, `git add <file-spesifik>`.
- **Versi dan tag:** penomoran `MAJOR.MINOR.PATCH` ([VERSIONING.md](VERSIONING.md)), ditulis hanya di `colab_leecher/_version.py`. Setiap perubahan kode diakhiri `git tag -a vX.Y.Z` setelah commit dan dicatat di [CHANGELOG.md](CHANGELOG.md). Perubahan dokumentasi saja tidak diberi tag. Cek versi dengan `./run.sh --version` atau `/version` di Telegram.
- **Branch kerja:** `lokal`. Branch `main` tetap sebagai cadangan versi Colab.
- **Data lokal:** repo di `~/Projects/Telegram-Leecher`, data dan folder kerja di `~/.local/share/telegram-leecher/`, hasil `/lcupload` di `~/Downloads/Leecher`.

## Ruang lingkup

**Dipertahankan:** direct link (aria2), YouTube (yt-dlp), link pesan Telegram, download Google Drive (kode ada, token ditunda), Compress/Extract/UnDoubleZip, konversi dan split video, `/lcupload`, `/drupload`, pengaturan (thumbnail, prefix, suffix, caption), `/version`.

**Dibuang:** `/gdupload`, integrasi Mega, integrasi Terabox, launcher Colab (digantikan `run.sh`).

**Tidak dijamin:** magnet/torrent (lewat aria2, deteksi nama file tidak akurat).

## Lisensi

Proyek ini turunan dari [XronTrix10/Telegram-Leecher](https://github.com/XronTrix10/Telegram-Leecher) dan tetap berlisensi GPL-3.0.
