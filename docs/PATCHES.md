# Perubahan Kode dari Versi Colab

Catatan lengkap semua patch (4.1 sampai 4.15) yang dibutuhkan agar bot berjalan di Arch Linux, dengan kode, perintah, dan pesan commit. Semua pesan commit berbahasa Inggris, **satu commit per langkah**, dan selalu `git add <file-spesifik>` (jangan `git add .`).

| Patch | Berkas | Tujuan |
|---|---|---|
| 4.1 | `colab_leecher/__init__.py` | Path `credentials.json` relatif, `workdir` sesi |
| 4.2 | `colab_leecher/utility/variables.py` | Semua path ke lokasi lokal |
| 4.3 | `colab_leecher/__main__.py` | Filter owner pada semua handler (keamanan) |
| 4.4 | `colab_leecher/__main__.py` | Hapus `/gdupload` |
| 4.5 | `colab_leecher/utility/helper.py` | `isLink` mengenali path Linux |
| 4.6 | `colab_leecher/utility/converters.py` | Ganti `GPUtil` dengan cek `nvidia-smi` |
| 4.7 | `colab_leecher/utility/handler.py` | Konversi video tidak menghapus file asli |
| 4.8 | `colab_leecher/utility/task_manager.py` | Timezone, fallback hero, satu jalur `Do_Leech` |
| 4.9 | `colab_leecher/downlader/ytdl.py` | Opsi yt-dlp yang benar |
| 4.11 | beberapa berkas | Hapus integrasi Mega |
| 4.12 | beberapa berkas | Hapus integrasi Terabox |
| 4.13 | `colab_leecher/__main__.py` | Tolak link Mega/Terabox di awal |
| 4.14 | `colab_leecher/downlader/aria2.py` | Task dibatalkan saat aria2c gagal |
| 4.15 | `downlader/telegram.py`, `manager.py` | Nama file media Telegram tanpa `file_name` |

(Nomor 4.10 sengaja kosong: penghapusan `main.py` masih opsional, lihat bagian akhir.)

### 4.1 `colab_leecher/__init__.py`

Ganti seluruh isi:

```python
# copyright 2023 © Xron Trix | https://github.com/Xrontrix10

import logging, json, asyncio
from pathlib import Path
from uvloop import install
from pyrogram.client import Client

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "credentials.json", "r") as file:
    credentials = json.loads(file.read())

API_ID = credentials["API_ID"]
API_HASH = credentials["API_HASH"]
BOT_TOKEN = credentials["BOT_TOKEN"]
OWNER = credentials["USER_ID"]
DUMP_ID = credentials["DUMP_ID"]


logging.basicConfig(level=logging.INFO)

install()

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

colab_bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir=str(ROOT),
)
```

`workdir=str(ROOT)` membuat `my_bot.session` selalu dibuat di root repo.

```fish
git add colab_leecher/__init__.py
git commit -m "refactor(init): load credentials.json relative to the repo" -m "Replace the hardcoded /content/Telegram-Leecher path with a ROOT-relative path. Set workdir=ROOT on the Client so my_bot.session is always created in the repository root."
```

### 4.2 `colab_leecher/utility/variables.py`

Tambahkan di bagian import:

```python
from pathlib import Path as _P

_ROOT = _P(__file__).resolve().parents[2]
_DATA = _P.home() / ".local" / "share" / "telegram-leecher"
```

Ganti seluruh class `Paths`:

```python
class Paths:
    # PENTING: folder ini DIHAPUS (rmtree) setiap task baru dan saat cancel.
    # Jangan arahkan ke folder yang berisi data penting, dan jangan di /tmp (RAM).
    WORK_PATH = str(_DATA / "BOT_WORK")
    BASE_DOWN_PATH = f"{WORK_PATH}/Downloads"
    THMB_PATH = str(_ROOT / "colab_leecher" / "Thumbnail.jpg")
    VIDEO_FRAME = f"{WORK_PATH}/video_frame.jpg"
    HERO_IMAGE = f"{WORK_PATH}/Hero.jpg"
    DEFAULT_HERO = str(_ROOT / "custom_thmb.jpg")
    down_path = BASE_DOWN_PATH
    temp_dirleech_path = f"{WORK_PATH}/dir_leech_temp"
    local_mirror_dir = str(_P.home() / "Downloads" / "Leecher")
    temp_zpath = f"{WORK_PATH}/Leeched_Files"
    temp_unzip_path = f"{WORK_PATH}/Unzipped_Files"
    temp_files_dir = f"{WORK_PATH}/leech_temp"
    thumbnail_ytdl = f"{WORK_PATH}/ytdl_thumbnails"
    access_token = str(_DATA / "token.pickle")
```

