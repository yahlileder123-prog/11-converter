"""Switch between main (music/history) and settings views."""

from converter11.ui_context import main_module
from converter11.ui_theme import show_history_page, show_music_page


def show_home_view() -> None:
    m = main_module()
    m.view_settings.pack_forget()
    m.view_home.pack(fill="both", expand=True)
    if m._active_main_tab == "history":
        show_history_page()
    else:
        show_music_page()


def show_settings_view() -> None:
    m = main_module()
    if m.is_converting:
        return
    m.view_home.pack_forget()
    m.view_settings.pack(fill="both", expand=True)
