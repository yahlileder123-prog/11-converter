"""Left navigation column (11 CONVERTER, music/history, settings)."""

import customtkinter as ctk

from converter11.ui_palette import FONTS, RADII, palette
from converter11.ui_theme import show_history_page, show_music_page


def _nav_item(parent, m, *, text: str, command, row_attr: str, indicator_attr: str, btn_attr: str) -> None:
    _ui = palette(m.current_appearance)
    row = ctk.CTkFrame(parent, fg_color=_ui["sidebar"], corner_radius=RADII["md"], height=44)
    row.pack(fill="x", pady=3)
    row.pack_propagate(False)

    indicator = ctk.CTkFrame(row, width=3, corner_radius=2, fg_color=_ui["sidebar"])
    indicator.pack(side="left", fill="y", padx=(6, 0), pady=8)

    btn = ctk.CTkButton(
        row,
        text=text,
        font=FONTS["nav"],
        anchor="w",
        height=40,
        fg_color=_ui["sidebar"],
        hover_color=_ui["nav_hover"],
        text_color=_ui["muted"],
        corner_radius=RADII["sm"],
        command=command,
    )
    btn.pack(side="left", fill="both", expand=True, padx=(4, 8))

    setattr(m, row_attr, row)
    setattr(m, indicator_attr, indicator)
    setattr(m, btn_attr, btn)


def build_sidebar(m) -> None:
    _ui = palette(m.current_appearance)

    m.sidebar_frame = ctk.CTkFrame(
        m.view_home,
        fg_color=_ui["sidebar"],
        width=248,
        corner_radius=0,
        border_width=0,
    )
    m.sidebar_frame.pack(side="left", fill="y")
    m.sidebar_frame.pack_propagate(False)

    brand_block = ctk.CTkFrame(m.sidebar_frame, fg_color=_ui["sidebar"])
    brand_block.pack(fill="x", padx=22, pady=(26, 0))

    m.sidebar_title = ctk.CTkLabel(
        brand_block,
        text="11",
        font=FONTS["brand"],
        text_color=_ui["text"],
    )
    m.sidebar_title.pack(anchor="w")

    m.sidebar_subtitle = ctk.CTkLabel(
        brand_block,
        text=m.t("sidebar_tagline"),
        font=FONTS["brand_sub"],
        text_color=_ui["muted"],
    )
    m.sidebar_subtitle.pack(anchor="w", pady=(2, 0))

    m.sidebar_divider = ctk.CTkFrame(
        m.sidebar_frame,
        height=1,
        fg_color=_ui["border"],
        corner_radius=0,
    )
    m.sidebar_divider.pack(fill="x", padx=20, pady=(20, 16))

    nav_wrap = ctk.CTkFrame(m.sidebar_frame, fg_color=_ui["sidebar"])
    nav_wrap.pack(fill="x", padx=14)

    _nav_item(
        nav_wrap,
        m,
        text=m.t("nav_music"),
        command=show_music_page,
        row_attr="nav_music_row",
        indicator_attr="nav_music_indicator",
        btn_attr="nav_music_btn",
    )
    _nav_item(
        nav_wrap,
        m,
        text=m.t("nav_history"),
        command=show_history_page,
        row_attr="nav_history_row",
        indicator_attr="nav_history_indicator",
        btn_attr="nav_history_btn",
    )

    info_card = ctk.CTkFrame(
        m.sidebar_frame,
        fg_color=_ui["surface"],
        corner_radius=RADII["md"],
        border_width=1,
        border_color=_ui["border"],
    )
    m.sidebar_info_card = info_card

    m.sidebar_file_kinds = ctk.CTkLabel(
        info_card,
        fg_color=_ui["surface"],
        text=(
            f"{m.t('sidebar_source_prefix')}: {m.t('sidebar_no_source_yet')}\n"
            f"{m.t('sidebar_export_prefix')}: —"
        ),
        font=FONTS["caption"],
        text_color=_ui["muted"],
        anchor="w",
        justify="left",
        wraplength=200,
    )
    m.sidebar_file_kinds.pack(fill="x", padx=12, pady=10)

    m.sidebar_spacer = ctk.CTkFrame(m.sidebar_frame, fg_color=_ui["sidebar"])
    m.sidebar_spacer.pack(fill="both", expand=True)

    m.sidebar_bottom = ctk.CTkFrame(m.sidebar_frame, fg_color=_ui["sidebar"])
    m.sidebar_bottom.pack(side="bottom", fill="x", padx=14, pady=(0, 22))

    m.sidebar_settings_btn = ctk.CTkButton(
        m.sidebar_bottom,
        text=m.t("nav_settings"),
        height=40,
        font=FONTS["body_sm"],
        fg_color=_ui["surface"],
        hover_color=_ui["nav_hover"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=RADII["md"],
        command=lambda: None,
    )
    m.sidebar_settings_btn.pack(fill="x")
