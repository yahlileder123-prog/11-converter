"""CustomTkinter entry helpers (selection, RTL/LTR alignment)."""


def ctk_entry_justify(widget, side: str) -> None:
    """side: 'left' or 'right' (text alignment inside CTkEntry)."""
    try:
        widget.configure(justify=side)
    except Exception:
        pass
    inner = getattr(widget, "_entry", None)
    if inner is not None:
        try:
            inner.configure(justify=side)
        except Exception:
            pass


def wire_entry_text_selection(widget) -> None:
    """Allow select / Ctrl+A / copy in CTkEntry (including readonly path fields)."""
    inner = getattr(widget, "_entry", None)
    if inner is None:
        return
    try:
        inner.configure(exportselection=True)
    except Exception:
        pass

    def _select_all(_e=None):
        try:
            inner.selection_range(0, "end")
            inner.icursor("end")
        except Exception:
            pass
        return "break"

    for seq in ("<Control-a>", "<Control-A>"):
        try:
            widget.bind(seq, _select_all)
            inner.bind(seq, _select_all)
        except Exception:
            pass
