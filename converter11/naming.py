"""Exported filename pattern migration and building."""

import re

from converter11.constants import VALID_NAME_PARTS


def build_name_pattern_string(parts: list, sep: str) -> str:
    tags = []
    for p in parts:
        if p != "skip" and p in VALID_NAME_PARTS:
            tags.append("{" + p + "}")
    return sep.join(tags) if tags else "{title}"


def infer_sep_from_pattern(raw: str) -> str:
    valid_ms = []
    for m in re.finditer(r"\{(\w+)\}", raw):
        if m.group(1) in VALID_NAME_PARTS:
            valid_ms.append(m)
    if len(valid_ms) < 2:
        return " - "
    gap = raw[valid_ms[0].end() : valid_ms[1].start()]
    return gap if gap.strip() else " - "


def migrate_audio_name_pattern(st: dict) -> None:
    raw = (st.get("name_pattern") or "{artist} - {title}").strip()
    ver = int(st.get("name_pattern_format_version") or 1)

    if ver < 2:
        tags = [x for x in re.findall(r"\{(\w+)\}", raw) if x in VALID_NAME_PARTS][:4]
        while len(tags) < 4:
            tags.append("skip")
        st["name_pattern_parts"] = tags[:4]
        st["name_pattern_sep"] = st.get("name_pattern_sep") or infer_sep_from_pattern(raw)
        rebuilt = build_name_pattern_string(st["name_pattern_parts"], st["name_pattern_sep"])
        st["name_pattern_advanced"] = rebuilt.strip() != raw.strip()
        if not st["name_pattern_advanced"]:
            st["name_pattern"] = rebuilt
        st["name_pattern_format_version"] = 2
        return

    parts = st.get("name_pattern_parts")
    if not isinstance(parts, list):
        parts = ["artist", "title", "skip", "skip"]
    cleaned = []
    for p in parts[:4]:
        if p == "skip" or p in VALID_NAME_PARTS:
            cleaned.append(p)
        else:
            cleaned.append("skip")
    while len(cleaned) < 4:
        cleaned.append("skip")
    st["name_pattern_parts"] = cleaned[:4]
    if not st.get("name_pattern_sep"):
        st["name_pattern_sep"] = " - "
    if st.get("name_pattern_advanced"):
        return
    st["name_pattern"] = build_name_pattern_string(
        st["name_pattern_parts"], st["name_pattern_sep"]
    )