```fish
mkdir -p ~/.local/share/telegram-leecher ~/Downloads/Leecher
git add colab_leecher/utility/variables.py
git commit -m "refactor(paths): replace Colab paths with local ones" -m "Move WORK_PATH to ~/.local/share/telegram-leecher, local_mirror_dir to ~/Downloads/Leecher, and the Drive token to the local data directory. Remove MOUNTED_DRIVE and mirror_dir, which were only used by /gdupload."
```

Hanya yang di bawah `WORK_PATH` yang dihapus bot. `THMB_PATH`, `DEFAULT_HERO`, `access_token`, dan `local_mirror_dir` sengaja di luarnya.

### 4.3 Filter owner di `__main__.py` (keamanan)

Tambahkan tepat di atas `src_request_msg = None`:

```python
owner_only = filters.user(OWNER)
```

Pasang ke semua decorator:

```fish
sed -i -E 's/^(@colab_bot\.on_message\(.*)\)$/\1 \& owner_only)/' colab_leecher/__main__.py
sed -i 's/@colab_bot\.on_callback_query()/@colab_bot.on_callback_query(owner_only)/' colab_leecher/__main__.py
grep -nE "on_(message|callback_query)" colab_leecher/__main__.py | grep -vc owner_only
```

Hasil yang benar: `0` (15 handler sebelum `/gdupload` dihapus, 14 sesudahnya).

```fish
git add colab_leecher/__main__.py
git commit -m "fix(security): restrict all bot handlers to the owner" -m "Only /settings checked OWNER, so anyone who found the bot could start downloads, and /drupload could upload arbitrary local files. Add an owner_only filter and apply it to every message and callback handler."
```

### 4.4 Buang `/gdupload`

Lihat dulu isinya, lalu hapus (nomor baris dari repo asli: decorator di baris 49, handler berikutnya di baris 59):

```fish
sed -n '47,59p' colab_leecher/__main__.py
sed -i '49,58d' colab_leecher/__main__.py
grep -c "gdupload" colab_leecher/__main__.py
```

Hasil yang benar: `0`. Kalau nomor baris di salinan Anda berbeda, hapus fungsi `drive_upload` secara manual lewat editor.

```fish
git add colab_leecher/__main__.py
git commit -m "refactor: remove /gdupload command" -m "Mirroring to Google Drive depends on Drive being mounted at /content/drive, which does not exist outside Colab. Local copying remains available through /lcupload."
```

### 4.5 `isLink` mengenali path Linux (`utility/helper.py`)

Ganti seluruh fungsi `isLink`:

```python
def isLink(_, __, update):
    if update.text:
        lines = update.text.strip().splitlines()
        if not lines:
            return False
        first = lines[0].strip()

        if ospath.isabs(first) and ospath.exists(first):
            return True
        if first.startswith("magnet:?xt=urn:btih:"):
            return True

        parsed = urlparse(first)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            return True

    return False
```

```fish
git add colab_leecher/utility/helper.py
git commit -m "fix(helper): detect any existing absolute path in isLink" -m "The old check only matched strings containing /content/ or /home, so paths such as /mnt or /run/media were ignored by /drupload. Accept the first line if it is an absolute path that exists on disk, and guard against empty messages."
```

### 4.6 Ganti `GPUtil` (`utility/converters.py`)

```fish
sed -i '/^import GPUtil$/d' colab_leecher/utility/converters.py
sed -i 's/gpu = len(GPUtil.getAvailable())/gpu = 1 if shutil.which("nvidia-smi") else 0/' colab_leecher/utility/converters.py
```

