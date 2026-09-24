"""Settings: export filename pattern — simple builder, advanced {tags} entry, preview."""

import re

from converter11.audio_engine import fill_export_filename
from converter11.config_io import save_audio_settings_disk
from converter11.constants import (
    PATTERN_PART_ORDER,
    PATTERN_PREVIEW_META,
    PATTERN_SEP_CHOICES,
    VALID_NAME_PARTS,
)
from converter11.naming import build_name_pattern_string, infer_sep_from_pattern
from converter11.ui_context import main_module


def pat_labels() -> list[str]:
    m = main_module()
    return [m.t(f"pat_{k}") for k in PATTERN_PART_ORDER]


def pat_id_from_label(label: str) -> str:
    m = main_module()
    for k in PATTERN_PART_ORDER:
        if m.t(f"pat_{k}") == label:
            return k
    return "skip"


def update_pattern_preview() -> None:
    m = main_module()
    pat = m.audio_settings.get("name_pattern") or "{title}"
    shown = fill_export_filename(pat, PATTERN_PREVIEW_META, "file")
    m.pattern_preview_label.configure(
        text=f'{m.t("pattern_preview_label")}: {shown}'
    )


def rebuild_pattern_from_builder() -> None:
    m = main_module()
    if m.audio_settings.get("name_pattern_advanced"):
        return
    parts = [pat_id_from_label(om.get()) for om in m.pattern_slot_menus]
    sep = m.pattern_sep_option.get()
    m.audio_settings["name_pattern_parts"] = parts
    m.audio_settings["name_pattern_sep"] = sep
    m.audio_settings["name_pattern"] = build_name_pattern_string(parts, sep)
    save_audio_settings_disk()
    update_pattern_preview()


def pattern_slot_cmd(_choice, idx: int) -> None:
    rebuild_pattern_from_builder()


def pattern_sep_cmd(_choice) -> None:
    rebuild_pattern_from_builder()


def save_name_pattern(_e=None) -> None:
    m = main_module()
    m.audio_settings["name_pattern"] = (
        m.audio_pattern_entry.get().strip() or "{artist} - {title}"
    )
    save_audio_settings_disk()
    update_pattern_preview()


def on_pattern_advanced_toggle() -> None:
    m = main_module()
    on = m.pattern_advanced_check.get() == 1
    if on:
        m.audio_settings["name_pattern_advanced"] = True
        m.pattern_preview_label.pack_forget()
        m.pattern_builder_frame.pack_forget()
        m.pattern_sep_row.pack_forget()
        m.pattern_hint_label.pack(anchor="w", pady=(0, 6))
        m.audio_pattern_entry.pack(anchor="w", pady=(0, 12))
        m.audio_pattern_entry.delete(0, "end")
        m.audio_pattern_entry.insert(
            0, m.audio_settings.get("name_pattern") or "{artist} - {title}"
        )
    else:
        raw = (m.audio_pattern_entry.get() or "").strip() or "{title}"
        tags = [
            x for x in re.findall(r"\{(\w+)\}", raw) if x in VALID_NAME_PARTS
        ][:4]
        while len(tags) < 4:
            tags.append("skip")
        m.audio_settings["name_pattern_parts"] = tags[:4]
        m.audio_settings["name_pattern_sep"] = infer_sep_from_pattern(raw)
        m.audio_settings["name_pattern_advanced"] = False
        sep_now = m.audio_settings["name_pattern_sep"]
        svals = list(PATTERN_SEP_CHOICES)
        if sep_now not in svals:
            svals = svals + [sep_now]
            m.pattern_sep_option.configure(values=svals)
        m.pattern_sep_option.set(sep_now)
        for i, slot in enumerate(m.pattern_slot_menus):
            slot.set(m.t(f"pat_{m.audio_settings['name_pattern_parts'][i]}"))
        m.pattern_hint_label.pack_forget()
        m.audio_pattern_entry.pack_forget()
        m.pattern_preview_label.pack(anchor="w", pady=(0, 6))
        m.pattern_builder_frame.pack(anchor="w", fill="x", pady=(0, 6))
        m.pattern_sep_row.pack(anchor="w", fill="x", pady=(0, 8))
        rebuild_pattern_from_builder()
    save_audio_settings_disk()
    update_pattern_preview()
