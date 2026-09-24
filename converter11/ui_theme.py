"""Theme, navigation, and appearance for the main window."""

from converter11.constants import APPEARANCE_FILE
from converter11.ui_context import main_module
from converter11.ui_palette import FONTS, palette


def accent_hover() -> str:
    return "#E56F00"



def apply_theme(mode: str) -> None:
    m = main_module()
    m.current_appearance = mode
    p = palette(mode)
    ac = m.brand_color

    m.app.configure(bg=p["window"])

    m.sidebar_frame.configure(fg_color=p["sidebar"])
    m.sidebar_title.configure(text_color=p["text"])
    m.sidebar_subtitle.configure(text_color=p["muted"], fg_color=p["sidebar"])
    m.sidebar_divider.configure(fg_color=p["border"])
    m.sidebar_file_kinds.configure(text_color=p["muted"], fg_color=p["surface"])
    m.sidebar_spacer.configure(fg_color=p["sidebar"])
    m.sidebar_bottom.configure(fg_color=p["sidebar"])
    m.sidebar_settings_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )

    set_nav_active(m._active_main_tab)

    m.main_area.configure(fg_color=p["window"])
    m.music_page.configure(fg_color=p["window"])
    m.history_page.configure(fg_color=p["window"])
    m.music_upper.configure(fg_color=p["window"])
    m.top_header_row.configure(fg_color=p["window"])
    m.url_row_frame.configure(fg_color=p["window"])
    m.queue_section.configure(fg_color=p["window"])
    m.middle_scroll.configure(fg_color=p["window"])
    m.queue_card.configure(fg_color=p["surface"], border_color=p["border"])
    try:
        m.queue_header_row.configure(fg_color=p["surface"])
    except Exception:
        pass
    m.drop_zone.configure(fg_color=p["drop_zone"], border_color=p["drop_zone_border"])
    m.queue_drop_row.configure(fg_color=p["drop_zone"])
    m.text_mid.configure(fg_color=p["drop_zone"])
    m.bottom_action_bar.configure(fg_color=p["window"])
    m.status_card.configure(fg_color=p["surface"], border_color=p["border"])
    m.status_inner.configure(fg_color=p["surface"])
    m.bottom_fmt_row.configure(fg_color=p["surface"])
    m.fmt_row_left.configure(fg_color=p["surface"])
    m.output_card.configure(fg_color=p["surface"], border_color=p["surface"])
    m.output_entry_row.configure(fg_color=p["surface"])
    m.history_header.configure(fg_color=p["window"])

    m.page_title.configure(text_color=p["text"])
    m.page_subtitle.configure(text_color=p["muted"])

    m.url_entry.configure(
        fg_color=p["input_bg"],
        text_color=p["text"],
        border_color=p["border"],
        placeholder_text_color=p["subtle"],
    )
    m.url_add_btn.configure(fg_color=ac, hover_color=accent_hover())

    m.queue_label.configure(text_color=p["subtle"])
    m.track_queue_scroll.configure(
        fg_color=p["surface"],
        scrollbar_button_color=p["border"],
        scrollbar_button_hover_color=p["subtle"],
    )

    m.drag_illustration.configure(text_color=ac)
    m.hint_drop.configure(text_color=p["muted"])
    m.hint_drop_sub.configure(text_color=p["muted"])
    m.queue_add_btn.configure(fg_color=ac, hover_color=accent_hover(), text_color="white")
    m.count_badge.configure(fg_color=p["surface"], text_color=p["muted"])

    m.progress_label.configure(text_color=p["text"])
    m.progress_bar.configure(fg_color=p["progress_trough"], progress_color=ac)
    m.eta_label.configure(text_color=p["muted"])
    m.convert_btn.configure(fg_color=ac, hover_color=accent_hover(), text_color="white")

    m.fmt_lbl.configure(text_color=p["muted"])
    m.format_help_btn.configure(
        fg_color=p["btn_neutral"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_width=0,
    )
    m.format_option.configure(
        fg_color=p["btn_neutral"],
        button_color=ac,
        button_hover_color=accent_hover(),
        text_color=p["text"],
        dropdown_fg_color=p["surface"],
        dropdown_hover_color=p["btn_neutral_hover"],
        dropdown_text_color=p["text"],
    )
    m.out_lbl.configure(text_color=p["subtle"])
    m.output_folder_entry.configure(
        fg_color=p["input_bg"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.output_browse_btn.configure(
        fg_color=p["btn_neutral"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_width=0,
    )
    m.more_settings_btn.configure(
        fg_color=p["btn_neutral"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_width=0,
    )

    m.history_title.configure(text_color=p["text"])
    m.history_sub.configure(text_color=p["muted"])

    m.view_home.configure(fg_color=p["window"])
    m.view_settings.configure(fg_color=p["window"])
    m.settings_inner.configure(fg_color=p["window"])
    m.settings_scroll.configure(fg_color=p["window"])
    m.theme_buttons_row.configure(fg_color=p["window"])
    m.settings_head_row.configure(fg_color=p["window"])

    m.settings_main_heading.configure(text_color=p["text"])
    m.settings_audio_title.configure(text_color=p["text"])
    m.audio_section_header.configure(fg_color=p["window"])
    m.settings_audio_help_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_active"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
    )
    m.sr_label.configure(text_color=p["text"])
    m.bd_label.configure(text_color=p["text"])
    m.sample_rate_option.configure(
        fg_color=p["surface"],
        button_color=ac,
        button_hover_color=accent_hover(),
        text_color=p["text"],
        dropdown_fg_color=p["surface"],
        dropdown_hover_color=p["btn_neutral_hover"],
        dropdown_text_color=p["text"],
    )
    m.bit_depth_option.configure(
        fg_color=p["surface"],
        button_color=ac,
        button_hover_color=accent_hover(),
        text_color=p["text"],
        dropdown_fg_color=p["surface"],
        dropdown_hover_color=p["btn_neutral_hover"],
        dropdown_text_color=p["text"],
    )
    m.embed_meta_check.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.normalize_check.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.formats_header_row.configure(fg_color=p["window"])
    m.formats_heading_label.configure(text_color=p["text"])
    m.formats_help_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_active"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
    )
    m.pattern_header_row.configure(fg_color=p["window"])
    m.pattern_label.configure(text_color=p["text"])
    m.pattern_help_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_active"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
    )
    m.pattern_preview_label.configure(text_color=p["text"])
    m.pattern_hint_label.configure(text_color=p["muted"])
    m.audio_pattern_entry.configure(
        fg_color=p["input_bg"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.sep_label_widget.configure(text_color=p["text"])
    for _pl in m.pattern_part_row_labels:
        _pl.configure(text_color=p["text"])
    m.pattern_builder_frame.configure(fg_color=p["window"])
    m.pattern_sep_row.configure(fg_color=p["window"])
    for _pm in m.pattern_slot_menus:
        _pm.configure(
            fg_color=p["surface"],
            button_color=ac,
            button_hover_color=accent_hover(),
            text_color=p["text"],
            dropdown_fg_color=p["surface"],
            dropdown_hover_color=p["btn_neutral_hover"],
            dropdown_text_color=p["text"],
        )
    m.pattern_sep_option.configure(
        fg_color=p["surface"],
        button_color=ac,
        button_hover_color=accent_hover(),
        text_color=p["text"],
        dropdown_fg_color=p["surface"],
        dropdown_hover_color=p["btn_neutral_hover"],
        dropdown_text_color=p["text"],
    )
    m.pattern_advanced_check.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.split_format_check.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.video_extract_check.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.video_row.configure(fg_color=p["window"])
    m.video_help_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_active"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
    )
    m.lang_header_row.configure(fg_color=p["window"])
    m.lang_help_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_active"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
    )
    m.appearance_header_row.configure(fg_color=p["window"])
    m.appearance_help_btn.configure(
        fg_color=p["surface"],
        hover_color=p["nav_active"],
        text_color=p["text"],
        border_width=1,
        border_color=p["border"],
    )
    m.audio_sr_row.configure(fg_color=p["window"])
    m.audio_bd_row.configure(fg_color=p["window"])
    m.settings_lang_heading.configure(text_color=p["text"])
    m.lang_btn_he.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=ac,
    )
    m.lang_btn_en.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=ac,
    )
    m.settings_screen_title.configure(text_color=p["text"])
    m.back_to_app_btn.configure(
        fg_color=p["btn_neutral"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=p["border"],
    )
    m.theme_btn_light.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=ac,
    )
    m.theme_btn_dark.configure(
        fg_color=p["surface"],
        hover_color=p["btn_neutral_hover"],
        text_color=p["text"],
        border_color=ac,
    )

    from converter11.track_queue import sync_sidebar_format_panel
    from converter11.win_geometry import windows_apply_native_chrome

    sync_sidebar_format_panel()
    windows_apply_native_chrome(m.app, dark=(mode == "dark"))
    # Avoid heavy rebuilds here; those can make screen switches feel laggy.
    # Queue/history tables are rebuilt only when their underlying data changes.



