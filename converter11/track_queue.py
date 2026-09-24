"""Track list queue: add/remove files, sortable table, window title, drag-and-drop."""

import os
from collections import Counter
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from converter11.constants import EXT_KIND_LABEL
from converter11.history_store import record_files_to_history
from converter11.metadata_manager import read_audio_meta
from converter11.path_utils import shorten_path
from converter11.security_utils import (
    allowed_file_suffixes as build_allowed_suffix_tuple,
    is_allowed_media_file,
)
from converter11.table_widgets import (
    pack_sortable_header_row,
    pack_table_row_cells,
    queue_sort_tuple,
)
from converter11.ui_context import main_module
from converter11.ui_dialogs import open_track_selection_dialog
from converter11.ui_motion import bind_surface_hover
from converter11.ui_palette import get_total_size, palette


def truncate_window_title(text: str, max_len: int = 220) -> str:
    one = text.replace("\r", " ").replace("\n", " ")
    if len(one) <= max_len:
        return one
    return one[: max(0, max_len - 1)] + "…"


def norm_path_key(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))


def read_audio_meta_cached(path: str) -> dict:
    """Cache metadata reads (TinyTag can be slow, especially on navigation/redraw)."""
    m = main_module()
    key = norm_path_key(path)
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        mtime = -1.0
    cache = getattr(m, "queue_meta_cache", None)
    if isinstance(cache, dict):
        hit = cache.get(key)
        if hit and hit[0] == mtime:
            return hit[1]
    meta = read_audio_meta(path)
    if isinstance(cache, dict):
        cache[key] = (mtime, meta)
    return meta


def current_allowed_suffixes() -> tuple[str, ...]:
    m = main_module()
    return build_allowed_suffix_tuple(bool(m.audio_settings.get("allow_video_extract")))


def prune_queue_exclude_set() -> None:
    m = main_module()
    if not m.selected_files_globally:
        m.queue_excluded_from_convert.clear()
        return
    ok = {norm_path_key(p) for p in m.selected_files_globally}
    m.queue_excluded_from_convert.intersection_update(ok)


def sync_output_folder_entry() -> None:
    m = main_module()
    if m.last_export_path == "NOT SET":
        txt = ""
    else:
        txt = m.last_export_path
    m.output_folder_entry.configure(state="normal")
    m.output_folder_entry.delete(0, "end")
    m.output_folder_entry.insert(0, txt)
    m.output_folder_entry.configure(state="readonly")


def file_kind_label(path: str) -> str:
    m = main_module()
    suf = Path(path).suffix.lower()
    if not suf:
        return m.t("file_kind_unknown")
    return EXT_KIND_LABEL.get(
        suf, suf.upper().lstrip(".") or m.t("file_kind_unknown")
    )


def selection_kinds_summary() -> str:
    """Human-readable file-type line for badge and sidebar (matches title-bar logic)."""
    m = main_module()
    paths = m.selected_files_globally
    if not paths:
        return ""
    if len(paths) == 1:
        return file_kind_label(paths[0])
    kinds = [file_kind_label(p) for p in paths]
    cnt = Counter(kinds)
    return " · ".join(
        f"{label} ×{c}"
        for label, c in sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
    )


def sync_sidebar_format_panel() -> None:
    """Sidebar: source file type(s) in queue + chosen export format (always visible)."""
    m = main_module()
    if not hasattr(m, "sidebar_file_kinds"):
        return
    kinds = selection_kinds_summary()
    kinds_display = kinds if kinds else m.t("sidebar_no_source_yet")
    try:
        export_fmt = m.format_option.get()
    except Exception:
        export_fmt = "—"
    text = (
        f"{m.t('sidebar_source_prefix')}: {kinds_display}\n"
        f"{m.t('sidebar_export_prefix')}: {export_fmt}"
    )
    m.sidebar_file_kinds.configure(text=text)


