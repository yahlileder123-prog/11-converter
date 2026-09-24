"""Windows DPI / work-area sizing and clamp (no network)."""

import os

import ctypes
from ctypes import wintypes


def windows_set_dpi_awareness() -> None:
    if os.name != "nt":
        return
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass


def windows_apply_native_chrome(win, *, dark: bool) -> None:
    """Windows 10/11: dark title bar + rounded corners. Fails silently if unavailable."""
    if os.name != "nt":
        return
    hwnd = tk_top_hwnd(win)
    if not hwnd:
        return
    try:
        dwmapi = ctypes.windll.dwmapi
        pref = ctypes.c_int(1 if dark else 0)
        # 20 = DWMWA_USE_IMMERSIVE_DARK_MODE (Win10 1903+); 19 = older
        for attr in (20, 19):
            dwmapi.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(pref), ctypes.sizeof(pref))
        round_pref = ctypes.c_int(2)  # DWMWCP_ROUND
        dwmapi.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(round_pref), ctypes.sizeof(round_pref))
    except Exception:
        pass


def fit_window_to_work_area(win) -> None:
    """Size/position the window inside the primary monitor work area (above taskbar)."""
    if os.name != "nt":
        return
    try:

        class _RECT(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        rect = _RECT()
        SPI_GETWORKAREA = 48
        if ctypes.windll.user32.SystemParametersInfoW(
            SPI_GETWORKAREA, 0, ctypes.byref(rect), 0
        ):
            margin = 10
            wa_w = rect.right - rect.left - 2 * margin
            wa_h = rect.bottom - rect.top - 2 * margin
            if wa_w < 320 or wa_h < 240:
                return
            w = min(1120, wa_w)
            h = min(800, wa_h)
            w = max(w, min(800, wa_w))
            h = max(h, min(600, wa_h))
            x = rect.left + margin + max(0, (wa_w - w) // 2)
            y = rect.top + margin + max(0, (wa_h - h) // 2)
            win.geometry(f"{w}x{h}+{x}+{y}")
    except Exception:
        pass


def tk_top_hwnd(win) -> int:
    """Best-effort HWND for the Tk toplevel (Windows)."""
    if os.name != "nt":
        return 0
    try:
        tid = int(win.winfo_id())
        user32 = ctypes.windll.user32
        hwnd = int(user32.GetParent(tid))
        if not hwnd:
            hwnd = int(user32.GetAncestor(tid, 2))
        return hwnd
    except Exception:
        return 0


def windows_clamp_toplevel_to_work_area(win) -> None:
    """
    If the window rectangle drifts outside the current monitor's work area (e.g. taskbar
    overlap after DPI / monitor changes), move it back. Does not use topmost or steal focus.
    Skips maximized/minimized windows.
    """
    if os.name != "nt":
        return
    try:
        st = win.state()
        if st in ("iconic", "zoomed"):
            return
    except Exception:
        pass
    hwnd = tk_top_hwnd(win)
    if not hwnd:
        return
    try:
        user32 = ctypes.windll.user32
        wr = wintypes.RECT()
        if not user32.GetWindowRect(hwnd, ctypes.byref(wr)):
            return
        hmon = user32.MonitorFromWindow(hwnd, 2)
        if not hmon:
            return

        class MONITORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", wintypes.DWORD),
                ("rcMonitor", wintypes.RECT),
                ("rcWork", wintypes.RECT),
                ("dwFlags", wintypes.DWORD),
            ]

        mi = MONITORINFO()
        mi.cbSize = ctypes.sizeof(MONITORINFO)
        if not user32.GetMonitorInfoW(hmon, ctypes.byref(mi)):
            return
        work = mi.rcWork
        margin = 8
        ww = wr.right - wr.left
        wh = wr.bottom - wr.top
        minx = work.left + margin
        miny = work.top + margin
        maxx = work.right - margin - ww
        maxy = work.bottom - margin - wh
        left = wr.left
        top = wr.top
        if maxx < minx:
            left = work.left + margin
            ww = max(work.right - work.left - 2 * margin, 200)
        else:
            left = min(max(left, minx), maxx)
        if maxy < miny:
            top = work.top + margin
            wh = max(work.bottom - work.top - 2 * margin, 200)
        else:
            top = min(max(top, miny), maxy)
        user32.MoveWindow(hwnd, int(left), int(top), int(ww), int(wh), True)
    except Exception:
        pass


_clamp_scheduled_id = None


def schedule_clamp_toplevel_to_work_area(win) -> None:
    """Debounce clamp so monitor/DPI changes don't spam MoveWindow."""
    global _clamp_scheduled_id

    def _run():
        global _clamp_scheduled_id
        _clamp_scheduled_id = None
        windows_clamp_toplevel_to_work_area(win)

    try:
        if _clamp_scheduled_id is not None:
            win.after_cancel(_clamp_scheduled_id)
    except Exception:
        pass
    try:
        _clamp_scheduled_id = win.after(120, _run)
    except Exception:
        pass
