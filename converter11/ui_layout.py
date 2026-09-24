"""RTL/LTR layout and language-driven UI text refresh for the main window."""

from converter11.ctk_helpers import ctk_entry_justify
from converter11.ui_context import main_module
from converter11.ui_theme import set_nav_active


def layout_settings_headers(rtl: bool) -> None:
    m = main_module()
    title_padx_end = 8

    def _title_help(title_w, help_w):
        title_w.pack_forget()
        help_w.pack_forget()
        if rtl:
            help_w.pack(side="right")
            title_w.pack(
                side="right",
                fill="x",
                expand=True,
                padx=(0, title_padx_end),
                anchor="e",
            )
        else:
            title_w.pack(side="left", fill="x", expand=True, anchor="w")
            help_w.pack(side="right")

    _title_help(m.settings_audio_title, m.settings_audio_help_btn)
    _title_help(m.formats_heading_label, m.formats_help_btn)
    _title_help(m.pattern_label, m.pattern_help_btn)
    _title_help(m.settings_lang_heading, m.lang_help_btn)
    _title_help(m.settings_screen_title, m.appearance_help_btn)

    m.video_extract_check.pack_forget()
    m.video_help_btn.pack_forget()
    if rtl:
        m.video_help_btn.pack(side="right")
        m.video_extract_check.pack(side="right", fill="x", expand=True, padx=(0, 8))
    else:
        m.video_extract_check.pack(side="left", fill="x", expand=True)
        m.video_help_btn.pack(side="right")


