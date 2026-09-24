"""Theme color maps and simple file-size formatting."""

import os

# Shared typography (Segoe UI is native on Windows; falls back cleanly elsewhere).
FONTS = {
    "brand": ("Segoe UI", 22, "bold"),
    "brand_sub": ("Segoe UI", 11),
    "page_title": ("Segoe UI", 26, "bold"),
    "page_sub": ("Segoe UI", 13),
    "section": ("Segoe UI", 11, "bold"),
    "body": ("Segoe UI", 13),
    "body_sm": ("Segoe UI", 12),
    "caption": ("Segoe UI", 11),
    "nav": ("Segoe UI", 14),
    "nav_active": ("Segoe UI", 14, "bold"),
    "btn": ("Segoe UI", 13, "bold"),
    "btn_primary": ("Segoe UI", 14, "bold"),
    "table_head": ("Segoe UI", 12, "bold"),
    "table_cell": ("Segoe UI", 12),
}

RADII = {"sm": 6, "md": 10, "lg": 12, "xl": 14}


def palette(mode: str) -> dict:
    if mode == "light":
        return {
            "window": "#eef1f6",
            "sidebar": "#ffffff",
            "surface": "#ffffff",
            "surface2": "#f8fafc",
            "border": "#d1d9e6",
            "text": "#0f172a",
            "muted": "#64748b",
            "subtle": "#94a3b8",
            "btn_neutral": "#eef2f7",
            "btn_neutral_hover": "#e2e8f0",
            "progress_trough": "#dbeafe",
            "drag_inner": "#f1f5f9",
            "input_bg": "#ffffff",
            "nav_active": "#f1f5f9",
            "nav_hover": "#e8edf3",
            "table_head": "#eef2f7",
            "table_row": "#ffffff",
            "table_row_alt": "#f8fafc",
            "table_grid": "#cbd5e1",
            "drop_zone": "#f8fafc",
            "drop_zone_border": "#cbd5e1",
            "drop_zone_hover": "#eef2f7",
            "accent_soft": "#fff4eb",
        }
    return {
        "window": "#0c0c0e",
        "sidebar": "#111114",
        "surface": "#18181c",
        "surface2": "#1e1e24",
        "border": "#2a2a32",
        "text": "#f4f4f5",
        "muted": "#a1a1aa",
        "subtle": "#71717a",
        "btn_neutral": "#222228",
        "btn_neutral_hover": "#2a2a32",
        "progress_trough": "#2a2a32",
        "drag_inner": "#1a1a20",
        "input_bg": "#141418",
        "nav_active": "#1e1e24",
        "nav_hover": "#222228",
        "table_head": "#141418",
        "table_row": "#1a1a20",
        "table_row_alt": "#1e1e26",
        "table_grid": "#2a2a32",
        "drop_zone": "#141418",
        "drop_zone_border": "#33333d",
        "drop_zone_hover": "#1a1a22",
        "accent_soft": "#2a1f14",
    }


def get_total_size(files) -> str:
    total_bytes = sum(os.path.getsize(f) for f in files)
    mb = total_bytes / (1024 * 1024)
    return f"{mb:.1f} MB"
