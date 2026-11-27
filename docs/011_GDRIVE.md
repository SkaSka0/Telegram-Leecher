# Token Google Drive (Ditunda)

Hanya dibutuhkan untuk fitur **download dari link Google Drive**. Saat ini ditunda karena fitur ini jarang dipakai dan pembuatan token butuh intervensi manual di browser. Kode Drive tetap ada di repo.

Dikerjakan kalau suatu saat butuh download dari link Google Drive. Ringkasnya:

1. Google Cloud Console: aktifkan Google Drive API, buat OAuth client tipe **Desktop app**, simpan JSON sebagai `client_secret.json` di root repo.
2. `git mv google_auth.py gdrive_token.py`, lalu isi dengan skrip `InstalledAppFlow.run_local_server(port=0, access_type="offline", prompt="consent")` yang menyimpan `token.pickle` ke `~/.local/share/telegram-leecher/token.pickle` (scope `drive.readonly`).
3. Jalankan `.venv/bin/python gdrive_token.py`, login di browser.
4. Catatan: selama consent screen berstatus **Testing**, refresh token kedaluwarsa tiap 7 hari. Ubah ke **In production** agar bertahan lama.

Tanpa `token.pickle`, link Drive hanya membuat task dibatalkan dengan pesan error (pesannya masih menyebut "Google Drive Cell", sisa Colab).

Setelah token jadi, kerjakan uji 7.5 di [005_TESTING.md](005_TESTING.md): upload satu file kecil ke Drive, salin tautannya, kirim lewat `/tupload` mode Regular. Hasil yang benar: engine `G-Api`, nama file asli, `File Count` 1.

Perhatikan: `google_auth.py` (versi Colab) masih ada di repo. Ganti dengan `gdrive_token.py` saat tahap ini dikerjakan.
