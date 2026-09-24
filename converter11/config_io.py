"""Persisted app settings beside the script (or next to the frozen exe)."""

import json
import os
from types import ModuleType

from converter11.constants import (
    APPEARANCE_FILE,
    AUDIO_SETTINGS_DEFAULT,
    AUDIO_SETTINGS_FILE,
    COLOR_CONFIG_FILE,
    CONFIG_FILE,
    HISTORY_FILE,
    LANGUAGE_FILE,
)
from converter11.naming import migrate_audio_name_pattern
from converter11.ui_context import main_module


def save_config(path: str, data: str) -> None:
    with open(path, "w") as f:
        f.write(data)


def load_app_state(app_mod: ModuleType) -> None:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            app_mod.last_export_path = f.read().strip()
    if os.path.exists(COLOR_CONFIG_FILE):
        with open(COLOR_CONFIG_FILE, "r") as f:
            raw = f.read().strip()
            if raw.startswith("#") and len(raw) >= 4:
                app_mod.brand_color = raw
    if os.path.exists(APPEARANCE_FILE):
        with open(APPEARANCE_FILE, "r") as f:
            raw = f.read().strip().lower()
            if raw in ("light", "dark"):
                app_mod.current_appearance = raw
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                app_mod.history_entries = json.load(f)
            if not isinstance(app_mod.history_entries, list):
                app_mod.history_entries = []
        except (json.JSONDecodeError, OSError):
            app_mod.history_entries = []
    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                raw = f.read().strip().lower()
                if raw in ("he", "en"):
                    app_mod.ui_lang = raw
        except OSError:
            pass
    app_mod.audio_settings = dict(AUDIO_SETTINGS_DEFAULT)
    if os.path.exists(AUDIO_SETTINGS_FILE):
        try:
            with open(AUDIO_SETTINGS_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                app_mod.audio_settings = {**AUDIO_SETTINGS_DEFAULT, **loaded}
        except (json.JSONDecodeError, OSError):
            pass
    migrate_audio_name_pattern(app_mod.audio_settings)


def save_audio_settings_disk() -> None:
    m = main_module()
    try:
        with open(AUDIO_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(m.audio_settings, f, ensure_ascii=False, indent=2)
    except OSError:
        pass
