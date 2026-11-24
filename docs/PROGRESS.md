# Progress

Terakhir diperbarui: 24 November 2026
Branch kerja: `lokal`

## Status

| Area | Status |
|---|---|
| Setup (kredensial, paket, venv, dependency) | ✅ Selesai |
| Patch kode 4.1 sampai 4.15 | ✅ Selesai ([PATCHES.md](PATCHES.md)) |
| Bot berjalan lokal, filter owner terbukti menolak akun lain | ✅ Selesai |
| Token Google Drive | ⏸ Ditunda ([GDRIVE.md](GDRIVE.md)) |
| Layanan systemd | ⬜ Opsional |

## Hasil uji fitur

| Uji | Isi | Hasil |
|---|---|---|
| 7.1 | Direct link, termasuk kegagalan yang dibatalkan dengan pesan jelas | ✅ Lolos |
| 7.2 | Compress, Extract, UnDoubleZip | ✅ Lolos |
| 7.3 | YouTube (`/ytupload` dan `/tupload`) | ✅ Lolos |
| 7.4 | Link pesan Telegram (termasuk nama untuk foto) | ✅ Lolos |
| 7.5 | Google Drive | ⏸ Ditunda |
| 7.6 | Konversi video (Convert dan Don't Convert) | ✅ Lolos |
| 7.7 | Split video dan split file biasa | ✅ Lolos |
| 7.8 | `/lcupload` | ⬜ Berikutnya |
| 7.9 | `/drupload` | ⬜ Berikutnya |
| 7.10 | Tombol Cancel | ⬜ Belum |

Prosedur lengkap tiap uji ada di [TESTING.md](TESTING.md).

## Langkah berikutnya (berurutan)

1. Selesaikan uji **7.8**, **7.9**, **7.10**.
2. Kerjakan [plans/batch-resilience.md](plans/batch-resilience.md): satu link gagal atau tidak valid tidak boleh menghentikan seluruh batch.
3. Rapikan sisa: hapus `main.py`, perbarui `README.md` utama ke cara pakai lokal, tautkan folder `docs/`.
4. Pilih pekerjaan dari [ISSUES.md](ISSUES.md).
5. Opsional: [GDRIVE.md](GDRIVE.md) dan layanan systemd.

## Log keputusan

| Keputusan | Alasan |
|---|---|
| Mega dihapus | Limit Mega ketat dan `megatools` tidak tersedia |
| Terabox dihapus | Bergantung API pihak ketiga yang sering error |
| `/gdupload` dihapus | Butuh Google Drive ter-mount di `/content/drive`, tidak ada di luar Colab |
| Download Google Drive: kode dipertahankan, token ditunda | Jarang dipakai dan pembuatan token butuh intervensi manual |
| Konfigurasi aria2 pribadi dinonaktifkan di sistem (file `aria2.conf` diganti nama jadi `.bak`), kode bot tidak diubah | Berisi `daemon=true` (sisa percobaan RPC dengan UI web), membuat `aria2c` langsung ke background |
| `thinkbroadband.com` tidak dipakai sebagai link uji | Diblokir dari jaringan ini (aria2c exit code 22) |
| Kegagalan aria2c membatalkan seluruh task (patch 4.14) | Lebih baik dari melaporkan "selesai" dengan 0 file. **Akan diubah** menjadi per-link oleh rencana batch |
| `/drupload` mode Regular tidak mengonversi video (patch 4.7) | Melindungi file asli di folder pengguna |
| Shell fish, pesan commit berbahasa Inggris, satu commit per langkah | Preferensi kerja |

## Riwayat commit (urutan)

1. `build(deps): adjust requirements for local environment`
2. `chore: ignore local secrets and virtualenv`
3. `chore: ignore user-set thumbnail`
4. `refactor(init): load credentials.json relative to the repo`
5. `refactor(paths): replace Colab paths with local ones`
6. `fix(security): restrict all bot handlers to the owner`
7. `refactor: remove /gdupload command`
8. `fix(helper): detect any existing absolute path in isLink`
9. `fix(converters): drop GPUtil in favor of an nvidia-smi check`
10. `fix(handler): never convert or delete source files in dir-leech`
11. `fix(task): use Jakarta timezone and a real hero image fallback`
12. `refactor(task): route every mode through Do_Leech`
13. `fix(ytdl): use the correct yt-dlp option for concurrent fragments`
14. `refactor: remove Mega integration`
15. `refactor: remove Terabox integration`
16. `feat(handler): reject unsupported Mega and Terabox links up front`
17. `build: add run script for the local environment`
18. `fix(aria2): abort the task when aria2c fails`
19. `fix(telegram): build a file name for media without one`

Periksa dengan `git log --oneline`; `git status --short` harus kosong.
