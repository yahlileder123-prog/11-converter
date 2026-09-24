"""
11 CONVERTER — window bootstrap (offline desktop app, Windows).

This module creates the Tk window, loads local settings, and builds the UI.
Conversion, metadata, and widgets live in the `converter11` package.

No network I/O. Settings and history are files next to this script
(or next to the .exe when frozen).
"""

import os
import sys
from datetime import datetime
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD
import ctypes


from converter11.config_io import load_app_state, save_config
from converter11.ffmpeg_runtime import configure_ffmpeg
from converter11.constants import (
    ACCENT_DEFAULT,
    APPEARANCE_FILE,
    AUDIO_EXT,
    AUDIO_SETTINGS_FILE,
    COLOR_CONFIG_FILE,
    CONFIG_FILE,
    LANGUAGE_FILE,
    LOCAL_LOG_FILE,
    VIDEO_EXT,
)
from converter11.strings import STRINGS
from converter11.ui_palette import palette
from converter11.ctk_helpers import wire_entry_text_selection
from converter11.win_geometry import (
    fit_window_to_work_area,
    schedule_clamp_toplevel_to_work_area,
    windows_apply_native_chrome,
    windows_set_dpi_awareness,
)
from converter11.ui_motion import animate_progress
from converter11.history_view import rebuild_history_page
from converter11.name_pattern_ui import (
    on_pattern_advanced_toggle as _on_pattern_advanced_toggle,
    pat_labels as _pat_labels,
    pattern_sep_cmd as _pattern_sep_cmd,
    pattern_slot_cmd as _pattern_slot_cmd,
    rebuild_pattern_from_builder as _rebuild_pattern_from_builder,
    save_name_pattern as _save_name_pattern,
    update_pattern_preview as _update_pattern_preview,
)
from converter11.track_queue import (
    finalize_track_selection as _finalize_track_selection,
    norm_path_key as _norm_path_key,
    refresh_track_queue_table,
    update_paths_ui as update_ui_paths,
)
from converter11.ui_layout import apply_all_texts, apply_layout_direction
from converter11.ui_build_music_page import build_music_page
from converter11.ui_build_settings_page import build_settings_page
from converter11.ui_build_sidebar import build_sidebar
from converter11.ui_navigation import show_settings_view
from converter11.ui_theme import (
    apply_theme,
    set_nav_active,
)