def set_nav_active(which: str) -> None:
    m = main_module()
    m._active_main_tab = which
    p = palette(m.current_appearance)
    ac = m.brand_color
    na = "e" if m.layout_rtl() else "w"

    nav_items = (
        ("music", m.nav_music_btn, m.nav_music_indicator, m.nav_music_row),
        ("history", m.nav_history_btn, m.nav_history_indicator, m.nav_history_row),
    )
    for key, btn, indicator, row in nav_items:
        active = which == key
        btn.configure(
            anchor=na,
            font=FONTS["nav_active"] if active else FONTS["nav"],
            fg_color=p["nav_active"] if active else p["sidebar"],
            hover_color=p["nav_hover"],
            text_color=p["text"] if active else p["muted"],
        )
        row.configure(fg_color=p["nav_active"] if active else p["sidebar"])
        indicator.configure(fg_color=ac if active else p["sidebar"])


def show_music_page() -> None:
    m = main_module()
    m.history_page.pack_forget()
    m.music_page.pack(fill="both", expand=True)
    set_nav_active("music")



def show_history_page() -> None:
    m = main_module()
    if m.is_converting:
        return
    m.music_page.pack_forget()
    m.history_page.pack(fill="both", expand=True)
    set_nav_active("history")
    if getattr(m, "history_dirty", True):
        m.rebuild_history_page()
        m.history_dirty = False



def pick_theme_and_save(mode: str) -> None:
    m = main_module()
    m.save_config(APPEARANCE_FILE, mode)
    apply_theme(mode)

