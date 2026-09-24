"""Hover, progress easing, and other motion helpers (local UI only)."""

from __future__ import annotations


def bind_surface_hover(widgets: list, idle: str, hover: str) -> None:
    """Highlight a group of frames as one surface; nested Enter/Leave is counted."""
    state = {"n": 0}

    def paint(color: str) -> None:
        for w in widgets:
            try:
                w.configure(fg_color=color)
            except Exception:
                pass

    def enter(_e=None) -> None:
        state["n"] += 1
        if state["n"] == 1:
            paint(hover)

    def leave(_e=None) -> None:
        state["n"] = max(0, state["n"] - 1)
        if state["n"] == 0:
            paint(idle)

    for w in widgets:
        try:
            w.bind("<Enter>", enter, add="+")
            w.bind("<Leave>", leave, add="+")
        except Exception:
            pass


def animate_progress(win, bar, state: dict, target: float, *, snap: bool = False) -> None:
    """Ease the progress bar toward target (~60fps). snap=True jumps immediately."""
    state["target"] = max(0.0, min(1.0, float(target)))
    if snap:
        if state.get("id") is not None:
            try:
                win.after_cancel(state["id"])
            except Exception:
                pass
            state["id"] = None
        state["shown"] = state["target"]
        try:
            bar.set(state["shown"])
        except Exception:
            pass
        return

    def tick() -> None:
        shown = float(state.get("shown") or 0.0)
        tgt = float(state.get("target") or 0.0)
        diff = tgt - shown
        if abs(diff) < 0.003:
            state["shown"] = tgt
            try:
                bar.set(tgt)
            except Exception:
                pass
            state["id"] = None
            return
        shown += diff * 0.26
        state["shown"] = shown
        try:
            bar.set(shown)
        except Exception:
            pass
        try:
            state["id"] = win.after(16, tick)
        except Exception:
            state["id"] = None

    if state.get("id") is None:
        try:
            state["id"] = win.after(16, tick)
        except Exception:
            state["id"] = None
            try:
                bar.set(state["target"])
            except Exception:
                pass
