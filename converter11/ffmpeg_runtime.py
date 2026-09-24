"""Locate FFmpeg shipped with the app, or fall back to PATH."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

from pydub import AudioSegment

_configured: str | None = None


def _exe_name(tool: str) -> str:
    return f"{tool}.exe" if os.name == "nt" else tool


def _candidate_dirs() -> list[Path]:
    dirs: list[Path] = []
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        dirs.extend(
            (
                exe_dir,
                exe_dir / "_internal",
                exe_dir / "ffmpeg",
                exe_dir / "_internal" / "ffmpeg",
            )
        )
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            dirs.append(Path(meipass))
    else:
        root = Path(__file__).resolve().parents[1]
        dirs.extend((root / "vendor" / "ffmpeg", root))
    return dirs


def resolve_tool(tool: str) -> str | None:
    name = _exe_name(tool)
    for folder in _candidate_dirs():
        trial = folder / name
        if trial.is_file():
            return str(trial)
    return shutil.which(tool)


def configure_ffmpeg() -> str | None:
    """Point pydub at bundled FFmpeg and put it on PATH. Safe to call often."""
    global _configured
    if _configured and Path(_configured).is_file():
        return _configured

    ffmpeg = resolve_tool("ffmpeg")
    if not ffmpeg:
        _configured = None
        return None

    folder = str(Path(ffmpeg).resolve().parent)
    path = os.environ.get("PATH", "")
    if folder.lower() not in path.lower():
        os.environ["PATH"] = folder + os.pathsep + path

    AudioSegment.converter = ffmpeg
    probe = resolve_tool("ffprobe")
    if probe:
        AudioSegment.ffprobe = probe

    _configured = ffmpeg
    return ffmpeg


def ffmpeg_available() -> bool:
    return configure_ffmpeg() is not None
