# Versioning

Bot ini memakai **Semantic Versioning** dengan tiga angka: `MAJOR.MINOR.PATCH` (contoh `0.1.0`). Versi pertama fork lokal adalah **0.1.0**. Riwayat perubahan per versi ada di [009_CHANGELOG.md](009_CHANGELOG.md).

## Arti tiap angka

| Angka | Naik bila | Contoh |
|---|---|---|
| **MAJOR** | Perubahan yang merusak kompatibilitas: format `credentials.json` berubah, perintah dihapus atau diganti, perilaku lama tidak lagi berlaku | Menghapus `/drupload`; mengganti struktur kredensial |
| **MINOR** | Fitur baru yang tidak merusak pemakaian lama | Batch tahan-gagal (PLAN-BATCH-RESILIENCE), dukungan Google Drive aktif, layanan systemd |
| **PATCH** | Perbaikan bug atau perubahan kecil tanpa fitur baru | Perbaikan nama file, pesan error, dokumentasi kode |

Aturan tambahan:

- Setiap kali angka naik, angka di kanannya **kembali ke 0** (`0.1.4` → `0.2.0`, `0.9.2` → `1.0.0`).
- Selama MAJOR masih `0`, bot dianggap **belum stabil**: perubahan di MINOR boleh mengubah perilaku. Naik ke `1.0.0` setelah semua uji di [005_TESTING.md](005_TESTING.md) lolos dan rencana batch selesai.
- Perubahan dokumentasi saja (folder `docs/`, `README.md`) **tidak** menaikkan versi, kecuali dikerjakan bersama perubahan kode.
- Satu rilis boleh berisi beberapa commit. Naikkan versi **sekali per rilis**, bukan per commit.

## Cara merilis versi baru

1. Pastikan `git status --short` kosong dan uji yang relevan lolos.
2. Tentukan angka baru dari tabel di atas.
3. Di [009_CHANGELOG.md](009_CHANGELOG.md), pindahkan isi `[Belum dirilis]` ke bagian baru `## [X.Y.Z] - TAHUN-BULAN-TANGGAL`.
4. Ubah `__version__` di `colab_leecher/_version.py` (lihat "Sumber nomor versi").
5. Commit dan beri tag:

```fish
git add docs/009_CHANGELOG.md colab_leecher/_version.py
git commit -m "chore(release): v0.2.0" -m "Move the unreleased entries to 0.2.0 in the changelog."
git tag -a v0.2.0 -m "v0.2.0"
```

Sertakan `colab_leecher/_version.py` di `git add` yang sama. Bila branch sudah di-push, kirim tag juga: `git push origin lokal --tags`.

## Sumber nomor versi

Nomor versi hanya ditulis di **satu tempat**: `colab_leecher/_version.py`.

```python
__version__ = "0.1.1"
```

Berkas ini sengaja tidak meng-import apa pun dari paket lain, sehingga bisa dibaca tanpa `credentials.json`. Semua yang lain (pesan `/start`, `/version`, log startup, `run.sh --version`) mengambil dari sini. Jangan menulis nomor versi di tempat lain selain [009_CHANGELOG.md](009_CHANGELOG.md) dan tag git.

## Cara melihat versi

| Cara | Hasil |
|---|---|
| `./run.sh --version` | Versi dan build, tanpa menjalankan bot dan tanpa butuh `credentials.json` |
| `/version` di Telegram | Versi, build, versi Python, `pyrofork`, `yt-dlp`, lisensi, upstream |
| `/start` di Telegram | Baris versi di bawah deskripsi bot |
| Log saat bot start | `Colab Leecher Started ! Telegram Leecher (lokal) v0.1.1 (...)` |
| `git describe --tags --always --dirty` | Posisi kode terhadap tag terakhir |

Arti **build** (hasil `git describe`):

| Contoh | Arti |
|---|---|
| `v0.1.1` | Tepat di tag rilis |
| `v0.1.1-3-g1a2b3c4` | Tiga commit setelah `v0.1.1`, commit `1a2b3c4` |
| `v0.1.1-3-g1a2b3c4-dirty` | Sama, tetapi ada perubahan yang belum di-commit |
| `1a2b3c4` | Belum ada tag sama sekali |
| `unknown (no git)` | Folder dijalankan tanpa repo git |

Bila build menunjukkan `-dirty` atau commit setelah tag, kode yang berjalan **bukan** rilis resmi.

## Format pesan commit dan changelog

- Pesan commit tetap bahasa Inggris, gaya Conventional Commits (`fix(scope): ringkasan`), satu commit per langkah.
- Tipe commit membantu menentukan angka versi: `feat` biasanya MINOR, `fix` biasanya PATCH, perubahan yang merusak (tandai dengan `!`, misalnya `feat(handler)!: ...`) MAJOR.
- Isi CHANGELOG ditulis dalam bahasa Indonesia, ringkas, dikelompokkan: **Ditambahkan**, **Diubah**, **Diperbaiki**, **Dihapus**, **Keamanan**.
