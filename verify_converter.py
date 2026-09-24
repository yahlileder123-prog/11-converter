# -*- coding: utf-8 -*-
"""
Smoke checks: parse `app.py`, then test naming and media-header logic.

The implementations here should stay in sync with:
  converter11.naming, converter11.audio_engine, converter11.security_utils
"""
from __future__ import annotations

import ast
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "app.py"

VALID_NAME_PARTS = {"artist", "title", "album", "bpm", "key"}

AUDIO_EXT = (".wav", ".mp3", ".flac", ".aiff", ".aif", ".m4a", ".ogg")
VIDEO_EXT = (".mp4", ".mkv", ".mov", ".webm", ".m4v")


def _sniff_media_container(head: bytes) -> str | None:
    if len(head) < 12:
        return None
    if head[:2] == b"MZ":
        return None
    if head[:4] == b"\x7fELF":
        return None
    if head[:4] == b"%PDF":
        return None
    if head[:2] == b"PK" and len(head) >= 4 and head[2:4] in (b"\x03\x04", b"\x05\x06"):
        return None
    if head.startswith(b"#!"):
        return None
    if head[:4] == b"RIFF" and len(head) >= 12 and head[8:12] == b"WAVE":
        return "wav"
    if head[:4] == b"fLaC":
        return "flac"
    if head[:3] == b"ID3":
        return "mp3"
    if head[0] == 0xFF and (head[1] & 0xE0) == 0xE0:
        return "mp3"
    if head[:4] == b"OggS":
        return "ogg"
    if len(head) >= 12 and head[4:8] == b"ftyp":
        return "isobmff"
    if head[:4] == b"\x1a\x45\xdf\xa3":
        return "matroska"
    if head[:4] == b"FORM" and len(head) >= 12 and head[8:12] in (b"AIFF", b"AIFC"):
        return "aiff"
    if len(head) >= 8 and head[4:8] in (
        b"moov",
        b"mdat",
        b"wide",
        b"free",
        b"skip",
        b"junk",
        b"pnot",
    ):
        return "qt_atom"
    return None


def _media_kind_matches_suffix(suffix: str, kind: str, allow_video: bool) -> bool:
    suffix = suffix.lower()
    if suffix in AUDIO_EXT:
        if suffix == ".wav":
            return kind in ("wav", "mp3", "flac", "aiff")
        if suffix == ".mp3":
            return kind == "mp3"
        if suffix == ".flac":
            return kind == "flac"
        if suffix in (".aiff", ".aif"):
            return kind == "aiff"
        if suffix == ".m4a":
            return kind in ("isobmff", "qt_atom")
        if suffix == ".ogg":
            return kind == "ogg"
        return False
    if allow_video and suffix in VIDEO_EXT:
        if suffix in (".mp4", ".m4v"):
            return kind in ("isobmff", "qt_atom")
        if suffix in (".mkv", ".webm"):
            return kind == "matroska"
        if suffix == ".mov":
            return kind in ("isobmff", "qt_atom")
        return False
    return False


def _build_name_pattern_string(parts: list, sep: str) -> str:
    tags = []
    for p in parts:
        if p != "skip" and p in VALID_NAME_PARTS:
            tags.append("{" + p + "}")
    return sep.join(tags) if tags else "{title}"


def _infer_sep_from_pattern(raw: str) -> str:
    valid_ms = []
    for m in re.finditer(r"\{(\w+)\}", raw):
        if m.group(1) in VALID_NAME_PARTS:
            valid_ms.append(m)
    if len(valid_ms) < 2:
        return " - "
    gap = raw[valid_ms[0].end() : valid_ms[1].start()]
    return gap if gap.strip() else " - "


def _sanitize_filename(name: str) -> str:
    bad = '<>:"/\\|?*'
    for c in bad:
        name = name.replace(c, "_")
    name = name.strip().strip(".")
    return name or "track"


def _fill_export_filename(pattern: str, meta: dict, stem_fallback: str) -> str:
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


def test_syntax_ast() -> None:
    src = APP.read_text(encoding="utf-8")
    ast.parse(src)


def test_py_compile() -> None:
    files = [APP, ROOT / "main.py", *sorted((ROOT / "converter11").glob("*.py"))]
    subprocess.run(
        [sys.executable, "-m", "py_compile", *[str(p) for p in files]],
        check=True,
    )


def test_name_pattern_builder() -> None:
    assert _build_name_pattern_string(
        ["artist", "title", "skip", "skip"], " - "
    ) == "{artist} - {title}"
    assert _build_name_pattern_string(["skip", "skip", "skip", "skip"], "_") == "{title}"
    assert _build_name_pattern_string(["bpm", "key", "skip", "skip"], " · ") == "{bpm} · {key}"


def test_infer_sep() -> None:
    assert _infer_sep_from_pattern("{artist} - {title}") == " - "
    assert _infer_sep_from_pattern("{artist}_{title}") == "_"
    assert _infer_sep_from_pattern("{title}") == " - "


def test_sanitize() -> None:
    assert "?" not in _sanitize_filename('a?b')
    assert _sanitize_filename("   ") == "track"


def test_fill_export() -> None:
    meta = {"artist": "A", "title": "T", "album": "", "bpm": "120", "key": "8A"}
    assert _fill_export_filename("{artist} - {title}", meta, "x") == "A - T"
    assert _fill_export_filename("{title}", {}, "stem") == "stem"


def test_media_magic_sniff() -> None:
    h = bytearray(64)
    h[:4], h[8:12] = b"RIFF", b"WAVE"
    assert _sniff_media_container(bytes(h)) == "wav"
    assert _sniff_media_container(b"fLaC" + b"\x00" * 60) == "flac"
    assert _sniff_media_container(b"MZ" + b"\x00" * 62) is None
    assert _sniff_media_container(b"\x1a\x45\xdf\xa3" + b"\x00" * 60) == "matroska"
    h2 = bytearray(64)
    h2[4:8] = b"ftyp"
    assert _sniff_media_container(bytes(h2)) == "isobmff"
    h3 = bytearray(64)
    h3[4:8] = b"mdat"
    assert _sniff_media_container(bytes(h3)) == "qt_atom"


def test_media_kind_matches_suffix() -> None:
    assert _media_kind_matches_suffix(".wav", "wav", False) is True
    assert _media_kind_matches_suffix(".wav", "mp3", False) is True
    assert _media_kind_matches_suffix(".mp3", "wav", False) is False
    assert _media_kind_matches_suffix(".m4a", "isobmff", False) is True
    assert _media_kind_matches_suffix(".m4a", "qt_atom", False) is True
    assert _media_kind_matches_suffix(".mp4", "isobmff", False) is False
    assert _media_kind_matches_suffix(".mp4", "isobmff", True) is True
    assert _media_kind_matches_suffix(".mp4", "qt_atom", True) is True


def test_pe_stripped_wav_rejected_on_disk() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "fake.wav"
        p.write_bytes(b"MZ" + b"\x00" * 120)
        head = p.read_bytes()[:64]
        assert _sniff_media_container(head) is None


def main() -> None:
    assert APP.is_file(), f"Missing {APP}"
    test_syntax_ast()
    test_py_compile()
    test_name_pattern_builder()
    test_infer_sep()
    test_sanitize()
    test_fill_export()
    test_media_magic_sniff()
    test_media_kind_matches_suffix()
    test_pe_stripped_wav_rejected_on_disk()
    print("verify_converter: all checks passed.")


if __name__ == "__main__":
    main()