def apply_layout_direction() -> None:
    """Hebrew: RTL; English: LTR. Call after widgets exist and when ui_lang changes."""
    m = main_module()
    rtl = m.layout_rtl()

    m.sidebar_frame.pack_forget()
    m.main_area.pack_forget()
    if rtl:
        m.main_area.pack(side="left", fill="both", expand=True)
        m.sidebar_frame.pack(side="right", fill="y")
    else:
        m.sidebar_frame.pack(side="left", fill="y")
        m.main_area.pack(side="right", fill="both", expand=True)

    m.sidebar_title.pack_configure(anchor="e" if rtl else "w")
    try:
        m.sidebar_subtitle.pack_configure(anchor="e" if rtl else "w")
        m.sidebar_file_kinds.pack_configure(anchor="e" if rtl else "w")
        m.sidebar_file_kinds.configure(
            anchor="e" if rtl else "w",
            justify="right" if rtl else "left",
        )
    except Exception:
        pass

    try:
        m.page_title.configure(anchor="e" if rtl else "w")
        m.page_subtitle.configure(justify="right" if rtl else "left")
    except Exception:
        pass

    ctk_entry_justify(m.url_entry, "right" if rtl else "left")

    try:
        m.progress_label.configure(anchor="e" if rtl else "w")
        m.eta_label.configure(anchor="e" if rtl else "w")
    except Exception:
        pass

    try:
        m.hint_drop.configure(anchor="e" if rtl else "w")
        m.text_mid.pack_forget()
        m.queue_add_btn.pack_forget()
        m.count_badge.pack_forget()
        if rtl:
            m.queue_add_btn.pack(side="left", padx=(0, 10))
            m.count_badge.pack(side="left", padx=(0, 8))
            m.text_mid.pack(side="right", fill="both", expand=True)
        else:
            m.text_mid.pack(side="left", fill="both", expand=True)
            m.count_badge.pack(side="right", padx=(0, 8))
            m.queue_add_btn.pack(side="right", padx=(10, 0))
    except Exception:
        pass

    for _nav_row, _ind, _btn in (
        (m.nav_music_row, m.nav_music_indicator, m.nav_music_btn),
        (m.nav_history_row, m.nav_history_indicator, m.nav_history_btn),
    ):
        try:
            _ind.pack_forget()
            _btn.pack_forget()
            if rtl:
                _ind.pack(side="right", fill="y", padx=(0, 6), pady=8)
                _btn.pack(side="right", fill="both", expand=True, padx=(8, 4))
            else:
                _ind.pack(side="left", fill="y", padx=(6, 0), pady=8)
                _btn.pack(side="left", fill="both", expand=True, padx=(4, 8))
        except Exception:
            pass

    m.format_option.pack_forget()
    m.convert_btn.pack_forget()
    m.fmt_row_left.pack_forget()
    m.output_card.pack_forget()
    if rtl:
        m.fmt_row_left.pack(side="right")
        m.format_option.pack(side="right")
        m.convert_btn.pack(side="left")
        m.output_card.pack(side="right", fill="x", expand=True, padx=10)
    else:
        m.fmt_row_left.pack(side="left")
        m.format_option.pack(side="left")
        m.output_card.pack(side="left", fill="x", expand=True, padx=10)
        m.convert_btn.pack(side="right")

    m.out_lbl.configure(anchor="e" if rtl else "w")

    m.output_folder_entry.pack_forget()
    m.output_browse_btn.pack_forget()
    if rtl:
        m.output_browse_btn.pack(side="right")
        m.output_folder_entry.pack(side="right", fill="x", expand=True, padx=(0, 10))
    else:
        m.output_folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        m.output_browse_btn.pack(side="left")
    ctk_entry_justify(m.output_folder_entry, "right" if rtl else "left")

    m.history_title.pack_configure(anchor="e" if rtl else "w")
    m.history_sub.pack_configure(anchor="e" if rtl else "w", pady=(6, 0))
    try:
        m.history_clear_btn.pack_configure(anchor="e" if rtl else "w")
    except Exception:
        pass

    m.back_to_app_btn.pack_forget()
    if rtl:
        m.back_to_app_btn.pack(side="right", anchor="e")
    else:
        m.back_to_app_btn.pack(side="left", anchor="w")

    m.settings_head_row.pack_configure(fill="x")
    m.settings_scroll.pack_configure(fill="both", expand=True)

    m.settings_main_heading.pack_configure(anchor="e" if rtl else "w")
    m.audio_section_header.pack_configure(anchor="e" if rtl else "w")
    m.audio_sr_row.pack_configure(anchor="e" if rtl else "w")
    m.audio_bd_row.pack_configure(anchor="e" if rtl else "w")
    m.formats_header_row.pack_configure(anchor="e" if rtl else "w")
    m.embed_meta_check.pack_configure(anchor="e" if rtl else "w")
    m.normalize_check.pack_configure(anchor="e" if rtl else "w")
    m.pattern_header_row.pack_configure(anchor="e" if rtl else "w")
    m.pattern_advanced_check.pack_configure(anchor="e" if rtl else "w")
    for _pw in (
        m.pattern_preview_label,
        m.pattern_builder_frame,
        m.pattern_sep_row,
        m.pattern_hint_label,
        m.audio_pattern_entry,
    ):
        try:
            _pw.pack_configure(anchor="e" if rtl else "w")
        except Exception:
            pass
    m.split_format_check.pack_configure(anchor="e" if rtl else "w")
    m.video_row.pack_configure(anchor="e" if rtl else "w")
    try:
        m.pattern_preview_label.configure(justify="right" if rtl else "left")
        m.pattern_hint_label.configure(justify="right" if rtl else "left")
    except Exception:
        pass
    ctk_entry_justify(m.audio_pattern_entry, "right" if rtl else "left")
    m.lang_header_row.pack_configure(anchor="e" if rtl else "w")
    m.appearance_header_row.pack_configure(anchor="e" if rtl else "w")
    layout_settings_headers(rtl)
    try:
        m.settings_audio_title.configure(justify="right" if rtl else "left")
        m.formats_heading_label.configure(justify="right" if rtl else "left")
        m.pattern_label.configure(justify="right" if rtl else "left")
        m.settings_lang_heading.configure(justify="right" if rtl else "left")
        m.settings_screen_title.configure(justify="right" if rtl else "left")
    except Exception:
        pass

    m.lang_row.pack_configure(anchor="e" if rtl else "w", pady=(0, 20))
    m.theme_buttons_row.pack_configure(anchor="e" if rtl else "w", pady=(0, 12))

    m.lang_btn_he.pack_forget()
    m.lang_btn_en.pack_forget()
    if rtl:
        m.lang_btn_he.pack(side="right", padx=(12, 0))
        m.lang_btn_en.pack(side="right")
    else:
        m.lang_btn_he.pack(side="left", padx=(0, 12))
        m.lang_btn_en.pack(side="left")

    m.theme_btn_light.pack_forget()
    m.theme_btn_dark.pack_forget()
    if rtl:
        m.theme_btn_dark.pack(side="right", padx=(0, 16))
        m.theme_btn_light.pack(side="right")
    else:
        m.theme_btn_light.pack(side="left", padx=(0, 16))
        m.theme_btn_dark.pack(side="left")

    set_nav_active(m._active_main_tab)