def sync_main_window_title() -> None:
    m = main_module()
    base = m.t("window_title")
    try:
        if not m.selected_files_globally:
            m.app.title(truncate_window_title(base))
            return
        n = len(m.selected_files_globally)
        if n == 1:
            pth = m.selected_files_globally[0]
            name = os.path.basename(pth)
            kind = file_kind_label(pth)
            folder = os.path.dirname(pth)
            extra = f"{name} · {kind} — {folder}"
        else:
            folder = (
                m.current_source_path
                if m.current_source_path and str(m.current_source_path) != "NOT SET"
                else os.path.dirname(m.selected_files_globally[0])
            )
            kinds = [file_kind_label(p) for p in m.selected_files_globally]
            cnt = Counter(kinds)
            summary = " · ".join(
                f"{label} ×{c}"
                for label, c in sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
            )
            extra = f"{n} {m.t('title_bar_files_word')} · {summary} — {folder}"
        m.app.title(truncate_window_title(f"{base} — {extra}"))
    except Exception:
        try:
            m.app.title(truncate_window_title(base))
        except Exception:
            pass


def apply_queue_sort() -> None:
    m = main_module()
    if len(m.selected_files_globally) < 2:
        return
    pairs = [(fp, read_audio_meta_cached(fp)) for fp in m.selected_files_globally]
    pairs.sort(
        key=lambda x: (queue_sort_tuple(x[1], m.queue_sort_column), x[0].lower()),
        reverse=m.queue_sort_reverse,
    )
    m.selected_files_globally = [fp for fp, _ in pairs]


def refresh_track_queue_table() -> None:
    """Recordbox-style rows for current selection."""
    m = main_module()
    for w in m.track_queue_scroll.winfo_children():
        w.destroy()
    p = palette(m.current_appearance)
    rtl = m.layout_rtl()
    anchor_h = "e" if rtl else "w"
    pack_side = "right" if rtl else "left"
    if m.selected_files_globally:
        apply_queue_sort()
    head = ctk.CTkFrame(m.track_queue_scroll, fg_color=p["table_head"], corner_radius=8)
    head.pack(fill="x", pady=(0, 6))
    head_inner = ctk.CTkFrame(head, fg_color=p["table_head"])
    head_inner.pack(fill="x", padx=4, pady=4)

    hdr_spec = [
        ("title", m.t("col_title"), 168),
        ("artist", m.t("col_artist"), 128),
        ("album", m.t("col_album"), 128),
        ("format", m.t("col_format"), 56),
        ("bpm", m.t("col_bpm"), 52),
        ("duration", m.t("col_dur"), 72),
        ("file_date", m.t("col_file_date"), 112),
        ("filename", m.t("col_file"), 148),
    ]
    if rtl:
        hdr_spec = list(reversed(hdr_spec))

    ctl_head = ctk.CTkFrame(head_inner, fg_color=p["table_head"], width=80)
    sort_head = ctk.CTkFrame(head_inner, fg_color=p["table_head"])
    if rtl:
        sort_head.pack(side="right", fill="x", expand=True)
        ctl_head.pack(side="right")
    else:
        ctl_head.pack(side="left")
        sort_head.pack(side="left", fill="x", expand=True)

    hfont = ("Segoe UI", 13, "bold")
    lh_convert = ctk.CTkLabel(
        ctl_head,
        text=m.t("queue_hdr_convert"),
        width=40,
        anchor="center",
        font=hfont,
        text_color=p["muted"],
    )
    lh_remove = ctk.CTkLabel(
        ctl_head,
        text=m.t("queue_hdr_remove"),
        width=36,
        anchor="center",
        font=hfont,
        text_color=p["muted"],
    )
    if rtl:
        lh_remove.pack(side="right", padx=(2, 4), pady=8)
        lh_convert.pack(side="right", padx=(2, 2), pady=8)
    else:
        lh_convert.pack(side="left", padx=(4, 2), pady=8)
        lh_remove.pack(side="left", padx=(2, 2), pady=8)

    pack_sortable_header_row(
        sort_head,
        hdr_spec,
        p,
        pack_side,
        anchor_h,
        m.queue_sort_column,
        m.queue_sort_reverse,
        queue_header_clicked,
        m.brand_color,
        header_font=("Segoe UI", 13, "bold"),
    )

    if not m.selected_files_globally:
        empty_box = ctk.CTkFrame(m.track_queue_scroll, fg_color=p["surface"])
        empty_box.pack(fill="both", expand=True, padx=8, pady=28)
        ctk.CTkLabel(
            empty_box,
            text=m.t("queue_empty"),
            font=("Segoe UI", 14),
            text_color=p["muted"],
        ).pack(pady=20)
        return

    for i, fp in enumerate(m.selected_files_globally):
        meta_rec = read_audio_meta_cached(fp)
        idle = p["table_row_alt"] if i % 2 else p["table_row"]
        hover = p["nav_hover"]
        row = ctk.CTkFrame(m.track_queue_scroll, fg_color=idle, corner_radius=10)
        row.pack(fill="x", pady=2)
        row_inner = ctk.CTkFrame(row, fg_color=idle)
        row_inner.pack(fill="x", padx=2, pady=0)

        ctl_fr = ctk.CTkFrame(row_inner, fg_color=idle, width=80)
        cells_fr = ctk.CTkFrame(row_inner, fg_color=idle)
        if rtl:
            cells_fr.pack(side="right", fill="x", expand=True)
            ctl_fr.pack(side="right")
        else:
            ctl_fr.pack(side="left")
            cells_fr.pack(side="left", fill="x", expand=True)

        nk = norm_path_key(fp)
        included = nk not in m.queue_excluded_from_convert
        cb = ctk.CTkCheckBox(
            ctl_fr,
            text="",
            width=28,
            fg_color=p["surface"],
            hover_color=p["btn_neutral_hover"],
            text_color=p["text"],
            border_width=1,
            border_color=p["border"],
        )
        if included:
            cb.select()
        else:
            cb.deselect()
        cb.configure(
            command=lambda w=cb, pth=fp: queue_convert_checkbox_changed(pth, w)
        )
        rm_btn = ctk.CTkButton(
            ctl_fr,
            text="×",
            width=32,
            height=28,
            font=("Segoe UI", 16, "bold"),
            fg_color=idle,
            hover_color=p["btn_neutral_hover"],
            text_color=p["text"],
            border_width=1,
            border_color=p["border"],
            corner_radius=8,
            command=lambda pth=fp: remove_path_from_queue(pth),
        )
        if rtl:
            rm_btn.pack(side="right", padx=2, pady=7)
            cb.pack(side="right", padx=4, pady=7)
        else:
            cb.pack(side="left", padx=4, pady=7)
            rm_btn.pack(side="left", padx=2, pady=7)

        vals = [
            (meta_rec["title"], 168),
            (meta_rec["artist"], 128),
            (meta_rec["album"], 128),
            (meta_rec.get("format") or "—", 56),
            (meta_rec["bpm"], 52),
            (meta_rec["duration"], 72),
            (meta_rec["file_date"], 112),
            (shorten_path(meta_rec["filename"], 28), 148),
        ]
        if rtl:
            vals = list(reversed(vals))
        path_ix = 0 if rtl else 7
        pack_table_row_cells(
            cells_fr,
            vals,
            p,
            pack_side,
            anchor_h,
            is_head=False,
            font_data=("Segoe UI", 13),
            path_entry_index=path_ix,
            path_full=fp,
        )
        bind_surface_hover([row, row_inner, ctl_fr, cells_fr], idle, hover)


