"""Header / magic-byte checks for media files (read-only, no execution)."""

import os
from pathlib import Path

from converter11.constants import AUDIO_EXT, MEDIA_HEADER_BYTES, VIDEO_EXT


def read_file_header(path: str, max_len: int = MEDIA_HEADER_BYTES) -> bytes:
    try:
        with open(path, "rb") as fp:
            return fp.read(max_len)
    except OSError:
        return b""


def sniff_media_container(head: bytes) -> str | None:
    """Return a coarse container id if bytes look like supported media; else None."""
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


def media_kind_matches_suffix(suffix: str, kind: str, allow_video: bool) -> bool:
    """True if sniffed container matches the file extension and settings."""
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


def allowed_file_suffixes(allow_video: bool) -> tuple[str, ...]:
    if allow_video:
        return AUDIO_EXT + VIDEO_EXT
    return AUDIO_EXT


def is_allowed_media_file(path: str, allow_video: bool) -> bool:
    """
    Read-only header check: reject executables / archives mislabeled as media.
    Does not execute or fully decode the file.
    """
    if not path or not os.path.isfile(path):
        return False
    suffix = Path(path).suffix.lower()
    if suffix not in allowed_file_suffixes(allow_video):
        return False
    head = read_file_header(path)
    kind = sniff_media_container(head)
    if kind is None:
        return False
    return media_kind_matches_suffix(suffix, kind, allow_video)
