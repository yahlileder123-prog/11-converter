"""Export / naming helpers for audio conversion (no GUI)."""

import os

from pydub import AudioSegment

from converter11.ffmpeg_runtime import configure_ffmpeg, ffmpeg_available

configure_ffmpeg()


def sanitize_filename(name: str) -> str:
    bad = '<>:"/\\|?*'
    for c in bad:
        name = name.replace(c, "_")
    name = name.strip().strip(".")
    return name or "track"


def fill_export_filename(pattern: str, meta: dict, stem_fallback: str) -> str:
    repl = {
        "artist": (meta.get("artist") or "").strip() or "Unknown",
        "title": (meta.get("title") or "").strip() or stem_fallback,
        "album": (meta.get("album") or "").strip(),
        "bpm": (meta.get("bpm") or "").replace("—", "").strip(),
        "key": (meta.get("key") or "").replace("—", "").strip(),
    }
    s = pattern
    for k, v in repl.items():
        s = s.replace("{" + k + "}", str(v))
    s = s.strip()
    return s or stem_fallback


def unique_output_path(directory: str, base: str, ext: str) -> str:
    base = sanitize_filename(base)
    trial = os.path.join(directory, f"{base}.{ext}")
    if not os.path.exists(trial):
        return trial
    for n in range(2, 10000):
        trial = os.path.join(directory, f"{base}_{n}.{ext}")
        if not os.path.exists(trial):
            return trial
    return os.path.join(directory, f"{base}.{ext}")


def pcm_codec(bit_depth: str, aiff: bool) -> str:
    if aiff:
        return {
            "16": "pcm_s16be",
            "24": "pcm_s24be",
            "32f": "pcm_f32be",
        }.get(bit_depth, "pcm_s16be")
    return {
        "16": "pcm_s16le",
        "24": "pcm_s24le",
        "32f": "pcm_f32le",
    }.get(bit_depth, "pcm_s16le")


def export_audio_segment(
    audio: AudioSegment,
    out_path: str,
    target: str,
    sample_rate: int,
    bit_depth: str,
    *,
    aac_bitrate_kbps: int,
) -> None:
    if audio.frame_rate != sample_rate:
        audio = audio.set_frame_rate(sample_rate)
    if target == "mp3":
        params = ["-c:a", "libmp3lame", "-b:a", "320k", "-ar", str(sample_rate)]
        audio.export(out_path, format="mp3", parameters=params)
        return
    if target == "wav":
        codec = pcm_codec(bit_depth, False)
        audio.export(
            out_path,
            format="wav",
            parameters=["-acodec", codec, "-ar", str(sample_rate)],
        )
        return
    if target in ("aiff", "aif"):
        codec = pcm_codec(bit_depth, True)
        audio.export(
            out_path,
            format="aiff",
            parameters=["-acodec", codec, "-ar", str(sample_rate)],
        )
        return
    if target == "flac":
        audio.export(out_path, format="flac", parameters=["-ar", str(sample_rate)])
        return
    if target == "m4a":
        br = int(aac_bitrate_kbps or 256)
        audio.export(
            out_path,
            format="ipod",
            parameters=["-c:a", "aac", "-b:a", f"{br}k", "-ar", str(sample_rate)],
        )
        return
    audio.export(out_path, format=target)
