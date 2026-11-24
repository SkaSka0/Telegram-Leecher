# Rencana: Satu Link Gagal Tidak Menghentikan Batch

**Status:** rencana, belum dikerjakan.
**Prasyarat:** uji 7.8, 7.9, dan 7.10 di [TESTING.md](TESTING.md) selesai, dan `git status --short` bersih.

## Masalah

Saat mengirim banyak link sekaligus, satu link yang gagal atau tidak valid membatalkan **seluruh task**, dan folder kerja dihapus termasuk file dari link sebelumnya yang sudah selesai. Titik-titik penyebabnya di kode saat ini:

| # | Lokasi | Perilaku sekarang |
|---|---|---|
| 1 | `handle_url` (`__main__.py`) | Hanya baris pertama yang divalidasi `isLink`. Baris lain yang bukan link (misalnya nama file tanpa `[ ]`) dianggap sumber dan akan gagal di aria2. Patch 4.13 menolak **seluruh pesan** bila ada satu link Mega/Terabox |
| 2 | `calDownSize` (`downlader/manager.py`) | Error Drive memanggil `cancelTask`. Link Telegram tanpa media membuat `media_Identifier` memanggil `cancelTask` lalu mengembalikan `None`, sehingga pemanggil crash dengan `TypeError` |
| 3 | `get_d_name` (hanya link pertama) | Kegagalan YouTube pada link pertama memanggil `cancelTask` lewat `get_YT_Name` |
| 4 | `downloadManager` | `except Exception` lalu `cancelTask` lalu `return`: satu link gagal membatalkan semuanya |
| 5 | Downloader yang memanggil `cancelTask` sendiri | `gdrive.py` (`getIDFromURL`, `gDownloadFile`), `telegram.py` (`media_Identifier`), `ytdl.py` (`get_YT_Name`) |
| 6 | Thread `YouTubeDL` (`ytdl.py`) | Kegagalan hanya dicatat (`YTDL ERROR`), tidak diteruskan: link gagal diam-diam dan task bisa "selesai" dengan 0 file (gejala yang sama dengan aria2 sebelum patch 4.14). Pada playlist, satu entri yang gagal menghentikan sisa playlist |
| 7 | Sisa file parsial | aria2c meninggalkan file parsial dan `.aria2`, yt-dlp meninggalkan `.part`. `Leech` mengunggah semua isi folder unduhan sehingga sampah ikut terkirim, dan `isYtdlComplete()` menunggu selamanya bila `.part` tidak hilang |
| 8 | `applyCustomName` | Mengganti nama semua file ke satu nama, sehingga saling menimpa bila ada lebih dari satu file |

## Perilaku target

- Link bermasalah **dilewati**, sisanya tetap diproses.
- Di akhir ada **ringkasan**: berapa link berhasil, serta daftar link gagal beserta alasannya.
- Task dibatalkan hanya bila **semua link gagal**, atau terjadi kesalahan skala task (lihat klasifikasi di bawah).
- File parsial dari link yang gagal **dibersihkan** sebelum lanjut.
- Tombol **Cancel** tetap membatalkan semuanya, dan perilaku mode Compress/Extract tidak berubah (hanya file yang berhasil yang diproses).

## Klasifikasi error

| Jenis | Contoh | Tindakan |
|---|---|---|
| **Per-link** | aria2 exit 3 (tidak ditemukan), 19 (DNS), 22 (respons HTTP aneh), 24 (autentikasi), timeout; file Drive tidak ada atau akses ditolak; pesan Telegram tanpa media atau tidak bisa diakses; yt-dlp `DownloadError`; baris bukan link | Catat, bersihkan parsial, **lanjut** |
| **Per-task** | Disk penuh (aria2 exit 9); `token.pickle` hilang atau refresh gagal; Cancel dari pengguna | **Hentikan** dengan `cancelTask` |

## Desain

### 1. Dua exception baru (berkas baru `colab_leecher/utility/errors.py`)

```python
class LinkError(Exception):
    """A single link failed; the rest of the batch can continue."""
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


class TaskAbort(Exception):
    """A task-wide failure; the whole task must stop."""
```

### 2. Pelacak hasil (`variables.py`)

```python
class LinkResults:
    ok = []       # links that finished
    failed = []   # (link, reason) pairs
```

Direset di `taskScheduler` bersama variabel lain, dan `YTDL` mendapat atribut `error = ""`.

