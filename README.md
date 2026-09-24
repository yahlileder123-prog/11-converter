# 11 CONVERTER

A Windows desktop **batch audio converter**. Everything stays on your machine — no server, no account, no network.

Drop files in, pick a format and output folder, then convert.

---

## Download (Windows)

Get the installer from the latest [Release](https://github.com/yahlileder123-prog/11-converter/releases/latest).

1. Download `11_CONVERTER_Setup.exe`
2. Run it (no Administrator required)
3. Open **11 CONVERTER** from the Start menu

Python and FFmpeg are already inside the installer. You do not install them separately.

---

## What it does

1. Drag files (or a folder) in, or click **Add**.
2. Choose an export format and destination folder.
3. Click **Convert**.

The app reads metadata (artist, title, album, BPM, key), names files from a pattern you choose, and writes the new format.

**Formats:** WAV, MP3, FLAC, AIFF, M4A, OGG  
**Optional:** extract audio from video (MP4, MKV, MOV, WebM)  
**UI:** English / Hebrew · light / dark

---

## Run from source (developers)

You need **Python 3.11+**. For source runs only, also put **FFmpeg** on PATH — the installer build bundles it for you.

```text
pip install -r requirements.txt
python main.py
```

```text
python verify_converter.py
```

In Cursor / VS Code, the **▶ 11 CONVERTER** launch config runs `main.py`.

---

## Project layout

| Path | Role |
| --- | --- |
| `main.py` | Entry point — start here |
| `app.py` | Window bootstrap |
| `converter11/` | Conversion, queue, history, UI |
| `requirements.txt` | Python dependencies |
| `11_converter.spec` | PyInstaller spec |
| `packaging/` | Installer (Inno Setup) + FFmpeg notice |
| `verify_converter.py` | Smoke tests without a GUI |

Inside `converter11`:

- `audio_engine.py` / `conversion_runner.py` — background export via FFmpeg
- `ffmpeg_runtime.py` — finds bundled FFmpeg next to the app
- `security_utils.py` — header sniff (dropped files are never executed)
- `metadata_manager.py` — tags
- `track_queue.py` — track list on the main page
- `strings.py` — all UI copy (English + Hebrew)
- `ui_build_*.py` — sidebar, music, settings

---

## Local files the app creates

Settings stay **next to the app** (or under the installed folder), not in the cloud:

- `audio_settings.json` — sample rate, bit depth, name pattern
- `track_history.json` — files you have loaded
- `language.txt` / `appearance.txt` — language and theme
- `config.txt` — export folder
- `converter11.log` — local log (private paths redacted)

These are listed in `.gitignore` and are not committed.

---

## Privacy

No files, metadata, or telemetry are sent anywhere.  
Output is always a **new** file in the folder you chose.

---

## Build the installer

See [`PACKAGING.md`](PACKAGING.md).
