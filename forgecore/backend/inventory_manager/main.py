"""Inventory management utilities."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class InventoryManager:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def list_stock(self, remnants_only: bool = False):
        cur = dict_cursor(self.conn)
        if remnants_only:
            cur.execute("SELECT * FROM materials WHERE is_remnant = 1")
        else:
            cur.execute("SELECT * FROM materials")
        materials = cur.fetchall()
        cur.close()
        return materials


if __name__ == "__main__":
    inv = InventoryManager()
    for item in inv.list_stock():
        print(item)
