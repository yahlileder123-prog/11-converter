"""Access the running Tk application module (populated as `converter_main`)."""

import sys
from types import ModuleType


def main_module() -> ModuleType:
    mod = sys.modules.get("converter_main") or sys.modules.get("__main__")
    if mod is None:
        raise RuntimeError("Application module not loaded (converter_main not registered).")
    return mod
