"""Main content: music queue / convert / output, and history page shell."""

import customtkinter as ctk
from tkinterdnd2 import DND_FILES
from tkinter import messagebox

from converter11.ui_dialogs import pick_export_destination
from converter11.conversion_runner import run_conversion_thread
from converter11.ui_help_dialogs import show_format_help
from converter11.ui_palette import FONTS, RADII, palette
from converter11.ui_motion import bind_surface_hover
from converter11.track_queue import (
    add_from_input_or_picker,
    handle_drop,
    select_source_files,
    sync_sidebar_format_panel,
)


def build_music_page(m) -> None:
    _ui = palette(m.current_appearance)

    m.main_area = ctk.CTkFrame(m.view_home, fg_color=_ui["window"], corner_radius=0)
    m.main_area.pack(side="right", fill="both", expand=True)

    m.music_page = ctk.CTkFrame(m.main_area, fg_color=_ui["window"], corner_radius=0)
    m.music_page.pack(fill="both", expand=True)

    m.music_upper = ctk.CTkFrame(m.music_page, fg_color=_ui["window"], corner_radius=0)

    m.history_page = ctk.CTkFrame(m.main_area, fg_color=_ui["window"], corner_radius=0)

    m.history_header = ctk.CTkFrame(m.history_page, fg_color=_ui["window"])
    m.history_header.pack(fill="x", padx=32, pady=(28, 8))

    m.history_title = ctk.CTkLabel(
        m.history_header,
        text=m.t("history_title"),
        font=FONTS["page_title"],
        text_color=_ui["text"],
    )
    m.history_title.pack(anchor="w")

    from converter11.history_store import clear_history

    def _clear_history_clicked() -> None:
        if not messagebox.askyesno(m.t("window_title"), m.t("history_clear_confirm")):
            return
        clear_history()
        m.rebuild_history_page()
        m.history_dirty = False

    m.history_clear_btn = ctk.CTkButton(
        m.history_header,
        text=m.t("history_clear"),
        width=132,
        height=32,
        font=FONTS["caption"],
        fg_color=_ui["surface"],
        hover_color=_ui["nav_hover"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=RADII["md"],
        command=_clear_history_clicked,
    )
    m.history_clear_btn.pack(anchor="w", pady=(12, 0))

    m.history_sub = ctk.CTkLabel(
        m.history_header,
        text=m.t("history_sub"),
        font=FONTS["body"],
        text_color=_ui["muted"],
    )
    m.history_sub.pack(anchor="w", pady=(6, 0))

    m.history_scroll = ctk.CTkScrollableFrame(
        m.history_page,
        fg_color=_ui["window"],
        corner_radius=0,
    )
    m.history_scroll.pack(fill="both", expand=True, padx=32, pady=(8, 28))

    # Unused on the simplified home screen; kept so theme/layout/wiring stay valid.
    hidden = ctk.CTkFrame(m.music_page, fg_color=_ui["window"])
    m.top_header_row = ctk.CTkFrame(hidden, fg_color=_ui["window"])
    m.page_title = ctk.CTkLabel(hidden, text=m.t("page_main_title"), font=FONTS["page_title"], text_color=_ui["text"])
    m.page_subtitle = ctk.CTkLabel(hidden, text=m.t("page_subtitle"), font=FONTS["page_sub"], text_color=_ui["muted"])
    m.url_row_frame = ctk.CTkFrame(hidden, fg_color=_ui["window"])
    m.url_entry = ctk.CTkEntry(hidden, placeholder_text=m.t("url_placeholder"))
    m.url_add_btn = ctk.CTkButton(hidden, text=m.t("btn_add_paths"), command=add_from_input_or_picker)
    m.queue_label = ctk.CTkLabel(hidden, text=m.t("queue_label"))
    m.drag_illustration = ctk.CTkLabel(hidden, text="")
    m.hint_drop_sub = ctk.CTkLabel(hidden, text=m.t("drag_hint_sub"))
    m.fmt_lbl = ctk.CTkLabel(hidden, text=m.t("output_format"))
    m.format_help_btn = ctk.CTkButton(hidden, text="?", command=show_format_help)
    m.more_settings_btn = ctk.CTkButton(hidden, text=m.t("more_settings"))
    m.out_lbl = ctk.CTkLabel(hidden, text=m.t("output_folder"))
    m.queue_header_row = ctk.CTkFrame(hidden, fg_color=_ui["surface"])

    m.middle_scroll = ctk.CTkFrame(m.music_upper, fg_color=_ui["window"], corner_radius=0)
    m.middle_scroll.pack(fill="both", expand=True, padx=28, pady=(24, 8))

    m.queue_section = ctk.CTkFrame(m.middle_scroll, fg_color=_ui["window"])
    m.queue_section.pack(fill="both", expand=True)

    m.queue_card = ctk.CTkFrame(
        m.queue_section,
        fg_color=_ui["surface"],
        corner_radius=RADII["lg"],
        border_width=1,
        border_color=_ui["border"],
    )
    m.queue_card.pack(fill="both", expand=True)

    m.drop_zone = ctk.CTkFrame(
        m.queue_card,
        fg_color=_ui["drop_zone"],
        corner_radius=RADII["md"],
        border_width=1,
        border_color=_ui["drop_zone_border"],
    )
    m.drop_zone.pack(fill="x", padx=12, pady=12)

    m.queue_drop_row = ctk.CTkFrame(m.drop_zone, fg_color=_ui["drop_zone"])
    m.queue_drop_row.pack(fill="x", padx=12, pady=10)

    m.text_mid = ctk.CTkFrame(m.queue_drop_row, fg_color=_ui["drop_zone"])
    m.text_mid.pack(side="left", fill="both", expand=True)

    m.hint_drop = ctk.CTkLabel(
        m.text_mid,
        text=m.t("drag_hint"),
        font=FONTS["body"],
        text_color=_ui["muted"],
        anchor="w",
    )
    m.hint_drop.pack(fill="x", anchor="w")

    m.queue_add_btn = ctk.CTkButton(
        m.queue_drop_row,
        text=m.t("queue_add_tracks"),
        font=FONTS["btn"],
        height=36,
        width=88,
        fg_color=m.brand_color,
        hover_color="#E56F00",
        text_color="white",
        corner_radius=RADII["md"],
        command=select_source_files,
    )
    m.queue_add_btn.pack(side="right", padx=(10, 0))

    m.count_badge = ctk.CTkLabel(
        m.queue_drop_row,
        text=m.t("badge_none"),
        font=FONTS["caption"],
        text_color=_ui["muted"],
        fg_color=_ui["surface"],
        corner_radius=RADII["sm"],
        padx=10,
        pady=4,
    )
    m.count_badge.pack(side="right", padx=(0, 8))

    def _paint_drop_zone(active: bool) -> None:
        p = palette(m.current_appearance)
        fill = p["drop_zone_hover"] if active else p["drop_zone"]
        border = m.brand_color if active else p["drop_zone_border"]
        m.drop_zone.configure(fg_color=fill, border_color=border)
        m.queue_drop_row.configure(fg_color=fill)
        m.text_mid.configure(fg_color=fill)

    m._paint_drop_zone = _paint_drop_zone
    bind_surface_hover(
        [m.drop_zone, m.queue_drop_row, m.text_mid],
        _ui["drop_zone"],
        _ui["drop_zone_hover"],
    )

    def _on_drop(event) -> None:
        _paint_drop_zone(False)
        handle_drop(event)

    m.queue_card.drop_target_register(DND_FILES)
    m.queue_card.dnd_bind("<<Drop>>", _on_drop)
    m.drop_zone.drop_target_register(DND_FILES)
    m.drop_zone.dnd_bind("<<Drop>>", _on_drop)
    try:
        m.drop_zone.dnd_bind("<<DropEnter>>", lambda _e: _paint_drop_zone(True))
        m.drop_zone.dnd_bind("<<DropLeave>>", lambda _e: _paint_drop_zone(False))
        m.queue_card.dnd_bind("<<DropEnter>>", lambda _e: _paint_drop_zone(True))
        m.queue_card.dnd_bind("<<DropLeave>>", lambda _e: _paint_drop_zone(False))
    except Exception:
        pass

    m.track_queue_scroll = ctk.CTkScrollableFrame(
        m.queue_card,
        fg_color=_ui["surface"],
        corner_radius=0,
        border_width=0,
        scrollbar_button_color=_ui["border"],
        scrollbar_button_hover_color=_ui["subtle"],
    )
    m.track_queue_scroll.pack(fill="both", expand=True, padx=8, pady=(0, 12))

    m.bottom_action_bar = ctk.CTkFrame(m.music_page, fg_color=_ui["window"], corner_radius=0)

    m.status_card = ctk.CTkFrame(
        m.bottom_action_bar,
        fg_color=_ui["surface"],
        corner_radius=RADII["lg"],
        border_width=1,
        border_color=_ui["border"],
    )
    m.status_card.pack(fill="x")

    m.status_inner = ctk.CTkFrame(m.status_card, fg_color=_ui["surface"])
    m.status_inner.pack(fill="x", padx=14, pady=(12, 4))

    m.progress_label = ctk.CTkLabel(
        m.status_inner,
        text="",
        font=FONTS["caption"],
        text_color=_ui["muted"],
        anchor="w",
    )

    m.progress_bar = ctk.CTkProgressBar(
        m.status_inner,
        height=5,
        progress_color=m.brand_color,
        fg_color=_ui["progress_trough"],
        corner_radius=3,
    )
    m.progress_bar.pack(fill="x")
    m.progress_bar.set(0)

    m.eta_label = ctk.CTkLabel(
        m.status_inner,
        text="",
        font=FONTS["caption"],
        text_color=_ui["muted"],
        anchor="w",
    )

    m.bottom_fmt_row = ctk.CTkFrame(m.status_card, fg_color=_ui["surface"])
    m.bottom_fmt_row.pack(fill="x", padx=14, pady=(10, 12))

    m.fmt_row_left = ctk.CTkFrame(m.bottom_fmt_row, fg_color=_ui["surface"])
    m.fmt_row_left.pack(side="left")

    m.format_option = ctk.CTkOptionMenu(
        m.fmt_row_left,
        values=["WAV", "MP3", "FLAC", "AIFF", "M4A (Apple)"],
        width=120,
        height=36,
        font=FONTS["body_sm"],
        fg_color=_ui["btn_neutral"],
        button_color=m.brand_color,
        corner_radius=RADII["md"],
        command=lambda _c: sync_sidebar_format_panel(),
    )
    m.format_option.pack(side="left")
    m.format_option.set("WAV")

    m.output_card = ctk.CTkFrame(m.bottom_fmt_row, fg_color=_ui["surface"], corner_radius=0, border_width=0)
    m.output_card.pack(side="left", fill="x", expand=True, padx=10)

    m.output_entry_row = ctk.CTkFrame(m.output_card, fg_color=_ui["surface"])
    m.output_entry_row.pack(fill="x")

    m.output_folder_entry = ctk.CTkEntry(
        m.output_entry_row,
        height=36,
        font=FONTS["body_sm"],
        state="readonly",
        fg_color=_ui["input_bg"],
        border_color=_ui["border"],
        text_color=_ui["text"],
        corner_radius=RADII["md"],
    )
    m.output_folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

    m.output_browse_btn = ctk.CTkButton(
        m.output_entry_row,
        text=m.t("browse_folder"),
        width=100,
        height=36,
        font=FONTS["body_sm"],
        fg_color=_ui["btn_neutral"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_width=0,
        corner_radius=RADII["md"],
        command=pick_export_destination,
    )
    m.output_browse_btn.pack(side="left")

    m.convert_btn = ctk.CTkButton(
        m.bottom_fmt_row,
        text=m.t("btn_convert"),
        font=FONTS["btn_primary"],
        height=36,
        width=140,
        fg_color=m.brand_color,
        hover_color="#E56F00",
        text_color="white",
        corner_radius=RADII["md"],
        command=run_conversion_thread,
    )
    m.convert_btn.pack(side="right")

    m.bottom_action_bar.pack(side="bottom", fill="x", padx=28, pady=(0, 22))
    m.music_upper.pack(fill="both", expand=True)
