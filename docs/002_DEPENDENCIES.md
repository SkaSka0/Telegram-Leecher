# Dependensi Sistem (Arch Linux)

Daftar aplikasi yang harus terpasang **sebelum** menjalankan bot. Dependensi Python ada di `requirements.txt` dan dipasang ke `.venv` (lihat [003_SETUP.md](003_SETUP.md), Langkah 2). Perintah kompatibel **fish shell**.

## Wajib

| Paket pacman | Perintah yang dipakai | Dipakai untuk |
|---|---|---|
| `aria2` | `aria2c` | Unduh direct link dan magnet; juga gambar hero tiap task |
| `ffmpeg` | `ffmpeg`, `ffprobe` | Konversi video, split video, baca bitrate |
| `zip` | `zip` | Mode Compress tanpa password |
| `7zip` | `7z` | Compress dengan password, Extract (`.7z`, `.zip`, `.001`, `.z01`) |
| `unrar` | `unrar` | Extract arsip `.rar` |
| `git` | `git` | Clone repo dan commit |
| `base-devel` | `gcc`, `make` | Build `tgcrypto` saat `pip install` |
| `uv` | `uv` | Membuat venv Python 3.12 dan memasang dependensi |

`tar` dan `gzip` (untuk `.tar` dan `.gz`) sudah termasuk paket dasar Arch.

Pasang sekaligus:

```fish
sudo pacman -S --needed aria2 ffmpeg zip 7zip unrar base-devel git uv
```

## Opsional

| Paket pacman | Dipakai untuk | Bila tidak dipasang |
|---|---|---|
| `deno` (atau `nodejs`) | Runtime JavaScript yang dibutuhkan yt-dlp untuk YouTube | YouTube gagal dengan "no JS runtime" |
| `nvidia-utils` | `nvidia-smi`; konversi video lewat GPU (`h264_nvenc`) | Bot otomatis memakai CPU (`libx264`) |

```fish
sudo pacman -S --needed deno
sudo pacman -S --needed nvidia-utils    # hanya bila punya GPU NVIDIA
```

## Pengaturan sistem

Sinkronkan jam, supaya tidak muncul error `msg_id is too low/high` dari Telegram:

```fish
timedatectl set-ntp true
```

Pastikan tidak ada konfigurasi aria2 pribadi yang berisi `daemon=true` (`~/.aria2/aria2.conf` atau `~/.config/aria2/aria2.conf`). Gejala dan solusinya ada di [006_TROUBLESHOOTING.md](006_TROUBLESHOOTING.md).

## Python

Bot memakai **Python 3.12** lewat `uv` (bukan Python sistem), karena `GPUtil` dan beberapa paket lama rusak di versi lebih baru dan `tgcrypto` paling aman dibangun di 3.12:

```fish
uv venv --python 3.12 .venv
uv pip install -r requirements.txt
```

## Verifikasi

Jalankan ini; semua baris harus berawalan `ok` (kecuali yang opsional):

```fish
for t in aria2c ffmpeg ffprobe zip 7z unrar tar git uv gcc make
    if type -q $t
        echo "ok       $t"
    else
        echo "MISSING  $t"
    end
end
for t in deno nvidia-smi
    if type -q $t
        echo "ok       $t (opsional)"
    else
        echo "absen    $t (opsional)"
    end
end
```

Lalu cek paket Python:

```fish
.venv/bin/python -c 'import colab_leecher.downlader.manager; print("import OK")'
```

Kalau `import OK` muncul, dependensi Python sudah lengkap. Bila `credentials.json` belum dibuat, perintah ini gagal dengan `FileNotFoundError`; selesaikan [003_SETUP.md](003_SETUP.md) Langkah 3 dulu.

## Tidak diperlukan

`megatools` (integrasi Mega dihapus), `ffmpeg` versi GPU khusus, Docker, dan `p7zip` (di Arch sekarang diganti `7zip`).