def queue_header_clicked(sort_key: str) -> None:
    m = main_module()
    if m.queue_sort_column == sort_key:
        m.queue_sort_reverse = not m.queue_sort_reverse
    else:
        m.queue_sort_column = sort_key
        m.queue_sort_reverse = False
    refresh_track_queue_table()


def queue_convert_checkbox_changed(path: str, widget: ctk.CTkCheckBox) -> None:
    v = widget.get()
    on = v not in (0, False, None, "", "off", "0")
    k = norm_path_key(path)
    m = main_module()
    if on:
        m.queue_excluded_from_convert.discard(k)
    else:
        m.queue_excluded_from_convert.add(k)
    sync_main_window_title()


def remove_path_from_queue(path: str) -> None:
    m = main_module()
    if m.is_converting:
        return
    k = norm_path_key(path)
    m.selected_files_globally = [
        x for x in m.selected_files_globally if norm_path_key(x) != k
    ]
    m.queue_excluded_from_convert.discard(k)
    update_paths_ui()


def update_paths_ui(skip_progress_sync: bool = False) -> None:
    m = main_module()
    prune_queue_exclude_set()
    sync_output_folder_entry()
    refresh_track_queue_table()
    if m.selected_files_globally:
        size_str = get_total_size(m.selected_files_globally)
        kinds_s = selection_kinds_summary()
        n_files = len(m.selected_files_globally)
        m.app.after(
            0,
            lambda n=n_files, sz=size_str, ks=kinds_s: m.count_badge.configure(
                text=m.t("badge_files", n=n, kinds=ks, size=sz)
            ),
        )
        m.app.after(0, lambda: sync_sidebar_format_panel())
    else:
        m.app.after(0, lambda: m.count_badge.configure(text=m.t("badge_none")))
        m.app.after(0, lambda: sync_sidebar_format_panel())
    sync_main_window_title()
    if not m.is_converting and not skip_progress_sync:
        m.sync_idle_progress_labels()


