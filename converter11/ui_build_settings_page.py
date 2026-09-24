"""Settings scroll: audio, pattern, split, video, language, theme."""

import customtkinter as ctk

from converter11.audio_settings_handlers import (
    audio_save_bd as _audio_save_bd,
    audio_save_checkbox as _audio_save_checkbox,
    audio_save_sr as _audio_save_sr,
)
from converter11.constants import PATTERN_SEP_CHOICES
from converter11.name_pattern_ui import (
    on_pattern_advanced_toggle as _on_pattern_advanced_toggle,
    pat_labels as _pat_labels,
    pattern_sep_cmd as _pattern_sep_cmd,
    pattern_slot_cmd as _pattern_slot_cmd,
    rebuild_pattern_from_builder as _rebuild_pattern_from_builder,
    save_name_pattern as _save_name_pattern,
)
from converter11.ui_help_dialogs import (
    show_settings_appearance_help,
    show_settings_audio_help,
    show_settings_formats_help,
    show_settings_lang_help,
    show_settings_pattern_help,
    show_settings_video_help,
)
from converter11.ui_navigation import show_home_view
from converter11.ui_palette import FONTS, RADII, palette
from converter11.ui_theme import pick_theme_and_save


def build_settings_page(m) -> None:
    _ui = palette(m.current_appearance)

    m.view_settings = ctk.CTkFrame(m.main_frame, fg_color=_ui["window"])

    m.settings_inner = ctk.CTkFrame(m.view_settings, fg_color=_ui["window"])
    m.settings_inner.pack(fill="both", expand=True, padx=28, pady=24)

    m.settings_head_row = ctk.CTkFrame(m.settings_inner, fg_color=_ui["window"])
    m.settings_head_row.pack(fill="x", pady=(0, 8))

    m.back_to_app_btn = ctk.CTkButton(
        m.settings_head_row,
        text=m.t("btn_back"),
        font=FONTS["body"],
        width=112,
        height=38,
        corner_radius=RADII["md"],
        border_width=1,
        command=show_home_view,
    )
    m.back_to_app_btn.pack(side="left", anchor="w")

    m.settings_scroll = ctk.CTkScrollableFrame(
        m.settings_inner,
        fg_color=_ui["window"],
        corner_radius=0,
    )
    m.settings_scroll.pack(fill="both", expand=True)

    m.settings_main_heading = ctk.CTkLabel(
        m.settings_scroll,
        text=m.t("settings_main"),
        font=FONTS["page_title"],
        text_color=_ui["text"],
    )
    m.settings_main_heading.pack(anchor="w", pady=(16, 8))

    m.audio_section_header = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.audio_section_header.pack(anchor="w", fill="x", pady=(8, 4))
    m.settings_audio_title = ctk.CTkLabel(
        m.audio_section_header,
        text=m.t("settings_audio_section"),
        font=("Segoe UI", 22, "bold"),
        text_color=_ui["text"],
    )
    m.settings_audio_help_btn = ctk.CTkButton(
        m.audio_section_header,
        text="?",
        width=32,
        height=32,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["nav_active"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=8,
        command=show_settings_audio_help,
    )
    m.settings_audio_title.pack(side="left", fill="x", expand=True, anchor="w")
    m.settings_audio_help_btn.pack(side="right")

    m.audio_sr_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.audio_sr_row.pack(anchor="w", fill="x", pady=(0, 6))
    m.sr_label = ctk.CTkLabel(
        m.audio_sr_row,
        text=m.t("label_sample_rate"),
        font=("Segoe UI", 14),
        text_color=_ui["text"],
        width=200,
        anchor="w",
    )
    m.sr_label.pack(side="left", padx=(0, 12))
    m.sample_rate_option = ctk.CTkOptionMenu(
        m.audio_sr_row,
        values=["44100", "48000", "96000"],
        command=_audio_save_sr,
        width=220,
        height=34,
        font=("Segoe UI", 13),
        fg_color=_ui["surface"],
        button_color=m.brand_color,
        corner_radius=8,
    )
    m.sample_rate_option.pack(side="left")
    m.sample_rate_option.set(str(int(m.audio_settings.get("sample_rate_hz", 44100))))

    m.audio_bd_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.audio_bd_row.pack(anchor="w", fill="x", pady=(0, 6))
    m.bd_label = ctk.CTkLabel(
        m.audio_bd_row,
        text=m.t("label_bit_depth"),
        font=("Segoe UI", 14),
        text_color=_ui["text"],
        width=200,
        anchor="w",
    )
    m.bd_label.pack(side="left", padx=(0, 12))
    m.bit_depth_option = ctk.CTkOptionMenu(
        m.audio_bd_row,
        values=["16", "24", "32f"],
        command=_audio_save_bd,
        width=220,
        height=34,
        font=("Segoe UI", 13),
        fg_color=_ui["surface"],
        button_color=m.brand_color,
        corner_radius=8,
    )
    m.bit_depth_option.pack(side="left")
    m.bit_depth_option.set(str(m.audio_settings.get("pcm_bit_depth", "24")))

    m.formats_header_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.formats_header_row.pack(anchor="w", fill="x", pady=(8, 6))
    m.formats_heading_label = ctk.CTkLabel(
        m.formats_header_row,
        text=m.t("settings_formats_heading"),
        font=("Segoe UI", 16, "bold"),
        text_color=_ui["text"],
    )
    m.formats_help_btn = ctk.CTkButton(
        m.formats_header_row,
        text="?",
        width=32,
        height=32,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["nav_active"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=8,
        command=show_settings_formats_help,
    )
    m.formats_heading_label.pack(side="left", fill="x", expand=True, anchor="w")
    m.formats_help_btn.pack(side="right")

    m.embed_meta_check = ctk.CTkCheckBox(
        m.settings_scroll,
        text=m.t("settings_embed_meta"),
        font=("Segoe UI", 14),
        command=lambda: _audio_save_checkbox(m.embed_meta_check, "embed_metadata"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_color=_ui["border"],
    )
    m.embed_meta_check.pack(anchor="w", pady=(0, 6))
    if m.audio_settings.get("embed_metadata", True):
        m.embed_meta_check.select()

    m.normalize_check = ctk.CTkCheckBox(
        m.settings_scroll,
        text=m.t("settings_normalize"),
        font=("Segoe UI", 14),
        command=lambda: _audio_save_checkbox(m.normalize_check, "normalize"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_color=_ui["border"],
    )
    m.normalize_check.pack(anchor="w", pady=(0, 10))
    if m.audio_settings.get("normalize"):
        m.normalize_check.select()

    m.pattern_header_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.pattern_header_row.pack(anchor="w", fill="x", pady=(4, 4))
    m.pattern_label = ctk.CTkLabel(
        m.pattern_header_row,
        text=m.t("settings_name_pattern"),
        font=("Segoe UI", 14, "bold"),
        text_color=_ui["text"],
    )
    m.pattern_help_btn = ctk.CTkButton(
        m.pattern_header_row,
        text="?",
        width=32,
        height=32,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["nav_active"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=8,
        command=show_settings_pattern_help,
    )
    m.pattern_label.pack(side="left", fill="x", expand=True, anchor="w")
    m.pattern_help_btn.pack(side="right")

    m.pattern_preview_label = ctk.CTkLabel(
        m.settings_scroll,
        text="",
        font=("Segoe UI Semibold", 13),
        text_color=_ui["text"],
        wraplength=720,
        justify="left",
    )

    m.pattern_builder_frame = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.pattern_slot_menus = []
    m.pattern_part_row_labels = []
    for slot_i in range(4):
        prow = ctk.CTkFrame(m.pattern_builder_frame, fg_color=_ui["window"])
        prow.pack(anchor="w", fill="x", pady=3)
        plab = ctk.CTkLabel(
            prow,
            text=f'{m.t("pattern_slot_prefix")} {slot_i + 1}',
            font=("Segoe UI", 13),
            text_color=_ui["text"],
            width=72,
            anchor="w",
        )
        plab.pack(side="left", padx=(0, 10))
        m.pattern_part_row_labels.append(plab)
        om = ctk.CTkOptionMenu(
            prow,
            values=_pat_labels(),
            width=280,
            height=34,
            font=("Segoe UI", 13),
            fg_color=_ui["surface"],
            button_color=m.brand_color,
            corner_radius=8,
        )
        om.pack(side="left")
        pid = m.audio_settings["name_pattern_parts"][slot_i]
        om.set(m.t(f"pat_{pid}"))
        m.pattern_slot_menus.append(om)

    m.pattern_sep_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.sep_label_widget = ctk.CTkLabel(
        m.pattern_sep_row,
        text=m.t("pattern_sep_label"),
        font=("Segoe UI", 14),
        text_color=_ui["text"],
        width=200,
        anchor="w",
    )
    m.sep_label_widget.pack(side="left", padx=(0, 12))
    _sep_vals = list(PATTERN_SEP_CHOICES)
    _cur_sep = m.audio_settings.get("name_pattern_sep", " - ")
    if _cur_sep not in _sep_vals:
        _sep_vals = list(_sep_vals) + [_cur_sep]
    m.pattern_sep_option = ctk.CTkOptionMenu(
        m.pattern_sep_row,
        values=_sep_vals,
        width=220,
        height=34,
        font=("Segoe UI", 13),
        fg_color=_ui["surface"],
        button_color=m.brand_color,
        corner_radius=8,
    )
    m.pattern_sep_option.pack(side="left")
    m.pattern_sep_option.set(_cur_sep)

    m.pattern_hint_label = ctk.CTkLabel(
        m.settings_scroll,
        text=m.t("settings_name_pattern_hint"),
        font=("Segoe UI", 12),
        text_color=_ui["muted"],
        wraplength=700,
        justify="left",
    )

    m.audio_pattern_entry = ctk.CTkEntry(
        m.settings_scroll,
        width=560,
        height=38,
        font=("Segoe UI", 13),
        fg_color=_ui["input_bg"],
        border_color=_ui["border"],
        text_color=_ui["text"],
    )

    for idx, slot_menu in enumerate(m.pattern_slot_menus):
        slot_menu.configure(
            command=lambda c, i=idx: _pattern_slot_cmd(c, i)
        )
    m.pattern_sep_option.configure(command=_pattern_sep_cmd)

    m.pattern_advanced_check = ctk.CTkCheckBox(
        m.settings_scroll,
        text=m.t("pattern_advanced"),
        font=("Segoe UI", 14),
        command=_on_pattern_advanced_toggle,
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_color=_ui["border"],
    )

    if m.audio_settings.get("name_pattern_advanced"):
        m.pattern_advanced_check.select()
        m.pattern_hint_label.pack(anchor="w", pady=(0, 6))
        m.audio_pattern_entry.pack(anchor="w", pady=(0, 12))
        m.audio_pattern_entry.insert(
            0, m.audio_settings.get("name_pattern") or "{artist} - {title}"
        )
    else:
        m.pattern_preview_label.pack(anchor="w", pady=(0, 6))
        m.pattern_builder_frame.pack(anchor="w", fill="x", pady=(0, 6))
        m.pattern_sep_row.pack(anchor="w", fill="x", pady=(0, 8))
        _rebuild_pattern_from_builder()

    m.pattern_advanced_check.pack(anchor="w", pady=(0, 10))

    m.audio_pattern_entry.bind("<Return>", _save_name_pattern)
    m.audio_pattern_entry.bind("<FocusOut>", _save_name_pattern)

    m.split_format_check = ctk.CTkCheckBox(
        m.settings_scroll,
        text=m.t("settings_split_format"),
        font=("Segoe UI", 14),
        command=lambda: _audio_save_checkbox(m.split_format_check, "split_by_format"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_color=_ui["border"],
    )
    m.split_format_check.pack(anchor="w", pady=(0, 6))
    if m.audio_settings.get("split_by_format"):
        m.split_format_check.select()

    m.video_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.video_row.pack(anchor="w", fill="x", pady=(0, 20))
    m.video_extract_check = ctk.CTkCheckBox(
        m.video_row,
        text=m.t("settings_video_extract"),
        font=("Segoe UI", 14),
        command=lambda: _audio_save_checkbox(m.video_extract_check, "allow_video_extract"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_color=_ui["border"],
    )
    m.video_help_btn = ctk.CTkButton(
        m.video_row,
        text="?",
        width=32,
        height=32,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["nav_active"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=8,
        command=show_settings_video_help,
    )
    m.video_extract_check.pack(side="left", fill="x", expand=True)
    m.video_help_btn.pack(side="right")
    if m.audio_settings.get("allow_video_extract"):
        m.video_extract_check.select()

    m.lang_header_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.lang_header_row.pack(anchor="w", fill="x", pady=(8, 4))
    m.settings_lang_heading = ctk.CTkLabel(
        m.lang_header_row,
        text=m.t("settings_lang"),
        font=("Segoe UI", 16, "bold"),
        text_color=_ui["text"],
    )
    m.lang_help_btn = ctk.CTkButton(
        m.lang_header_row,
        text="?",
        width=32,
        height=32,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["nav_active"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=8,
        command=show_settings_lang_help,
    )
    m.settings_lang_heading.pack(side="left", fill="x", expand=True, anchor="w")
    m.lang_help_btn.pack(side="right")

    m.lang_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.lang_row.pack(anchor="w", pady=(0, 20))

    m.lang_btn_he = ctk.CTkButton(
        m.lang_row,
        text=m.t("lang_pick_he"),
        width=130,
        height=42,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_width=2,
        border_color=m.brand_color,
        corner_radius=10,
    )
    m.lang_btn_he.pack(side="left", padx=(0, 12))

    m.lang_btn_en = ctk.CTkButton(
        m.lang_row,
        text=m.t("lang_pick_en"),
        width=130,
        height=42,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_width=2,
        border_color=m.brand_color,
        corner_radius=10,
    )
    m.lang_btn_en.pack(side="left")

    m.appearance_header_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.appearance_header_row.pack(anchor="w", fill="x", pady=(12, 8))
    m.settings_screen_title = ctk.CTkLabel(
        m.appearance_header_row,
        text=m.t("settings_appearance"),
        font=("Segoe UI", 22, "bold"),
        text_color=_ui["text"],
    )
    m.appearance_help_btn = ctk.CTkButton(
        m.appearance_header_row,
        text="?",
        width=32,
        height=32,
        font=("Segoe UI", 14, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["nav_active"],
        text_color=_ui["text"],
        border_width=1,
        border_color=_ui["border"],
        corner_radius=8,
        command=show_settings_appearance_help,
    )
    m.settings_screen_title.pack(side="left", fill="x", expand=True, anchor="w")
    m.appearance_help_btn.pack(side="right")

    m.theme_buttons_row = ctk.CTkFrame(m.settings_scroll, fg_color=_ui["window"])
    m.theme_buttons_row.pack(anchor="w", pady=(0, 12))

    m.theme_btn_light = ctk.CTkButton(
        m.theme_buttons_row,
        text=m.t("theme_light"),
        width=140,
        height=48,
        font=("Segoe UI", 15, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_width=2,
        border_color=m.brand_color,
        corner_radius=12,
        command=lambda: pick_theme_and_save("light"),
    )
    m.theme_btn_light.pack(side="left", padx=(0, 16))

    m.theme_btn_dark = ctk.CTkButton(
        m.theme_buttons_row,
        text=m.t("theme_dark"),
        width=140,
        height=48,
        font=("Segoe UI", 15, "bold"),
        fg_color=_ui["surface"],
        hover_color=_ui["btn_neutral_hover"],
        text_color=_ui["text"],
        border_width=2,
        border_color=m.brand_color,
        corner_radius=12,
        command=lambda: pick_theme_and_save("dark"),
    )
    m.theme_btn_dark.pack(side="left")
