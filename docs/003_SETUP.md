# Setup dan Menjalankan Bot

Panduan memasang dan menjalankan fork lokal di Arch Linux dari nol. Perintah kompatibel **fish shell**.

> **Catatan:** semua perubahan kode dari versi Colab sudah dicatat di [010_PATCHES.md](010_PATCHES.md). Kalau branch `lokal` sudah di-push, cukup `git clone -b lokal` dan **lewati** langkah patch. Kalau mengerjakan dari branch `main`, kerjakan [010_PATCHES.md](010_PATCHES.md) dulu sebelum menjalankan bot (langkah "Jalan pertama" di bawah).

## Catatan umum

- **Shell fish:** aktivasi venv dengan `source .venv/bin/activate.fish`, atau panggil langsung `.venv/bin/python` (lebih aman). Kalau `python` biasa menghasilkan `ModuleNotFoundError: uvloop`, artinya venv belum aktif.
- **Aturan commit:** satu commit per langkah, `git add <file-spesifik>` (jangan `git add .` atau `git commit -a`), tipe `fix`/`refactor`/`feat`/`build`/`chore`/`docs`.
- **Branch kerja:** `lokal`. Branch `main` tetap sebagai cadangan versi Colab.
- **Folder penting:** repo di `~/Projects/Telegram-Leecher`, data di `~/.local/share/telegram-leecher/`, hasil `/lcupload` di `~/Downloads/Leecher`.

## Langkah 0: Kredensial Telegram

Siapkan lima nilai: `API_ID`, `API_HASH` (dari https://my.telegram.org), `BOT_TOKEN` (@BotFather), `USER_ID` (ID akun Anda), `DUMP_ID` (ID channel/grup dump, lengkap diawali `-100`). Bot harus admin di channel dump, dan **kirim satu pesan manual** di sana sebelum task pertama (mencegah `PEER_ID_INVALID`).

## Langkah 1: Paket sistem

Daftar lengkap paket wajib dan opsional, beserta fungsi tiap paket, ada di [002_DEPENDENCIES.md](002_DEPENDENCIES.md). Pasang paket wajib dari sana (satu perintah `pacman`), atur sinkronisasi jam (`timedatectl set-ntp true`, dijelaskan di berkas yang sama), lalu jalankan loop verifikasinya sampai tidak ada baris `MISSING`.

## Langkah 2: Clone, venv, dependency

```fish
mkdir -p ~/Projects; and cd ~/Projects
git clone https://github.com/SkaSka0/Telegram-Leecher.git
cd Telegram-Leecher
git checkout -b lokal
uv venv --python 3.12 .venv
source .venv/bin/activate.fish
```

Isi `requirements.txt`:

```fish
printf 'google-api-python-client\ngoogle-auth-httplib2\ngoogle-auth-oauthlib\nmoviepy<2\nnatsort\nPillow\npsutil\npytz\npyrofork\ntgcrypto\nuvloop\nyt-dlp[default]\n' > requirements.txt
uv pip install -r requirements.txt
```

Yang dibuang dari versi asli: `asyncio` (paket PyPI usang), `GPUtil` (rusak di Python ≥ 3.12), `opencv-python`, `pymegatools`, `requests`, `aiohttp`. `moviepy` di-pin `<2` karena `moviepy.editor` dihapus di versi 2.

Commit:

```fish
git add requirements.txt
git commit -m "build(deps): adjust requirements for local environment" -m "Remove asyncio (obsolete PyPI package), GPUtil (broken on Python >= 3.12), opencv-python, pymegatools, requests, and aiohttp, none of which are needed anymore. Pin moviepy<2 because moviepy.editor was removed in v2. Use yt-dlp[default]."
```

## Langkah 3: `credentials.json` dan `.gitignore`

Buat `credentials.json` di root repo lewat editor (API_ID, USER_ID, DUMP_ID berupa **angka**):

```json
{
    "API_ID": 123456,
    "API_HASH": "isi_api_hash",
    "BOT_TOKEN": "isi_bot_token",
    "USER_ID": 123456789,
    "DUMP_ID": -1001234567890
}
```

```fish
chmod 600 credentials.json
printf '\n# lokal\ncredentials.json\ntoken.pickle\nclient_secret.json\n.venv/\n' >> .gitignore
printf 'colab_leecher/Thumbnail.jpg\n' >> .gitignore
```

Verifikasi tanpa mencetak rahasia:

```fish
python -c 'import json; c=json.load(open("credentials.json")); print({k: type(c.get(k)).__name__ for k in ["API_ID","API_HASH","BOT_TOKEN","USER_ID","DUMP_ID"]}); print(str(c["DUMP_ID"]).startswith("-100"))'
git check-ignore -v credentials.json .venv
```

Hasil yang benar: tipe `int`, `str`, `str`, `int`, `int`, lalu `True`. Commit:

```fish
git add .gitignore
git commit -m "chore: ignore local secrets and virtualenv" -m "Add credentials.json, token.pickle, client_secret.json, .venv/, and the user-set thumbnail to .gitignore so credentials and runtime files are never committed."
```

## Langkah 4: Jalan pertama

Pastikan runtime Colab lama sudah dihentikan (dua instance dengan token sama saling berebut update).

```fish
printf '#!/usr/bin/env bash\ncd "$(dirname "$0")"\nif [ "$1" = "--version" ] || [ "$1" = "-V" ]; then\n    exec .venv/bin/python colab_leecher/_version.py\nfi\nexec .venv/bin/python -m colab_leecher\n' > run.sh
chmod +x run.sh
git add run.sh
git commit -m "build: add run script for the local environment" -m "Replace the Colab launcher with a small script that changes into the repository root and starts the bot with the virtualenv's Python, so my_bot.session is created next to the code and no manual activation is needed. Support --version, which prints the bot version without starting the bot."
./run.sh
```

Opsi `./run.sh --version` mencetak versi tanpa menjalankan bot dan tanpa butuh `credentials.json`; opsi ini bekerja setelah `colab_leecher/_version.py` ada (mulai versi 0.1.1, lihat [008_VERSIONING.md](008_VERSIONING.md)). Bila belum ada, lewati dulu.

Log yang sehat berisi `Colab Leecher Started !` (diikuti nomor versi mulai 0.1.1) dan `Started 16 HandlerTasks` (16 adalah worker dispatcher Pyrogram, bukan jumlah handler kita). Uji dari akun owner: `/start`, `/settings`, `/help`, dan `/version` (mulai 0.1.1). Dari akun lain, bot **tidak boleh membalas sama sekali**.

## Langkah 5: Service systemd (opsional)

`~/.config/systemd/user/telegram-leecher.service`:

```ini
[Unit]
Description=Telegram Leecher
After=network-online.target

[Service]
WorkingDirectory=%h/Projects/Telegram-Leecher
ExecStart=%h/Projects/Telegram-Leecher/run.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```fish
systemctl --user daemon-reload
systemctl --user enable --now telegram-leecher
journalctl --user -u telegram-leecher -f
```

Selanjutnya: [005_TESTING.md](005_TESTING.md) untuk menguji fitur satu per satu.
