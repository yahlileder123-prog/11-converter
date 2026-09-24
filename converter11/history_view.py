"""History tab: sortable table and open-in-OS for logged tracks."""

import os
import subprocess
import sys
from tkinter import messagebox

import customtkinter as ctk

from converter11.path_utils import shorten_path
from converter11.security_utils import is_allowed_media_file
from converter11.table_widgets import (
    history_sort_tuple,
    pack_sortable_header_row,
    pack_table_row_cells,
)
from converter11.ui_context import main_module
from converter11.ui_motion import bind_surface_hover
from converter11.ui_palette import palette


def history_open_file(path) -> None:
    m = main_module()
    if not path or not isinstance(path, str):
        messagebox.showwarning(m.t("window_title"), m.t("history_file_missing"))
        return
    path = os.path.normpath(path)
    if not os.path.isfile(path):
        messagebox.showwarning(m.t("window_title"), m.t("history_file_missing"))
        return
    allow_video = bool(m.audio_settings.get("allow_video_extract"))
    if not is_allowed_media_file(path, allow_video):
        messagebox.showwarning(m.t("window_title"), m.t("history_file_unsafe"))
        return
    try:
        if os.name == "nt":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception as e:
        messagebox.showerror(m.t("window_title"), m.t("history_open_failed", e=e))


def history_header_clicked(sort_key: str) -> None:
    m = main_module()
    if m.history_sort_column == sort_key:
        m.history_sort_reverse = not m.history_sort_reverse
    else:
        m.history_sort_column = sort_key
        m.history_sort_reverse = False
    rebuild_history_page()


def rebuild_history_page() -> None:
    m = main_module()
    for w in m.history_scroll.winfo_children():
        w.destroy()
    p = palette(m.current_appearance)
    rtl = m.layout_rtl()
    anchor_h = "e" if rtl else "w"
    pack_side = "right" if rtl else "left"
    head = ctk.CTkFrame(m.history_scroll, fg_color=p["table_head"], corner_radius=8)
    head.pack(fill="x", pady=(0, 8))
    hdr_spec = [
        ("logged_at", m.t("col_logged"), 136),
        ("title", m.t("col_title"), 156),
        ("artist", m.t("col_artist"), 116),
        ("album", m.t("col_album"), 116),
        ("bpm", m.t("col_bpm"), 48),
        ("duration", m.t("col_dur"), 72),
        ("file_date", m.t("col_file_date"), 104),
        ("filename", m.t("col_file"), 124),
    ]
    if rtl:
        hdr_spec = list(reversed(hdr_spec))
    pack_sortable_header_row(
        head,
        hdr_spec,
        p,
        pack_side,
        anchor_h,
        m.history_sort_column,
        m.history_sort_reverse,
        history_header_clicked,
        m.brand_color,
    )
    open_head = ctk.CTkLabel(
        head,
        text=m.t("history_col_open"),
        width=60,
        anchor=anchor_h,
        font=("Segoe UI", 12, "bold"),
        text_color=p["muted"],
    )
    open_head.pack(side=pack_side, padx=(4, 8), pady=(8, 8))

    rows = list(reversed(m.history_entries))
    rows.sort(
        key=lambda meta: (
            history_sort_tuple(meta, m.history_sort_column),
            (meta.get("filename") or "").lower(),
        ),
        reverse=m.history_sort_reverse,
    )
    if not rows:
        ctk.CTkLabel(
            m.history_scroll,
            text=m.t("history_empty"),
            font=("Segoe UI", 13),
            text_color=p["subtle"],
        ).pack(anchor="e" if rtl else "w", padx=8, pady=24)
        return

    for i, meta in enumerate(rows):
        idle = p["table_row_alt"] if i % 2 else p["table_row"]
        row = ctk.CTkFrame(m.history_scroll, fg_color=idle, corner_radius=10)
        row.pack(fill="x", pady=2)
        logged = meta.get("logged_at", "—")[:19].replace("T", " ")
        vals = [
            (logged, 136),
            (meta.get("title", "—"), 156),
            (meta.get("artist", "—"), 116),
            (meta.get("album", "—"), 116),
            (str(meta.get("bpm", "—")), 48),
            (meta.get("duration", "—"), 72),
            (meta.get("file_date", "—"), 104),
            (shorten_path(meta.get("filename", ""), 22), 124),
        ]
        if rtl:
            vals = list(reversed(vals))
        pack_table_row_cells(row, vals, p, pack_side, anchor_h, is_head=False)
        open_btn = ctk.CTkButton(
            row,
            text=m.t("history_open_btn"),
            width=60,
            height=28,
            font=("Segoe UI", 11, "bold"),
            fg_color=p["btn_neutral"],
            hover_color=p["btn_neutral_hover"],
            text_color=p["text"],
            border_width=0,
            corner_radius=8,
            command=lambda pth=meta.get("path"): history_open_file(pth),
        )
        open_btn.pack(side=pack_side, padx=(4, 8), pady=7)
        bind_surface_hover([row], idle, p["nav_hover"])
