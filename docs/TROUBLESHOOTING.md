# Troubleshooting

Gejala yang pernah muncul selama migrasi beserta solusinya.

| Gejala | Penyebab dan solusi |
|---|---|
| `aria2c` keluar seketika dengan exit 0 tanpa output, bot melapor `UNKNOWN DOWNLOAD NAME` / `0 Files` | Konfigurasi aria2 pribadi (`~/.aria2/aria2.conf` atau `~/.config/aria2/aria2.conf`) berisi `daemon=true`, sehingga aria2c langsung ke background. Ganti nama kedua file jadi `.bak` (jangan hapus), hentikan daemon dengan `pkill aria2c`, dan jalankan daemon RPC secara eksplisit lewat `--conf-path` bila perlu. Jangan menaruh `console-log-level` atau `summary-interval` di konfigurasi default karena bot membaca nama file dari keluaran level `notice` |
| `aria2c` exit code 22 | Server mengirim respons HTTP tak terduga, biasanya diblokir ISP. Pakai link dari host lain |
| `ModuleNotFoundError` saat `python -c ...` | venv belum aktif. Pakai `.venv/bin/python` atau `source .venv/bin/activate.fish` |
| `PEER_ID_INVALID` | Belum ada pesan di `DUMP_ID`, atau ID tidak diawali `-100`. Kirim pesan manual ke channel dump |
| `ModuleNotFoundError: moviepy.editor` | moviepy 2.x terpasang. Pastikan `moviepy<2` |
| `ModuleNotFoundError: distutils` | `GPUtil` masih ter-import. Selesaikan patch 4.6 |
| `tgcrypto` gagal build | Pasang `base-devel`, pakai Python 3.12 |
| `msg_id is too low/high` | Jam sistem tidak sinkron: `timedatectl set-ntp true` |
| Bot hidup tapi diam | `USER_ID` salah, filter owner menolak Anda |
| Error session aneh setelah ganti token | Hapus `my_bot.session*`, jalankan ulang |
| YouTube gagal / "no JS runtime" | Pasang `deno` atau `nodejs`, update `yt-dlp` |
| Perintah terminal dengan `<<'EOF'` gagal | Itu sintaks bash. Di fish pakai `printf`, `python -c '...'`, atau editor |
| `grep` menampilkan "binary file matches" di `__pycache__` | File bytecode lama, abaikan atau pakai `grep -I --include="*.py"` |
