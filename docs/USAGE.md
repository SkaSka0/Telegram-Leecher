# Cara Memakai Bot

Semua perintah hanya dibalas untuk akun owner (`USER_ID` di `credentials.json`); akun lain diabaikan.

## Perintah

| Perintah | Fungsi |
|---|---|
| `/start` | Cek bot hidup |
| `/tupload` | Download dari link, lalu upload ke Telegram (channel dump) |
| `/ytupload` | Seperti `/tupload`, tetapi semua link diproses yt-dlp |
| `/lcupload` | Download dari link, lalu salin ke `~/Downloads/Leecher` (tidak diupload ke Telegram) |
| `/drupload` | Upload folder atau file **lokal** ke Telegram (kirim path absolut, misalnya `/mnt/data/folder`) |
| `/settings` | Pengaturan: Media/Document, video (convert, split, format, kualitas), caption, thumbnail, prefix, suffix |
| `/setname`, `/zipaswd`, `/unzipaswd` | Nama file dan password; lihat catatan di bawah |
| `/help` | Daftar bantuan |

Kirim sebuah **gambar** kapan saja untuk menjadikannya thumbnail.

## Alur satu task

1. Kirim perintah (`/tupload`, dst.).
2. Kirim link, satu per baris (atau path untuk `/drupload`).
3. Pilih mode: **Regular** (unggah apa adanya), **Compress** (zip), **Extract** (ekstrak dulu), **UnDoubleZip** (ekstrak lalu zip ulang).

## Nama file kustom dan password

Argumen ditulis di **baris paling bawah** pesan (maksimal tiga, urutan bebas), masing-masing satu baris:

| Awal baris | Fungsi |
|---|---|
| `[nama]` | Nama file kustom |
| `{password}` | Password untuk membuat zip |
| `(password)` | Password untuk membuka arsip |

Contoh:

```
https://raw.githubusercontent.com/SkaSka0/Telegram-Leecher/main/custom_thmb.jpg
[foto-saya.jpg]
```

Aturan:

- Nama harus **di dalam kurung siku**. Tanpa kurung, baris itu dianggap link lain.
- Mode Regular: **sertakan ekstensi** (`[video-saya.mp4]`).
- Mode Compress: tulis nama **tanpa** `.zip` (`[arsip-saya]`), karena `.zip` ditambahkan otomatis.
- **Satu link per nama kustom.** Pada mode Regular, semua file hasil unduhan diganti ke nama yang sama sehingga saling menimpa. Untuk banyak link, jangan pakai nama kustom (kecuali mode Compress, di mana nama itu menjadi nama arsip).

### Catatan `/setname`, `/zipaswd`, `/unzipaswd`

Setiap kali Anda mengirim link, bot **mengosongkan** nama kustom dan kedua password. Jadi ketiga perintah itu hanya berlaku bila dikirim **setelah** link dan **sebelum** menekan tombol mode. Cara kurung (`[ ]`, `{ }`, `( )`) di atas lebih sederhana dan lebih aman.

## Sumber yang didukung

| Sumber | Catatan |
|---|---|
| Direct link | Lewat aria2 |
| YouTube (`youtube.com`, `youtu.be`) | Lewat yt-dlp. Nama file hasil berupa ID video; tambahkan `[nama.mp4]` untuk nama lain |
| Link pesan Telegram (`t.me/c/...`) | Bot harus menjadi member chat itu |
| Google Drive | Butuh `token.pickle` ([GDRIVE.md](GDRIVE.md)) |
| Magnet/torrent | Lewat aria2, tidak dijamin |
| Path lokal | Hanya `/drupload` |
| Mega, Terabox | **Tidak didukung** (dihapus) |

## Perilaku normal (bukan bug)

- `BOT_WORK` **tidak** dihapus setelah task sukses. Isinya dibersihkan sebagian, dan folder ini dihapus total di awal task berikutnya atau saat task dibatalkan. `Hero.jpg` di dalamnya selalu di-overwrite, jadi tidak menumpuk.
- Potongan hasil split video tidak persis seukuran batas, karena pemotongan `-c copy` hanya bisa jatuh di keyframe.
- `/drupload` mode Regular tidak mengonversi video; file asli di folder Anda tidak disentuh.
- Arsip hasil Compress berisi folder dengan nama file di dalamnya (misalnya `a.txt/a.txt`); itu bawaan cara bot mengarsipkan.
- Saat ini, jika salah satu link dalam satu task gagal, **seluruh task dibatalkan** dan file link yang sudah selesai ikut terhapus. Ini akan diubah oleh [PLAN-BATCH-RESILIENCE.md](PLAN-BATCH-RESILIENCE.md).
