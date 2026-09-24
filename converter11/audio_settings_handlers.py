"""Persist checkbox / sample-rate / bit-depth changes from the settings screen."""

from converter11.config_io import save_audio_settings_disk
from converter11.ui_context import main_module


def audio_save_checkbox(widget, key: str) -> None:
    m = main_module()
    m.audio_settings[key] = widget.get() == 1
    save_audio_settings_disk()


def audio_save_sr(choice: str) -> None:
    m = main_module()
    m.audio_settings["sample_rate_hz"] = int(choice)
    save_audio_settings_disk()


def audio_save_bd(choice: str) -> None:
    m = main_module()
    m.audio_settings["pcm_bit_depth"] = choice
    save_audio_settings_disk()
