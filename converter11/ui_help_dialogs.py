"""Messagebox helpers for format/settings tooltips."""

from tkinter import messagebox

from converter11.ui_context import main_module


def show_format_help() -> None:
    m = main_module()
    messagebox.showinfo(m.t("format_help_title"), m.t("format_help_body"))


def show_settings_audio_help() -> None:
    m = main_module()
    body = (
        m.t("settings_audio_hint")
        + "\n\n"
        + m.t("mp3_quality_note")
        + "\n\n"
        + m.t("aac_quality_note")
    )
    messagebox.showinfo(m.t("help_audio_export_title"), body)


def show_settings_formats_help() -> None:
    m = main_module()
    detail = "\n\n".join(
        [
            m.t("fmt_wav"),
            m.t("fmt_mp3"),
            m.t("fmt_flac"),
            m.t("fmt_aiff"),
            m.t("fmt_m4a"),
        ]
    )
    messagebox.showinfo(
        m.t("format_help_title"), m.t("format_help_body") + "\n\n" + detail
    )


def show_settings_pattern_help() -> None:
    m = main_module()
    messagebox.showinfo(
        m.t("help_pattern_title"),
        m.t("settings_name_pattern_simple") + "\n\n" + m.t("settings_name_pattern_hint"),
    )


def show_settings_video_help() -> None:
    m = main_module()
    messagebox.showinfo(m.t("help_video_title"), m.t("settings_video_hint"))


def show_settings_lang_help() -> None:
    m = main_module()
    messagebox.showinfo(m.t("help_lang_title"), m.t("settings_lang_hint"))


def show_settings_appearance_help() -> None:
    m = main_module()
    messagebox.showinfo(
        m.t("help_appearance_title"), m.t("settings_appearance_hint")
    )


def nav_placeholder(title: str) -> None:
    m = main_module()
    messagebox.showinfo(m.t("window_title"), m.t("msg_coming", title=title))