def _app_base_directory() -> str:
    """Directory containing the app (exe folder or project root beside the package)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def _maximize_main_window() -> None:
    """Maximize the main window (Windows: full work area). No network."""
    try:
        if sys.platform == "win32":
            app.state("zoomed")
        else:
            try:
                app.attributes("-zoomed", True)
            except Exception:
                pass
    except Exception:
        pass


def _redact_private_paths(message: str) -> str:
    """Keep logs useful without writing the Windows user folder."""
    try:
        home = os.path.expanduser("~")
        if home:
            for variant in (home, home.replace("\\", "/"), home.replace("/", "\\")):
                if variant:
                    message = message.replace(variant, "~")
    except Exception:
        pass
    if len(message) > 2000:
        message = message[:2000] + "…"
    return message


def _append_local_log(message: str) -> None:
    """Append one line to a local log file (no network). Fails silently if not writable."""
    try:
        path = os.path.join(_app_base_directory(), LOCAL_LOG_FILE)
        with open(path, "a", encoding="utf-8") as fp:
            fp.write(
                f"{datetime.now().isoformat(timespec='seconds')} {_redact_private_paths(message)}\n"
            )
    except OSError:
        pass


last_export_path = "NOT SET"
current_source_path = "NOT SET"
selected_files_globally = []
brand_color = ACCENT_DEFAULT
is_converting = False
current_appearance = "dark"
history_entries: list[dict] = []
_active_main_tab = "music"

queue_sort_column = "title"
queue_sort_reverse = False
history_sort_column = "logged_at"
history_sort_reverse = True
history_dirty = True

# Cache for queue metadata to keep UI instant (path_key -> (mtime, meta_dict))
queue_meta_cache: dict[str, tuple[float, dict]] = {}

# Paths excluded from conversion (normcase keys); checkbox off = in this set.
queue_excluded_from_convert: set[str] = set()

ui_lang = "en"

audio_settings: dict = {}


load_app_state(sys.modules[__name__])
if not (brand_color.startswith("#") and len(brand_color) >= 4):
    brand_color = ACCENT_DEFAULT


def t(key: str, **kwargs) -> str:
    s = STRINGS.get(ui_lang, STRINGS["en"]).get(key) or STRINGS["en"].get(key, key)
    if kwargs:
        try:
            return s.format(**kwargs)
        except (KeyError, ValueError):
            return s
    return s


def layout_rtl() -> bool:
    return ui_lang == "he"


def _pct(part: int, whole: int) -> int:
    if whole <= 0:
        return 0
    return min(100, max(0, round(100 * part / whole)))


_progress_motion = {"shown": 0.0, "target": 0.0, "id": None}


def sync_idle_progress_labels() -> None:
    """When idle: Ready line with 0% / 100% and queue count (not used while converting)."""
    if is_converting:
        return
    try:
        progress_label.pack_forget()
        eta_label.pack_forget()
    except Exception:
        pass
    animate_progress(app, progress_bar, _progress_motion, 0, snap=True)


def update_progress(text, progress_val, eta_text=""):
    def _apply():
        try:
            if not progress_label.winfo_manager():
                progress_label.pack(fill="x")
                progress_bar.pack_forget()
                progress_bar.pack(fill="x", pady=(6, 0))
                eta_label.pack(fill="x")
        except Exception:
            pass
        progress_label.configure(text=text)
        eta_label.configure(text=eta_text)
        animate_progress(app, progress_bar, _progress_motion, progress_val)

    app.after(0, _apply)


configure_ffmpeg()

# Allow ui_theme / ui_dialogs to reach this module's globals (widgets, t, save_config, …).
sys.modules["converter_main"] = sys.modules[__name__]

# Build the window (widgets live in converter11.ui_build_*).
windows_set_dpi_awareness()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)

app = TkinterDnD.Tk()
app.title(t("window_title"))
app.geometry("1120x800")
app.minsize(960, 680)

# CustomTkinter DPI/scaling expects CTk-like window helpers, but we run on TkinterDnD.Tk().
# Provide no-op shims to avoid internal scaling callback crashes (can manifest as "transparent" redraws).
if not hasattr(app, "block_update_dimensions_event"):
    app.block_update_dimensions_event = lambda *a, **k: None  # type: ignore[attr-defined]
if not hasattr(app, "unblock_update_dimensions_event"):
    app.unblock_update_dimensions_event = lambda *a, **k: None  # type: ignore[attr-defined]

_ui = palette(current_appearance)

def _initial_window_placement() -> None:
    fit_window_to_work_area(app)
    schedule_clamp_toplevel_to_work_area(app)


app.after(80, _initial_window_placement)
app.after(120, lambda: windows_apply_native_chrome(app, dark=(current_appearance == "dark")))
app.after(450, lambda: schedule_clamp_toplevel_to_work_area(app))

app.resizable(True, True)

try:
    icon_files = [f for f in os.listdir() if f.endswith(".ico")]
    if icon_files:
        app.after(200, lambda: app.iconbitmap(icon_files[0]))
    myappid = "converter11.audio.ui"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

app.configure(bg=_ui["window"])

main_frame = ctk.CTkFrame(app, fg_color=_ui["window"], corner_radius=0)
main_frame.pack(fill="both", expand=True)

view_home = ctk.CTkFrame(main_frame, fg_color=_ui["window"])
view_home.pack(fill="both", expand=True)

_m = sys.modules[__name__]
_m.main_frame = main_frame
_m.view_home = view_home

build_sidebar(_m)
build_music_page(_m)
build_settings_page(_m)


def _set_language(lang: str):
    global ui_lang
    if lang not in ("he", "en"):
        return
    ui_lang = lang
    save_config(LANGUAGE_FILE, lang)
    apply_all_texts()
    apply_theme(current_appearance)
    apply_layout_direction()
    app.after(0, _maximize_main_window)
    app.after(250, lambda: schedule_clamp_toplevel_to_work_area(app))


lang_btn_he.configure(command=lambda: _set_language("he"))
lang_btn_en.configure(command=lambda: _set_language("en"))

more_settings_btn.configure(command=show_settings_view)
sidebar_settings_btn.configure(command=show_settings_view)

set_nav_active("music")
apply_theme(current_appearance)
apply_all_texts()
apply_layout_direction()

wire_entry_text_selection(url_entry)
wire_entry_text_selection(output_folder_entry)
wire_entry_text_selection(audio_pattern_entry)

app.bind("<Map>", lambda e: schedule_clamp_toplevel_to_work_area(app))
try:
    app.bind("<Activate>", lambda e: schedule_clamp_toplevel_to_work_area(app))
except Exception:
    pass

app.mainloop()