```fish
git add colab_leecher/utility/converters.py
git commit -m "fix(converters): drop GPUtil in favor of an nvidia-smi check" -m "GPUtil imports distutils, which no longer exists in Python >= 3.12. Detect an NVIDIA GPU with shutil.which('nvidia-smi') instead and fall back to CPU encoding otherwise."
```

### 4.7 Konversi video tidak boleh menghapus file asli (`utility/handler.py`)

```fish
sed -i 's/if BOT\.Options\.convert_video and fileType/if remove and BOT.Options.convert_video and fileType/' colab_leecher/utility/handler.py
```

Akibatnya `/drupload` mode Regular meng-upload video apa adanya tanpa konversi, dan file asli di folder Anda tidak disentuh.

```fish
git add colab_leecher/utility/handler.py
git commit -m "fix(handler): never convert or delete source files in dir-leech" -m "videoConverter runs in place and removes the original file. In /drupload the source folder is the user's own directory, so only convert files when remove=True, i.e. when working on a temporary copy."
```

### 4.8 `utility/task_manager.py`

**Fase A:** timezone dan fallback gambar hero.

```fish
sed -i 's/Asia\/Kolkata/Asia\/Jakarta/' colab_leecher/utility/task_manager.py
```

Tambahkan di bawah blok `try: system(...) except` (indentasi 4 spasi):

```python
    if not ospath.exists(Paths.HERO_IMAGE):
        shutil.copy(Paths.DEFAULT_HERO, Paths.HERO_IMAGE)
```

```fish
git add colab_leecher/utility/task_manager.py
git commit -m "fix(task): use Jakarta timezone and a real hero image fallback" -m "Switch the task date from Asia/Kolkata to Asia/Jakarta. os.system never raises when aria2c fails, so the except branch was dead code; copy the bundled default image into place when Hero.jpg was not downloaded."
```

**Fase B:** ganti dispatch di akhir `taskScheduler` (tiga cabang `if/elif/else`) menjadi satu baris:

```python
    await Do_Leech(BOT.SOURCE, is_dir, BOT.Mode.ytdl, is_zip, is_unzip, is_dualzip)
```

Lalu hapus `Do_Mirror` dan `Do_Local_Mirror` (di akhir file):

```fish
grep -n "^async def" colab_leecher/utility/task_manager.py
set n (grep -n "^async def Do_Mirror" colab_leecher/utility/task_manager.py | cut -d: -f1)
sed -i "$n,\$d" colab_leecher/utility/task_manager.py
grep -rnI "Do_Mirror\|Do_Local_Mirror\|MOUNTED_DRIVE\|Paths.mirror_dir" colab_leecher/ --include="*.py"
```

Hasil yang benar: tinggal `task_starter`, `taskScheduler`, `Do_Leech`, dan `grep` kosong (abaikan file `.pyc`).

```fish
git add colab_leecher/utility/task_manager.py
git commit -m "refactor(task): route every mode through Do_Leech" -m "The local-mirror branch was unreachable because the first condition (mode != mirror) already matched it, and the mirror branch depended on Google Drive being mounted at /content/drive. Remove Do_Mirror and Do_Local_Mirror; local copying is handled inside Leech()."
```

### 4.9 Opsi yt-dlp (`downlader/ytdl.py`)

```fish
sed -i 's/"--concurrent-fragments": 4 ,/"concurrent_fragment_downloads": 4,/' colab_leecher/downlader/ytdl.py
```

```fish
git add colab_leecher/downlader/ytdl.py
git commit -m "fix(ytdl): use the correct yt-dlp option for concurrent fragments" -m "The key '--concurrent-fragments' is a CLI flag and was silently ignored by the Python API. Use concurrent_fragment_downloads instead."
```

### 4.11 Buang integrasi Mega

