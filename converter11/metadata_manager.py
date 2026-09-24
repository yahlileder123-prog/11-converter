"""Read track metadata (TinyTag) and write export tags (mutagen)."""

import os
from datetime import datetime
from pathlib import Path

from converter11.constants import EXT_KIND_LABEL

try:
    from tinytag import TinyTag
except Exception:
    TinyTag = None

try:
    from mutagen import File as MutagenFile
except Exception:
    MutagenFile = None


def _file_format_label(path: str) -> str:
    suf = Path(path).suffix.lower()
    if not suf:
        return "—"
    return EXT_KIND_LABEL.get(suf, suf.upper().lstrip(".") or "—")


def read_audio_meta(path: str) -> dict:
    base = os.path.basename(path)
    stem, _ext = os.path.splitext(base)
    title = stem
    artist = "—"
    album = "—"
    duration = "—"
    duration_seconds = -1.0
    bpm = "—"
    musical_key = "—"
    try:
        st = os.stat(path)
        file_date = datetime.fromtimestamp(st.st_ctime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        file_date = "—"
    if TinyTag is not None:
        try:
            tt = TinyTag.get(path)
            if tt.title and str(tt.title).strip():
                title = str(tt.title).strip()
            if tt.artist and str(tt.artist).strip():
                artist = str(tt.artist).strip()
            if tt.album and str(tt.album).strip():
                album = str(tt.album).strip()
            if tt.duration:
                duration_seconds = float(tt.duration)
                m, s = divmod(int(tt.duration), 60)
                duration = f"{m}:{s:02d}"
            bpm_val = getattr(tt, "extra", None) or {}
            if isinstance(bpm_val, dict):
                for k in ("tbpm", "BPM", "bpm"):
                    if k in bpm_val and bpm_val[k]:
                        bpm = str(bpm_val[k]).split(".")[0]
                        break
                for k in ("TKEY", "INITIALKEY", "KEY"):
                    if k in bpm_val and bpm_val[k]:
                        musical_key = str(bpm_val[k]).strip()
                        break
        except Exception:
            pass
    return {
        "path": path,
        "filename": base,
        "title": title or stem,
        "artist": artist,
        "album": album,
        "format": _file_format_label(path),
        "duration": duration,
        "duration_seconds": duration_seconds,
        "bpm": bpm,
        "key": musical_key,
        "file_date": file_date,
    }


def embed_mutagen_tags(
    out_path: str, meta: dict, target: str, *, embed_metadata: bool
) -> None:
    if not embed_metadata or MutagenFile is None:
        return
    title = (meta.get("title") or "").strip()
    artist = (meta.get("artist") or "").strip()
    album = (meta.get("album") or "").strip()
    try:
        if target == "mp3":
            from mutagen.easyid3 import EasyID3

            try:
                f = EasyID3(out_path)
            except Exception:
                m = MutagenFile(out_path)
                if m is None:
                    return
                try:
                    m.add_tags()
                except Exception:
                    return
                try:
                    f = EasyID3(out_path)
                except Exception:
                    return
            if title:
                f["title"] = title
            if artist:
                f["artist"] = artist
            if album:
                f["album"] = album
            f.save(out_path)
        elif target == "flac":
            from mutagen.flac import FLAC

            f = FLAC(out_path)
            if title:
                f["title"] = title
            if artist:
                f["artist"] = artist
            if album:
                f["album"] = album
            bpm = meta.get("bpm")
            if bpm and str(bpm) != "—":
                f["bpm"] = str(bpm)
            ky = meta.get("key")
            if ky and str(ky) != "—":
                try:
                    f["key"] = str(ky)
                except Exception:
                    pass
            f.save()
        elif target == "m4a":
            from mutagen.mp4 import MP4

            f = MP4(out_path)
            if title:
                f["\xa9nam"] = [title]
            if artist:
                f["\xa9ART"] = [artist]
            if album:
                f["\xa9alb"] = [album]
            bpm = meta.get("bpm")
            if bpm and str(bpm) != "—":
                try:
                    f["tmpo"] = [int(float(str(bpm).split(".")[0]))]
                except Exception:
                    pass
            f.save()
    except Exception:
        pass
