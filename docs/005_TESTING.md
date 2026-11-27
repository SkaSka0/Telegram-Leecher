# Prosedur Uji Fitur

Uji dikerjakan **satu per satu** dengan file uji lokal yang disajikan lewat server HTTP sementara, supaya tidak bergantung pada jaringan luar. Status hasil uji ada di [001_PROGRESS.md](001_PROGRESS.md).

Sebelum mulai, bot harus sudah jalan (`./run.sh`, lihat [003_SETUP.md](003_SETUP.md)).

### Link uji

- File kecil dari GitHub: `https://raw.githubusercontent.com/SkaSka0/Telegram-Leecher/main/custom_thmb.jpg`
- **Jangan** pakai `thinkbroadband.com` (diblokir dari jaringan ini, aria2c exit code 22).
- Untuk uji yang butuh file khusus, buat sendiri lalu sajikan lewat server lokal:

```fish
mkdir -p /tmp/leech-fixtures
python3 -m http.server 8000 --bind 127.0.0.1 -d /tmp/leech-fixtures
```

### 7.1 Direct link ✅

`/tupload` → tempel link GitHub → **Regular**. Hasil: `Name » custom_thmb.jpg`, `1 Files`, foto sampai di dump. Uji kegagalan (link yang diblokir) harus menghasilkan `#TASK_STOPPED` dengan `Reason`, **bukan** `#LEECH_COMPLETE`.

### 7.2 Compress, Extract, UnDoubleZip ✅

Fixture:

```fish
pushd /tmp/leech-fixtures
printf 'halo\n' > a.txt
printf 'dunia\n' > b.txt
zip -q test.zip a.txt b.txt
popd
```

| Uji | Link | Mode | Hasil |
|---|---|---|---|
| A | `http://127.0.0.1:8000/a.txt` | Compress | Satu file `a.txt.zip` (isinya folder `a.txt/` berisi `a.txt`, memang bawaan bot) |
| B | `http://127.0.0.1:8000/test.zip` | Extract | Dua file `a.txt` dan `b.txt` |
| C | `http://127.0.0.1:8000/test.zip` | UnDoubleZip | Satu zip hasil kompres ulang isi `test.zip` |

### 7.3 YouTube ✅

Pra-uji: `.venv/bin/yt-dlp --simulate --print "%(title)s" "https://www.youtube.com/watch?v=jNQXAC9IVRw"`. Uji dari kedua jalur: `/ytupload` dan `/tupload` dengan link yang sama. Nama file hasil berupa **ID video** (`jNQXAC9IVRw.mp4`), bukan judul, karena template nama di `ytdl.py` memakai `%(id)s`.

### 7.4 Link pesan Telegram ✅

Salin link pesan dokumen dari channel dump (Copy Link, bentuk `https://t.me/c/<id>/<id-pesan>`), kirim lewat `/tupload`. Uji pesan **foto** harus menghasilkan nama `photo_<kode>.jpg` (bukan `None`).

### 7.5 Google Drive ⏸

Ditunda sampai token Google Drive dibuat (lihat [011_GDRIVE.md](011_GDRIVE.md)).

### 7.6 Konversi video ✅

```fish
ffmpeg -y -loglevel error -f lavfi -i testsrc=duration=5:size=640x360:rate=25 -f lavfi -i sine=frequency=440:duration=5 -c:v libx264 -c:a aac -shortest /tmp/leech-fixtures/clip.mov
```

Uji A: **Convert Yes** → `clip.mp4`, status memperlihatkan `Handler » CPU` (tanpa NVIDIA). Uji B: **Don't Convert** → `clip.mov` terkirim apa adanya. Keduanya bisa diputar.

### 7.7 Split file besar ✅

Turunkan batas sementara, **jangan di-commit**:

```fish
sed -i 's/SPLIT_SIZE_MB = 1950/SPLIT_SIZE_MB = 2/' colab_leecher/utility/variables.py
ffmpeg -y -loglevel error -f lavfi -i testsrc2=duration=20:size=640x360:rate=25 -vf noise=alls=40:allf=t -c:v libx264 -crf 23 -g 25 -pix_fmt yuv420p /tmp/leech-fixtures/clip_big.mp4
head -c 6291456 /dev/urandom > /tmp/leech-fixtures/big.bin
```

Uji A: `clip_big.mp4` dengan **Split Videos** → beberapa bagian `.partNNN.mp4`, masing-masing bisa diputar. Uji B: `big.bin` → tiga bagian `.z01`, `.z02`, `.zip`; gabungkan dengan `7z x big.bin.zip` lalu `cmp` dengan file asli (harus identik). Setelah uji, **kembalikan**:

```fish
git checkout -- colab_leecher/utility/variables.py
grep -n "SPLIT_SIZE_MB =" colab_leecher/utility/variables.py
```

### 7.8 `/lcupload` ⬜ (berikutnya)

Kirim `/lcupload`, tempel `http://127.0.0.1:8000/a.txt`, mode **Regular**. Hasil yang diharapkan: file muncul di `~/Downloads/Leecher/` (bukan di Telegram), dan pesan akhir `#LOCAL-MIRROR_COMPLETE`.

### 7.9 `/drupload` ⬜ (berikutnya)

Pakai **folder salinan**, bukan folder data asli:

```fish
mkdir -p /tmp/drtest/sub
cp /tmp/leech-fixtures/clip.mov /tmp/drtest/
cp /tmp/leech-fixtures/a.txt /tmp/drtest/sub/
find /tmp/drtest -type f | sort > /tmp/drtest.before
```

Kirim `/drupload`, tempel `/tmp/drtest`, mode **Regular**. Setelah selesai:

```fish
find /tmp/drtest -type f | sort | diff - /tmp/drtest.before; and echo "folder asli utuh"
```

Hasil yang benar: `folder asli utuh` (bukti patch 4.7 bekerja: `clip.mov` tidak dikonversi atau dihapus). Uji juga Compress pada folder yang sama, lalu path di luar `/home` (misalnya `/tmp/...` seperti di atas) harus dikenali (bukti patch 4.5).

### 7.10 Tombol Cancel ⬜

Mulai task dengan file yang lebih lambat (misalnya `big.bin` dengan batas split normal), tekan **Cancel ❌** di tengah proses. Hasil yang benar: pesan `#TASK_STOPPED` dengan `Reason » User Cancelled !` dan folder `BOT_WORK` terhapus. Setelah itu bot harus bisa menerima task baru.
