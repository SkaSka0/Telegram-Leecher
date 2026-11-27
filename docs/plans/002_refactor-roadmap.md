# Roadmap Refactor (setelah konversi lokal)

Menggantikan `ROADMAP.md` lama (era Colab). Bagian yang sudah tidak relevan dibuang: sinkronisasi README untuk Mega/Terabox, `ProcessPoolExecutor` Mega, parsing progres Mega, retry Terabox, dan urutan pengujian yang bergantung pada notebook Colab.

Pelacak per item ada di [007_ISSUES.md](../007_ISSUES.md). Berkas ini hanya menyimpan **alasan dan urutan**.

## Prasyarat (jangan mulai refactor sebelum ini)

1. Uji 7.8, 7.9, 7.10 di [005_TESTING.md](../005_TESTING.md) lolos.
2. [001_batch-resilience.md](001_batch-resilience.md) selesai. Rencana itu mengambil alih "standarisasi penanganan error" (`LinkError` / `TaskAbort`), jadi refactor lain tidak boleh dibangun di atas pola error yang lama.
3. `git status --short` bersih.

## Patch era Colab yang sudah ada di kode

Sudah ada di kode, tetapi belum tercatat di [010_PATCHES.md](../010_PATCHES.md) maupun [009_CHANGELOG.md](../009_CHANGELOG.md). Catat saat verifikasi selesai.

| Patch | Berkas | Status | Verifikasi |
|---|---|---|---|
| Hapus file lama sebelum menulis (`gDownloadFile` tidak lagi menumpuk byte) | `gdrive.py` | Dipatch, belum diuji | Uji 7.5 (Drive ditunda), skenario "retry dengan nama sama": bandingkan ukuran/checksum dengan sumber |
| `cancelTask()` memanggil `BOT.TASK.cancel()` paling akhir | `handler.py` | Dipatch, **lolos uji 7.10** | Uji 7.10 |
| Penjagaan `BOT.State.task_going` di `Leech()` (race saat tombol Cancel ditekan) | `handler.py` | Dipatch, **lolos uji 7.10** | Uji 7.10; harus **tidak** ada `FileNotFoundError` di `os.stat` |
| Refresh otomatis `token.pickle` | `gdrive.py` (`build_service`) | Dipatch; skenario valid dan kedaluwarsa pernah lolos | Skenario token dicabut / format lama / berkas hilang menunggu 7.5 dan 7.10 |

Catatan: refresh token otomatis **sudah selesai** (item "fitur" di roadmap lama adalah duplikat).

## Urutan pengerjaan setelah prasyarat

### A. Keamanan dan kebenaran (lakukan dulu)

| Usulan ID | Item | Lokasi | Alasan |
|---|---|---|---|
| SEC-003 | `get_Aria2c_Name` menjalankan `aria2c ... "{link}"` dengan `shell=True`. Tanda kutip di dalam link bisa merusak atau menyisipkan perintah | `downlader/aria2.py` | Satu-satunya tempat link dari pengguna masuk ke shell. Minimal: ganti ke daftar argumen. Digabung dengan SEC-001 bila memungkinkan |
| BUG-006 | `gDownloadFolder` tidak menyaring shortcut ke Google Docs/Sheets sebelum `gDownloadFile` | `downlader/gdrive.py` | Folder Drive bisa gagal di tengah jalan. Kerjakan bersama FEAT-004 (token Drive), karena baru bisa diuji saat itu |

### B. Struktur

| Usulan ID | Item | Catatan |
|---|---|---|
| CHORE-005 | Pecah fungsi besar: `Leech()` (`handler.py`), `taskScheduler()` (`task_manager.py`), `YouTubeDL()` (`ytdl.py`) | `Leech()` kini lebih panjang karena penjagaan `task_going`; pecah per tahap (konversi, cek ukuran, upload split, upload biasa, bersih-bersih) tanpa mengubah perilaku. Satu fungsi per commit, uji Regular/Compress/Extract/Split setelah tiap commit |
| FEAT-005 | Ganti dua kali `aria2c` di `get_Aria2c_Name` dengan satu permintaan `HEAD` | Hati-hati: `--dry-run` aria2 menghormati `Content-Disposition` dan redirect; `HEAD` harus menangani keduanya, dan sebagian server menolak `HEAD`. Sediakan fallback ke nama dari URL |
| (keputusan) | Dukungan multi-task (`variables.py` jadi namespace per task) | Bot dirancang satu-pemilik, satu-task. **Default: tidak dikerjakan.** Buka lagi hanya bila ada kebutuhan nyata |

### C. Keandalan dan observabilitas

| Usulan ID | Item | Catatan |
|---|---|---|
| CHORE-006 | Ganti sisa `print()` dengan `logging` | Sisa saat ini: `downlader/manager.py`, `utility/task_manager.py` (`Do_Leech`), `utility/helper.py` (`thumbMaintainer`). `handler.py` sudah bersih |
| TEST-004 | Uji unit untuk fungsi murni | `sizeUnit`, `getTime`, `speedETA`, `fileType`, `shortFileName` (`helper.py`), `getIDFromURL` (`gdrive.py`), `media_Name` (`telegram.py`). **Kendala:** semua modul itu mengimpor `colab_leecher`, yang membaca `credentials.json` saat di-import. Pakai `credentials.json` palsu di fixture uji, atau pindahkan fungsi murni ke modul tanpa efek samping |
| FEAT-006 | Retry untuk downloader Drive dan Telegram | aria2 sudah punya `--max-tries=3`. Kerjakan **setelah** batch-resilience supaya retry berada di dalam isolasi per link |

## Dibuang dari roadmap lama

| Item lama | Alasan |
|---|---|
| Fase 0 (sinkronisasi README Mega/Terabox) | Keduanya sudah dihapus. Pembaruan README diwakili CHORE-003 |
| `ProcessPoolExecutor` tak terpakai | Hilang bersama integrasi Mega (patch 4.11) |
| Parsing progres Mega yang rapuh | Mega dihapus |
| Retry untuk Terabox | Terabox dihapus |
| Refresh token Drive otomatis sebagai fitur | Sudah dikerjakan sebagai patch |
| Resolver GDTot/Sharer/short link | Tidak ada di ruang lingkup fork lokal ([docs/README.md](../README.md)). Buka lagi hanya bila benar-benar dibutuhkan |
| Standarisasi error handling | Digantikan [001_batch-resilience.md](001_batch-resilience.md) |
| Penjelasan "kenapa Issue #2 sebelum #3" | Konteks pengujian di Colab, sudah selesai dipatch |