```fish
git rm colab_leecher/downlader/mega.py
sed -i '/^from colab_leecher.downlader.mega import megadl$/d' colab_leecher/downlader/manager.py
sed -i '/^from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor$/d' colab_leecher/downlader/manager.py
sed -i '/^    is_mega,$/d' colab_leecher/downlader/manager.py
grep -n -A4 "elif is_mega(link):" colab_leecher/downlader/manager.py
sed -i '/^                elif is_mega(link):$/,+3d' colab_leecher/downlader/manager.py
sed -i '/^    elif is_mega(link):$/,+3d' colab_leecher/downlader/manager.py
sed -i '/^    is_mega,$/d' colab_leecher/utility/task_manager.py
sed -i '/^            elif is_mega(link):$/,+1d' colab_leecher/utility/task_manager.py
sed -i '/^def is_mega(link):$/,+2d' colab_leecher/utility/helper.py
sed -i '/^def to_bytes(value, unit):$/,/^def fileType/{/^def fileType/!d}' colab_leecher/utility/helper.py
sed -i '/Mega.nz Link/d; /mega.py/d' README.md
grep -rniI "mega\|to_bytes" colab_leecher/ README.md
```

Hasil yang benar: `grep` terakhir kosong. Periksa juga pemisah antarfungsi di `helper.py` (`grep -n -B2 "^def fileType" colab_leecher/utility/helper.py`).

```fish
git add colab_leecher/downlader/manager.py colab_leecher/utility/task_manager.py colab_leecher/utility/helper.py README.md
git commit -m "refactor: remove Mega integration" -m "Mega has strict limits and megatools is not available. Delete the downloader, its dispatch branches, the is_mega link detector, and the to_bytes helper that only it used."
```

### 4.12 Buang integrasi Terabox

```fish
git rm colab_leecher/downlader/terabox.py
sed -i '/^from colab_leecher.downlader.terabox import terabox_download$/d' colab_leecher/downlader/manager.py
sed -i '/^    is_terabox,$/d' colab_leecher/downlader/manager.py
grep -n -A10 "elif is_terabox(link):" colab_leecher/downlader/manager.py
sed -i '/^                elif is_terabox(link):$/,+9d' colab_leecher/downlader/manager.py
sed -i '/^    is_terabox,$/d' colab_leecher/utility/task_manager.py
sed -i '/^            elif is_terabox(link):$/,+1d' colab_leecher/utility/task_manager.py
sed -i '/^def is_terabox(link):$/,+2d' colab_leecher/utility/helper.py
sed -i '/terabox.py/d' README.md
grep -rniI "terabox\|1024tera\|aiohttp\|megadl" colab_leecher/ README.md
.venv/bin/python -c 'import colab_leecher.downlader.manager, colab_leecher.utility.task_manager; print("import OK")'
```

Hasil yang benar: `grep` kosong dan `import OK`. Rantai cabang `downloadManager` tinggal `is_google_drive`, `is_telegram`, `is_ytdl_link`, `else`.

```fish
git add colab_leecher/downlader/manager.py colab_leecher/utility/task_manager.py colab_leecher/utility/helper.py README.md
git commit -m "refactor: remove Terabox integration" -m "The downloader depended on a third-party API that fails frequently. Delete the downloader, its dispatch branch, and the is_terabox link detector. aiohttp was only used here and is already gone from requirements."
```

### 4.13 Tolak link Mega/Terabox sejak awal (`__main__.py`)

Di `handle_url`, tambahkan **tepat di atas** `BOT.SOURCE = temp_source` (indentasi 8 spasi):

```python
        unsupported = ("mega.nz", "terabox", "1024tera")
        if any(d in link for link in temp_source for d in unsupported):
            await message.reply_text(
                "<i>Mega and Terabox links are not supported in the local version.</i>",
                quote=True,
            )
            return

        BOT.SOURCE = temp_source
```

```fish
git add colab_leecher/__main__.py
git commit -m "feat(handler): reject unsupported Mega and Terabox links up front" -m "These links would otherwise fall through to aria2 and fail with a confusing error, after get_d_name had already run aria2c --dry-run on them. Reply with a clear message before any task starts, and keep the started flag so the user can simply resend a valid link."
```

### 4.14 Task harus dibatalkan saat aria2c gagal (`downlader/aria2.py`)