def finalize_track_selection(paths: list[str]) -> None:
    m = main_module()
    allow_video = bool(m.audio_settings.get("allow_video_extract"))
    norm = [os.path.normpath(x) for x in paths if x and os.path.isfile(x)]
    norm = [p for p in norm if is_allowed_media_file(p, allow_video)]
    if not norm:
        return
    m.selected_files_globally = norm
    m.current_source_path = os.path.dirname(norm[0])
    record_files_to_history(norm)
    update_paths_ui()


def handle_drop(event) -> None:
    m = main_module()
    if m.is_converting:
        return
    raw = m.app.tk.splitlist(event.data)
    if not raw:
        return
    allow_video = bool(m.audio_settings.get("allow_video_extract"))
    candidates = expand_drop_paths_to_media_files(list(raw))
    if not candidates:
        messagebox.showwarning(m.t("window_title"), m.t("msg_drop_nothing_found"))
        return
    validated = [f for f in candidates if is_allowed_media_file(f, allow_video)]
    for f in candidates:
        if f not in validated:
            m._append_local_log(f"drop rejected header: {f!r}")
    if not validated:
        messagebox.showwarning(m.t("window_title"), m.t("msg_invalid_files_all"))
        return
    open_track_selection_dialog(validated)


def select_source_files() -> None:
    m = main_module()
    if m.is_converting:
        return
    files = filedialog.askopenfilenames(
        title=m.t("dlg_select_audio"),
        filetypes=[
            (
                m.t("dlg_audio_types"),
                "*.wav *.mp3 *.flac *.aiff *.aif *.m4a *.ogg *.mp4 *.mkv *.mov *.webm",
            )
        ],
    )
    if files:
        open_track_selection_dialog(list(files))


def add_from_input_or_picker() -> None:
    m = main_module()
    if m.is_converting:
        return
    allow_video = bool(m.audio_settings.get("allow_video_extract"))
    raw = m.url_entry.get().strip()
    if raw:
        paths = []
        allow = current_allowed_suffixes()
        for line in raw.replace("\r", "\n").split("\n"):
            line = line.strip().strip('"')
            if not line:
                continue
            if os.path.isfile(line) and line.lower().endswith(allow):
                np = os.path.normpath(line)
                if is_allowed_media_file(np, allow_video):
                    paths.append(np)
        if paths:
            m.url_entry.delete(0, "end")
            open_track_selection_dialog(paths)
            return
        messagebox.showwarning(
            m.t("window_title"),
            m.t("msg_warn_paths"),
        )
        return
    select_source_files()


def expand_drop_paths_to_media_files(raw_paths: list[str]) -> list[str]:
    """
    Keep dropped files with allowed extensions; if a path is a folder, collect
    matching files recursively. De-duplicates by normalized path.
    """
    allow = current_allowed_suffixes()
    out: list[str] = []
    seen: set[str] = set()

    def _add_one(fp: str) -> None:
        fp = os.path.normpath(fp)
        key = fp.casefold()
        if key in seen:
            return
        seen.add(key)
        out.append(fp)

    for raw in raw_paths:
        if not raw:
            continue
        p = os.path.normpath(str(raw).strip())
        try:
            if os.path.isfile(p):
                if p.lower().endswith(allow):
                    _add_one(p)
            elif os.path.isdir(p):
                for root, _dirnames, fnames in os.walk(p):
                    for name in fnames:
                        fp = os.path.join(root, name)
                        if fp.lower().endswith(allow):
                            _add_one(fp)
        except OSError:
            continue
    return out
