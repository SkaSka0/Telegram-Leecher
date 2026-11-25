# Versioning

Bot ini memakai **Semantic Versioning** dengan tiga angka: `MAJOR.MINOR.PATCH` (contoh `0.1.0`). Versi pertama fork lokal adalah **0.1.0**. Riwayat perubahan per versi ada di [CHANGELOG.md](CHANGELOG.md).

## Arti tiap angka

| Angka | Naik bila | Contoh |
|---|---|---|
| **MAJOR** | Perubahan yang merusak kompatibilitas: format `credentials.json` berubah, perintah dihapus atau diganti, perilaku lama tidak lagi berlaku | Menghapus `/drupload`; mengganti struktur kredensial |
| **MINOR** | Fitur baru yang tidak merusak pemakaian lama | Batch tahan-gagal (PLAN-BATCH-RESILIENCE), dukungan Google Drive aktif, layanan systemd |
| **PATCH** | Perbaikan bug atau perubahan kecil tanpa fitur baru | Perbaikan nama file, pesan error, dokumentasi kode |

Aturan tambahan:

- Setiap kali angka naik, angka di kanannya **kembali ke 0** (`0.1.4` → `0.2.0`, `0.9.2` → `1.0.0`).
- Selama MAJOR masih `0`, bot dianggap **belum stabil**: perubahan di MINOR boleh mengubah perilaku. Naik ke `1.0.0` setelah semua uji di [TESTING.md](TESTING.md) lolos dan rencana batch selesai.
- Perubahan dokumentasi saja (folder `docs/`, `README.md`) **tidak** menaikkan versi, kecuali dikerjakan bersama perubahan kode.
- Satu rilis boleh berisi beberapa commit. Naikkan versi **sekali per rilis**, bukan per commit.

## Cara merilis versi baru

1. Pastikan `git status --short` kosong dan uji yang relevan lolos.
2. Tentukan angka baru dari tabel di atas.
3. Di [CHANGELOG.md](CHANGELOG.md), pindahkan isi `[Belum dirilis]` ke bagian baru `## [X.Y.Z] - TAHUN-BULAN-TANGGAL`.
4. Perbarui nomor versi di sumbernya (lihat bagian "Sumber nomor versi").
5. Commit dan beri tag:

```fish
git add docs/CHANGELOG.md
git commit -m "chore(release): v0.2.0" -m "Move the unreleased entries to 0.2.0 in the changelog."
git tag -a v0.2.0 -m "v0.2.0"
```

Tambahkan file lain yang berubah (misalnya `colab_leecher/__init__.py`) ke `git add` yang sama. Bila branch sudah di-push, kirim tag juga: `git push origin lokal --tags`.

## Sumber nomor versi

Satu-satunya sumber kebenaran sebaiknya satu konstanta di kode:

```python
# colab_leecher/__init__.py
__version__ = "0.1.0"
```

**Status:** belum dipasang di kode; saat ini nomor versi baru tercatat di dokumen dan tag git. Langkah yang disarankan (dikerjakan sebagai rilis PATCH berikutnya):

1. Tambahkan `__version__` di atas, dekat `ROOT`.
2. Tampilkan di `/start`, misalnya `Colab Leecher v0.1.0`, memakai `from colab_leecher import __version__` di `__main__.py`.
3. Catat di CHANGELOG di bawah `Ditambahkan`.

Commit yang disarankan:

```fish
git add colab_leecher/__init__.py colab_leecher/__main__.py docs/CHANGELOG.md
git commit -m "feat(version): expose the bot version in /start" -m "Add __version__ to the package and show it in the /start reply so the running version can be checked from Telegram."
```

## Format pesan commit dan changelog

- Pesan commit tetap bahasa Inggris, gaya Conventional Commits (`fix(scope): ringkasan`), satu commit per langkah.
- Tipe commit membantu menentukan angka versi: `feat` biasanya MINOR, `fix` biasanya PATCH, perubahan yang merusak (tandai dengan `!`, misalnya `feat(handler)!: ...`) MAJOR.
- Isi CHANGELOG ditulis dalam bahasa Indonesia, ringkas, dikelompokkan: **Ditambahkan**, **Diubah**, **Diperbaiki**, **Dihapus**, **Keamanan**.