Sebelumnya kegagalan aria2c hanya dicatat ke log, lalu bot melaporkan `#LEECH_COMPLETE` dengan 0 file. Di akhir `aria2_Download`, ganti blok `if exit_code != 0:` dengan:

```python
    if exit_code != 0:
        if exit_code == 3:
            reason = "The resource was not found."
        elif exit_code == 9:
            reason = "Not enough disk space available."
        elif exit_code == 19:
            reason = "Name resolution failed."
        elif exit_code == 22:
            reason = "The server sent a bad or unexpected HTTP response (it may be blocking the connection)."
        elif exit_code == 24:
            reason = "HTTP authorization failed."
        else:
            reason = f"aria2c exited with code {exit_code}."
        logging.error(f"{reason} Link: {link}\nError: {error_output}")
        raise RuntimeError(reason)
```

`downloadManager` sudah menangkap `Exception` dan memanggil `cancelTask`, jadi task berhenti dengan pesan `#TASK_STOPPED` yang jelas.

```fish
git add colab_leecher/downlader/aria2.py
git commit -m "fix(aria2): abort the task when aria2c fails" -m "A non-zero exit code was only logged, so the bot kept going and reported a completed task with zero files. Raise a RuntimeError with a readable reason instead; downloadManager already turns exceptions into cancelTask, which stops the task and notifies the owner."
```

### 4.15 Nama file untuk media Telegram tanpa `file_name`

Foto Telegram tidak punya `file_name`, sehingga nama file menjadi string `None`. Di `downlader/telegram.py`, tambahkan di bawah `media_Identifier`:

```python
def media_Name(media, message) -> str:
    """Return the file name of a Telegram media object.

    Photos, voice notes, video notes and some videos carry no file name,
    so build one from the media type and its unique id instead of
    returning None.
    """
    name = getattr(media, "file_name", None)
    if name:
        return name

    default_ext = {
        "photo": ".jpg",
        "video": ".mp4",
        "audio": ".mp3",
        "voice": ".ogg",
        "video_note": ".mp4",
        "animation": ".mp4",
        "sticker": ".webp",
    }
    kind = next(
        (k for k in default_ext if getattr(message, k, None) is not None), "file"
    )
    return f"{kind}_{media.file_unique_id}{default_ext.get(kind, '')}"
```

Di `TelegramDownload`, ganti blok `name = media.file_name if hasattr(...) else "None"` dengan `name = media_Name(media, message)`. Di `get_d_name` (`manager.py`), ganti dua baris pada cabang `is_telegram` menjadi:

```python
        media, message = await media_Identifier(link)
        Messages.download_name = media_Name(media, message)
```

```fish
sed -i 's/import TelegramDownload, media_Identifier$/import TelegramDownload, media_Identifier, media_Name/' colab_leecher/downlader/manager.py
.venv/bin/python -c 'from types import SimpleNamespace as S; from colab_leecher.downlader.telegram import media_Name; p=S(file_unique_id="AQADxyz", file_name=None); print(media_Name(p, S(photo=p))); d=S(file_unique_id="u", file_name="a.txt.zip"); print(media_Name(d, S())); v=S(file_unique_id="vid1", file_name=None); print(media_Name(v, S(video=v)))'
```

Hasil yang benar: `photo_AQADxyz.jpg`, `a.txt.zip`, `video_vid1.mp4`.

```fish
git add colab_leecher/downlader/telegram.py colab_leecher/downlader/manager.py
git commit -m "fix(telegram): build a file name for media without one" -m "Photos have no file_name attribute, so hasattr() fell back to the literal string 'None', and media whose file_name is None (videos, voice notes, animations) would crash os.path.join. Add media_Name(), which returns the real name when present and otherwise builds one from the media type and file_unique_id with a sensible extension, and use it in both TelegramDownload and get_d_name."
```

### Belum dikerjakan (opsional)

- Hapus `main.py` (launcher Colab, sudah digantikan `run.sh`) dan `google_auth.py` (diganti saat [GDRIVE.md](GDRIVE.md) dikerjakan): `git rm main.py` lalu commit `chore: remove the Colab launcher`.
- Perbarui `README.md` ke cara pakai lokal (instalasi, `run.sh`, daftar fitur final).
