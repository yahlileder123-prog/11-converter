"""Sortable table headers and row cells for queue / history views."""

import customtkinter as ctk

from converter11.ctk_helpers import wire_entry_text_selection


def pack_table_row_cells(
    parent: ctk.CTkFrame,
    cells: list[tuple[str, int]],
    p: dict,
    pack_side: str,
    anchor_h: str,
    *,
    is_head: bool,
    font_data: tuple = ("Segoe UI", 12),
    font_header: tuple = ("Segoe UI", 12, "bold"),
    path_entry_index: int | None = None,
    path_full: str | None = None,
    with_separators: bool = False,
) -> None:
    """Pack label cells; separators off by default for a cleaner table."""
    font = font_header if is_head else font_data
    sep_h = 32 if is_head else 28
    pady_cell = (9, 9) if is_head else (8, 8)
    n = len(cells)
    use_path_entry = (
        not is_head
        and path_entry_index is not None
        and path_full
        and 0 <= path_entry_index < n
    )
    for i, (text, wpx) in enumerate(cells):
        if use_path_entry and i == path_entry_index:
            ent = ctk.CTkEntry(
                parent,
                width=wpx,
                height=28,
                font=font,
                fg_color=p["table_row"],
                border_width=0,
                text_color=p["text"],
                justify="left" if anchor_h == "w" else "right",
            )
            ent.insert(0, path_full)
            ent.configure(state="readonly")
            wire_entry_text_selection(ent)
            ent.pack(side=pack_side, padx=(4, 4), pady=pady_cell)
        else:
            lbl = ctk.CTkLabel(
                parent,
                text=text,
                width=wpx,
                anchor=anchor_h,
                font=font,
                text_color=p["muted"] if is_head else p["text"],
            )
            lbl.pack(side=pack_side, padx=(4, 4), pady=pady_cell)
        if with_separators and i < n - 1:
            sep = ctk.CTkFrame(
                parent,
                width=1,
                height=sep_h,
                fg_color=p["table_grid"],
                corner_radius=0,
            )
            sep.pack(side=pack_side, fill="y", pady=(8, 8))


def parse_duration_mmss(s) -> float:
    if s is None or s == "—":
        return -1.0
    try:
        parts = str(s).strip().split(":")
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except (ValueError, IndexError):
        pass
    return -1.0


def queue_sort_tuple(m: dict, key: str):
    if key == "title":
        return ((m.get("title") or "").lower(),)
    if key == "artist":
        return ((m.get("artist") or "").lower(),)
    if key == "album":
        return ((m.get("album") or "").lower(),)
    if key == "format":
        return ((m.get("format") or "").lower(),)
    if key == "bpm":
        v = m.get("bpm", "—")
        if v in (None, "", "—"):
            return (1, "")
        try:
            return (0, float(str(v).replace(",", ".")))
        except ValueError:
            return (1, str(v).lower())
    if key == "duration":
        ds = m.get("duration_seconds")
        if isinstance(ds, (int, float)) and ds >= 0:
            return (0, float(ds))
        return (1, parse_duration_mmss(m.get("duration")))
    if key == "file_date":
        return ((m.get("file_date") or ""),)
    if key == "filename":
        return ((m.get("filename") or "").lower(),)
    return (("",),)


def history_sort_tuple(meta: dict, key: str):
    if key == "logged_at":
        return ((meta.get("logged_at") or ""),)
    if key == "title":
        return ((meta.get("title") or "").lower(),)
    if key == "artist":
        return ((meta.get("artist") or "").lower(),)
    if key == "album":
        return ((meta.get("album") or "").lower(),)
    if key == "bpm":
        v = meta.get("bpm", "—")
        if v in (None, "", "—"):
            return (1, "")
        try:
            return (0, float(str(v).replace(",", ".")))
        except ValueError:
            return (1, str(v).lower())
    if key == "duration":
        ds = meta.get("duration_seconds")
        if isinstance(ds, (int, float)) and ds >= 0:
            return (0, float(ds))
        return (1, parse_duration_mmss(meta.get("duration")))
    if key == "file_date":
        return ((meta.get("file_date") or ""),)
    if key == "filename":
        return ((meta.get("filename") or "").lower(),)
    return (("",),)


def sort_header_suffix(active: str, col: str, reverse: bool) -> str:
    if active != col:
        return ""
    return " ▲" if not reverse else " ▼"


def pack_sortable_header_row(
    parent: ctk.CTkFrame,
    col_specs: list[tuple[str, str, int]],
    p: dict,
    pack_side: str,
    anchor_h: str,
    active_col: str,
    reverse: bool,
    on_click,
    accent_color: str,
    *,
    header_font: tuple = ("Segoe UI", 12, "bold"),
    with_separators: bool = False,
) -> None:
    """col_specs: (sort_key, label_text, width). on_click(sort_key)."""
    sep_h = 32
    pady_cell = (9, 9)
    n = len(col_specs)
    for i, (sort_key, label_text, wpx) in enumerate(col_specs):
        txt = label_text + sort_header_suffix(active_col, sort_key, reverse)
        lbl = ctk.CTkLabel(
            parent,
            text=txt,
            width=wpx,
            anchor=anchor_h,
            font=header_font,
            text_color=accent_color if active_col == sort_key else p["muted"],
        )
        lbl.pack(side=pack_side, padx=(8, 8), pady=pady_cell)
        try:
            lbl.configure(cursor="hand2")
        except Exception:
            pass
        lbl.bind("<Button-1>", lambda e, sk=sort_key: on_click(sk))
        if with_separators and i < n - 1:
            sep = ctk.CTkFrame(
                parent,
                width=1,
                height=sep_h,
                fg_color=p["table_grid"],
                corner_radius=0,
            )
            sep.pack(side=pack_side, fill="y", pady=(8, 8))
