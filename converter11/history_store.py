"""Append-only track history list persisted as JSON (last 500 entries)."""

import json
import os
from datetime import datetime

from converter11.constants import HISTORY_FILE
from converter11.metadata_manager import read_audio_meta
from converter11.security_utils import is_allowed_media_file
from converter11.ui_context import main_module


def _save_history_to_disk() -> None:
    m = main_module()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(m.history_entries[-500:], f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def clear_history() -> None:
    m = main_module()
    m.history_entries = []
    m.history_dirty = True
    _save_history_to_disk()


def record_files_to_history(paths: list[str]) -> None:
    m = main_module()
    # Rebuild the history UI only when new rows are added (keeps screen switches instant).
    m.history_dirty = True
    allow_video = bool(m.audio_settings.get("allow_video_extract"))
    for path in paths:
        if not os.path.isfile(path):
            continue
        if not is_allowed_media_file(path, allow_video):
            m._append_local_log(f"history skip (header): {path!r}")
            continue
        meta = read_audio_meta(path)
        meta["logged_at"] = datetime.now().isoformat(timespec="seconds")
        m.history_entries.append(meta)
    if len(m.history_entries) > 500:
        m.history_entries = m.history_entries[-500:]
    _save_history_to_disk()
