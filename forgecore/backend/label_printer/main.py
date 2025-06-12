"""Label printing utilities."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


class LabelPrinter:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def print_label(self, material_id: int, text: str) -> None:
        print(f"Printing label for material {material_id}: {text}")


if __name__ == "__main__":
    lp = LabelPrinter()
    lp.print_label(1, "Sample Material")