def apply_all_texts() -> None:
    m = main_module()
    t = m.t
    m.nav_music_btn.configure(text=t("nav_music"))
    m.nav_history_btn.configure(text=t("nav_history"))
    m.sidebar_subtitle.configure(text=t("sidebar_tagline"))
    m.sidebar_settings_btn.configure(text=t("nav_settings"))
    m.page_title.configure(text=t("page_main_title"))
    m.page_subtitle.configure(text=t("page_subtitle"))
    m.url_entry.configure(placeholder_text=t("url_placeholder"))
    m.url_add_btn.configure(text=t("btn_add_paths"))
    m.queue_label.configure(text=t("queue_label"))
    m.hint_drop.configure(text=t("drag_hint"))
    m.hint_drop_sub.configure(text=t("drag_hint_sub"))
    m.queue_add_btn.configure(text=t("queue_add_tracks"))
    if not m.is_converting:
        m.convert_btn.configure(text=t("btn_convert"))
        m.sync_idle_progress_labels()
    m.fmt_lbl.configure(text=t("output_format"))
    m.out_lbl.configure(text=t("output_folder"))
    m.output_browse_btn.configure(text=t("browse_folder"))
    m.more_settings_btn.configure(text=t("more_settings"))
    m.history_title.configure(text=t("history_title"))
    m.history_sub.configure(text=t("history_sub"))
    m.settings_main_heading.configure(text=t("settings_main"))
    m.settings_audio_title.configure(text=t("settings_audio_section"))
    m.sr_label.configure(text=t("label_sample_rate"))
    m.bd_label.configure(text=t("label_bit_depth"))
    m.embed_meta_check.configure(text=t("settings_embed_meta"))
    m.normalize_check.configure(text=t("settings_normalize"))
    m.formats_heading_label.configure(text=t("settings_formats_heading"))
    m.pattern_label.configure(text=t("settings_name_pattern"))
    m.sep_label_widget.configure(text=t("pattern_sep_label"))
    m.pattern_advanced_check.configure(text=t("pattern_advanced"))
    m.pattern_hint_label.configure(text=t("settings_name_pattern_hint"))
    for i, pl in enumerate(m.pattern_part_row_labels):
        pl.configure(text=f'{t("pattern_slot_prefix")} {i + 1}')
    _labs = m._pat_labels()
    for slot_menu in m.pattern_slot_menus:
        slot_menu.configure(values=_labs)
    _pparts = m.audio_settings.get("name_pattern_parts") or []
    for i, slot_menu in enumerate(m.pattern_slot_menus):
        pid = _pparts[i] if i < len(_pparts) else "skip"
        slot_menu.set(t(f"pat_{pid}"))
    m._update_pattern_preview()
    m.split_format_check.configure(text=t("settings_split_format"))
    m.video_extract_check.configure(text=t("settings_video_extract"))
    m.settings_lang_heading.configure(text=t("settings_lang"))
    m.lang_btn_he.configure(text=t("lang_pick_he"))
    m.lang_btn_en.configure(text=t("lang_pick_en"))
    m.settings_screen_title.configure(text=t("settings_appearance"))
    m.back_to_app_btn.configure(text=t("btn_back"))
    m.theme_btn_light.configure(text=t("theme_light"))
    m.theme_btn_dark.configure(text=t("theme_dark"))
    m.update_ui_paths()