### 3. `downloadManager`: isolasi per link

Pseudocode versi target (cabang non-YTDL):

```python
LinkResults.ok.clear()
LinkResults.failed.clear()

for i, link in enumerate(source):
    before = snapshot_files(Paths.down_path)
    try:
        await download_one(link, i + 1)          # isi if/elif yang sekarang
        LinkResults.ok.append(link)
    except TaskAbort as e:
        await cancelTask(str(e))
        return
    except LinkError as e:
        cleanup_new_files(Paths.down_path, before)
        LinkResults.failed.append((link, e.reason))
        logging.error(f"Skipped {link}: {e.reason}")
    except Exception as e:                        # kegagalan tak terduga
        cleanup_new_files(Paths.down_path, before)
        LinkResults.failed.append((link, f"Unexpected error: {e}"))
        logging.exception(f"Unexpected error for {link}")

if not LinkResults.ok:
    await cancelTask("All links failed.")
```

`CancelledError` adalah `BaseException`, jadi tombol Cancel tetap lolos dari `except Exception`.

### 4. Ubah downloader agar melempar exception, bukan memanggil `cancelTask`

| Berkas | Perubahan |
|---|---|
| `aria2.py` | `RuntimeError` hasil patch 4.14 menjadi `LinkError`; exit code 9 (disk penuh) menjadi `TaskAbort` |
| `gdrive.py` | `getIDFromURL` dan `gDownloadFile`: `cancelTask` diganti `raise LinkError`. `build_service` (token hilang atau refresh gagal) menjadi `TaskAbort` |
| `telegram.py` | `media_Identifier` melempar `LinkError` bila pesan atau media tidak ada, dan tidak lagi memanggil `cancelTask` atau mengembalikan `None` |
| `ytdl.py` | `get_YT_Name` melempar `LinkError`; lihat poin 5 untuk thread |

### 5. Kegagalan yang tidak terlihat di thread yt-dlp

- `YouTubeDL` (thread) mengisi `YTDL.error` saat ada exception, termasuk `DownloadError` per entri playlist (entri yang gagal dicatat, sisa playlist tetap jalan).
- `YTDL_Status` memeriksa `YTDL.error` setelah thread selesai dan melempar `LinkError`. `YTDL.error` direset di awal tiap link.
- Pembersihan parsial (poin 6) wajib untuk jalur ini supaya `isYtdlComplete()` tidak menunggu `.part` yang tersisa selamanya.

### 6. Pembersihan file parsial

Pendekatan perubahan minimal: ambil **snapshot** daftar file di folder unduhan sebelum tiap link, lalu setelah gagal hapus semua yang baru (termasuk `.aria2`, `.part`, `.ytdl`, folder playlist yang setengah jadi).

```python
def snapshot_files(path: str) -> set:
    found = set()
    for root, _, names in os.walk(path):
        for n in names:
            found.add(os.path.join(root, n))
    return found


def cleanup_new_files(path: str, before: set) -> None:
    for f in snapshot_files(path) - before:
        try:
            os.remove(f)
        except OSError:
            pass
```

(Alternatif yang lebih bersih tetapi lebih invasif: unduh tiap link ke subfolder sementara lalu pindahkan saat sukses. Ditolak karena mengubah struktur folder yang dipakai penamaan zip.)

### 7. `calDownSize` dan `get_d_name`

- Bungkus per link; gagal berarti **dilewati** (ukuran tidak dihitung), tanpa `cancelTask`.
- `get_d_name` mencoba link berurutan sampai ada nama; bila semua gagal, pakai nama generik `UNKNOWN DOWNLOAD NAME`. Tidak ada pembatalan di tahap ini.

### 8. Validasi baris di `handle_url`

- Pisahkan baris menjadi **valid** (URL `http(s)`, magnet, path yang ada) dan **dilewati** (bukan link, atau domain tidak didukung).
- Bila ada yang dilewati, balas satu pesan: "Skipped N line(s): ..." dan lanjutkan dengan yang valid.
- Bila tidak ada yang valid, tolak seluruh pesan seperti sekarang.
- Ini mengubah patch 4.13 dari "tolak seluruh pesan" menjadi "lewati baris Mega/Terabox dan beri tahu". **Perlu konfirmasi** (lihat bagian keputusan).

### 9. Laporan akhir (`SendLogs` di `handler.py`)

