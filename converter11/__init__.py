"""
11 CONVERTER — app package (no network).

`app.py` builds the window and registers itself as `converter_main`.
Modules in this package then read that live app via `ui_context.main_module()`.

What lives where
----------------
Settings & text
    constants.py      File names, audio defaults, allowed extensions
    strings.py        Hebrew + English UI copy
    config_io.py      Load/save config beside the app (not in the cloud)

Convert & files
    audio_engine.py       FFmpeg / pydub export and filename sanitizing
    ffmpeg_runtime.py     Bundled FFmpeg next to the installed app
    conversion_runner.py  Background batch convert (thread)
    metadata_manager.py   Read tags (TinyTag), write tags (mutagen)
    naming.py             Export filename pattern
    security_utils.py     Magic-byte sniff — never execute dropped files
    path_utils.py         Path display helpers

Queue & history
    track_queue.py        Music-page file list, drag-and-drop
    history_store.py      Local JSON history (last 500)
    history_view.py       History page

UI
    ui_build_*.py         Sidebar, Music, Settings pages
    ui_theme.py / ui_palette.py / ui_layout.py / ui_navigation.py
    ui_dialogs.py / ui_help_dialogs.py / name_pattern_ui.py
    table_widgets.py      Sortable tables
    win_geometry.py       Windows DPI / work-area
"""

__all__ = [
    "config_io",
    "constants",
    "strings",
    "security_utils",
    "metadata_manager",
    "name_pattern_ui",
    "audio_engine",
    "audio_settings_handlers",
    "conversion_runner",
    "history_store",
    "history_view",
    "path_utils",
    "ui_palette",
    "ctk_helpers",
    "win_geometry",
    "table_widgets",
    "track_queue",
    "ui_context",
    "ui_theme",
    "ui_layout",
    "ui_help_dialogs",
    "ui_navigation",
    "ui_build_sidebar",
    "ui_build_music_page",
    "ui_build_settings_page",
    "ui_dialogs",
]
