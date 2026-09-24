"""Modal dialogs for queue and export folder (uses main app module via `converter_main`)."""

import os

import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

from converter11.constants import CONFIG_FILE
from converter11.path_utils import desktop_path, shorten_path, sanitize_folder_name
from converter11.security_utils import is_allowed_media_file
from converter11.ui_context import main_module
from converter11.ui_palette import palette


def open_track_selection_dialog(candidates: list[str]) -> None:
    """After picking multiple files, let the user include/exclude each before loading."""
    m = main_module()
    if m.is_converting:
        return
    allow_video = bool(m.audio_settings.get("allow_video_extract"))
    uniq: list[str] = []
    seen: set[str] = set()
    for raw in candidates:
        np = os.path.normpath(raw)
        key = np.lower()
        if key in seen or not os.path.isfile(np):
            continue
        seen.add(key)
        uniq.append(np)
    if not uniq:
        return
    validated: list[str] = []
    for np in uniq:
        if is_allowed_media_file(np, allow_video):
            validated.append(np)
        else:
            m._append_local_log(f"rejected header: {np!r}")
    if not validated:
        messagebox.showwarning(m.t("window_title"), m.t("msg_invalid_files_all"))
        return
    uniq = validated
    if len(uniq) == 1:
        m._finalize_track_selection(uniq)
        return

    p = palette(m.current_appearance)
    dlg = ctk.CTkToplevel(m.app)
    dlg.title(m.t("dlg_pick_tracks_title"))
    try:
        dlg.transient(m.app)
        dlg.grab_set()
    except Exception:
        pass
    dlg.resizable(True, True)
    dlg.geometry("580x460")
    dlg.minsize(480, 360)
    dlg.configure(fg_color=p["window"])

    ctk.CTkLabel(
        dlg,
        text=m.t("dlg_pick_tracks_hint"),
        font=("Segoe UI", 13),
        text_color=p["muted"],
        wraplength=540,
        justify="left",
    ).pack(anchor="w", padx=16, pady=(16, 8))

    scroll = ctk.CTkScrollableFrame(
        dlg,
        fg_color=p["surface"],
        height=280,
        corner_radius=8,
        border_width=1,
        border_color=p["border"],
    )
    scroll.pack(fill="both", expand=True, padx=16, pady=(0, 8))

    checks: list[tuple[str, ctk.CTkCheckBox]] = []
    for fp in uniq:
        row = ctk.CTkFrame(scroll, fg_color=p["surface"])
        row.pack(fill="x", pady=3, padx=4)
        cb = ctk.CTkCheckBox(
            row,
            text=os.path.basename(fp),
            font=("Segoe UI", 13, "bold"),
            text_color=p["text"],
            fg_color=p["surface"],
            hover_color=p["btn_neutral_hover"],
            border_width=1,
            border_color=p["border"],
        )
        cb.select()
        cb.pack(anchor="w")
        ctk.CTkLabel(
            row,
            text=shorten_path(fp, 72),
            font=("Segoe UI", 11),
            text_color=p["subtle"],
            anchor="w",
        ).pack(anchor="w", padx=(28, 0))
        checks.append((fp, cb))

    btn_row = ctk.CTkFrame(dlg, fg_color=p["window"])
    btn_row.pack(fill="x", padx=16, pady=(0, 8))

    def _all_on():
        for _, c in checks:
            c.select()

    def _all_off():
        for _, c in checks:
            c.deselect()

    def _apply():
        def _cb_yes(c):
            v = c.get()
            return v not in (0, False, None, "", "off", "0")

        chosen = [fp for fp, c in checks if _cb_yes(c)]
        if not chosen:
            messagebox.showwarning(m.t("window_title"), m.t("msg_pick_at_least_one"))
            return
        dlg.destroy()
        m._finalize_track_selection(chosen)

    def _cancel():
        dlg.destroy()

    ctk.CTkButton(
        btn_row,
        text=m.t("btn_select_all_tracks"),
        width=138,
        height=36,
        font=("Segoe UI", 12),
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
        command=_all_on,
    ).pack(side="left", padx=(0, 8))

    ctk.CTkButton(
        btn_row,
        text=m.t("btn_select_none_tracks"),
        width=138,
        height=36,
        font=("Segoe UI", 12),
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
        command=_all_off,
    ).pack(side="left", padx=(0, 16))

    ctk.CTkButton(
        btn_row,
        text=m.t("dlg_cancel"),
        width=100,
        height=36,
        font=("Segoe UI", 12),
        fg_color=p["btn_neutral"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
        command=_cancel,
    ).pack(side="right", padx=(8, 0))

    ctk.CTkButton(
        btn_row,
        text=m.t("btn_load_selected"),
        width=140,
        height=40,
        font=("Segoe UI", 14, "bold"),
        fg_color=m.brand_color,
        hover_color="#E56F00",
        text_color="white",
        command=_apply,
    ).pack(side="right")

    dlg.after(50, lambda: dlg.lift())
    dlg.after(60, lambda: dlg.focus_force())
    try:
        dlg.update_idletasks()
        sw = dlg.winfo_screenwidth()
        sh = dlg.winfo_screenheight()
        ww = dlg.winfo_width()
        wh = dlg.winfo_height()
        dlg.geometry(f"+{(sw - ww) // 2}+{(sh - wh) // 3}")
    except Exception:
        pass


def pick_export_destination() -> None:
    m = main_module()
    if m.is_converting:
        return
    initial_dir = desktop_path()
    if not os.path.isdir(initial_dir):
        initial_dir = os.path.expanduser("~")
    parent = filedialog.askdirectory(
        title=m.t("dlg_pick_parent"),
        initialdir=initial_dir,
    )
    if not parent:
        return
    name = simpledialog.askstring(
        m.t("dlg_output_name"),
        m.t("dlg_output_prompt"),
        initialvalue="11_Export",
    )
    if name is None:
        return
    name = sanitize_folder_name(name.strip() or "11_Export")
    dest = os.path.join(parent, name)
    try:
        os.makedirs(dest, exist_ok=True)
    except OSError as e:
        messagebox.showerror(m.t("window_title"), m.t("dlg_mkdir_err", e=e))
        return
    m.last_export_path = dest
    m.save_config(CONFIG_FILE, dest)
    m.update_ui_paths()