- `#LEECH_COMPLETE` ditambah baris `⚠️ Failed » N link(s)` bila ada.
- Pesan terpisah memuat daftar link gagal dan alasannya (link di dalam `<code>`), dipecah per 4096 karakter seperti `final_texts` yang sudah ada.
- Bila semua gagal: `#TASK_STOPPED` dengan daftar alasan (dari `cancelTask`).

### 10. Nama kustom

`applyCustomName` hanya berjalan bila hasil unduhan tepat **satu file**. Bila lebih, nama kustom dilewati dan peringatan dimasukkan ke laporan akhir.

## Urutan commit (bahasa Inggris, satu per langkah)

1. `feat(errors): add LinkError and TaskAbort exceptions`
2. `feat(task): track per-link results during a batch`
3. `refactor(downloaders): raise LinkError or TaskAbort instead of cancelling the task`
4. `fix(ytdl): propagate thread failures and per-entry playlist errors`
5. `fix(manager): remove partial files left behind by a failed link`
6. `refactor(manager): isolate failures per link and cancel only when all fail`
7. `fix(manager): do not abort on size or name lookup errors`
8. `feat(handler): skip invalid lines instead of rejecting the whole message`
9. `feat(report): list failed links in the final report`
10. `fix(helper): apply the custom name only when one file was downloaded`

Setiap langkah diuji sebelum commit berikutnya, mulai dari langkah 1 sampai 3 (tidak mengubah perilaku selama `downloadManager` belum diubah) lalu langkah 4 sampai 6.

## Matriks uji

Gunakan server HTTP lokal dari [TESTING.md](TESTING.md) dengan `a.txt`, `b.txt`, dan satu link yang sengaja 404 (`http://127.0.0.1:8000/tidak-ada.txt`).

| # | Input | Hasil yang benar |
|---|---|---|
| 1 | `a.txt`, link 404, `b.txt` (Regular) | Dua file terkirim; ringkasan: 1 gagal (not found) |
| 2 | Link 404 di **posisi pertama**, lalu `a.txt` | `a.txt` tetap terkirim; nama task tidak `None` |
| 3 | Semua link gagal | `#TASK_STOPPED` dengan daftar alasan; `BOT_WORK` terhapus |
| 4 | Baris bukan link di tengah (teks biasa) | Baris dilewati dengan pesan; link lain diproses |
| 5 | Link Mega/Terabox di antara link valid | Dilewati dan diberi tahu; sisanya jalan |
| 6 | YouTube tidak valid (`watch?v=invalid000`) + `a.txt` | Link YouTube gagal tercatat; `a.txt` terkirim; tidak menggantung |
| 7 | Link pesan Telegram ke pesan teks + `a.txt` | Gagal tercatat; `a.txt` terkirim; tidak ada `TypeError` |
| 8 | Mode Compress dengan satu link gagal | Zip hanya berisi file yang berhasil; tidak ada sisa `.aria2` |
| 9 | Dua link berhasil + nama kustom `[x.txt]` | Nama kustom dilewati dengan peringatan; kedua file utuh |
| 10 | Cancel di tengah batch | `#TASK_STOPPED` dengan `Reason » User Cancelled !`; semua dihentikan |
| 11 | Satu link gagal di tengah batch besar | Tidak ada file parsial (`.aria2`, `.part`) di dump |

## Risiko

- `cancelTask` memanggil `BOT.TASK.cancel()` dan dipakai di banyak jalur; setelah perubahan, uji Cancel (uji 10) ulang.
- `Transfer.down_bytes` hanya boleh bertambah pada link yang berhasil, supaya persentase progres tetap benar.
- Perubahan menyentuh banyak berkas; kerjakan bertahap dan selalu pertahankan commit kecil.

## Keputusan yang perlu dikonfirmasi

1. **Baris Mega/Terabox:** dilewati dengan pemberitahuan (disarankan) atau tetap menolak seluruh pesan seperti sekarang?
2. **Link gagal diulang otomatis?** Aria2 sudah memakai `--max-tries=3`, jadi tambahan percobaan ulang di tingkat bot tidak disarankan.
3. **Format ringkasan:** satu pesan terpisah berisi daftar link gagal (disarankan), atau digabung ke `#LEECH_COMPLETE` saja?
4. **Bila semua link gagal:** tetap `#TASK_STOPPED` (disarankan) atau `#LEECH_COMPLETE` dengan 0 file?
