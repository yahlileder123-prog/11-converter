"""
11 CONVERTER — start here.

    python main.py

Starts the same UI as running `app.py` directly.
"""

from pathlib import Path
import runpy


def main() -> None:
    root = Path(__file__).resolve().parent
    runpy.run_path(str(root / "app.py"), run_name="__main__")


if __name__ == "__main__":
    main()
