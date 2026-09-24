"""Path display and safe folder naming (no GUI)."""

from pathlib import Path


def desktop_path() -> str:
    home = Path.home()
    for rel in ("Desktop", "שולחן עבודה", "OneDrive/Desktop", "OneDrive/שולחן עבודה"):
        p = home / rel
        if p.is_dir():
            return str(p)
    return str(home)


def shorten_path(path: str, max_len: int = 36) -> str:
    if not path or path == "NOT SET":
        return path
    norm = path.replace("\\", "/")
    if len(norm) <= max_len:
        return norm
    return "…" + norm[-(max_len - 1) :]


def sanitize_folder_name(name: str) -> str:
    for c in '<>:"/\\|?*':
        name = name.replace(c, "_")
    name = name.strip()
    return name if name else "11_Export"
