"""Simple cutlist optimizer demo."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class CutlistOptimizer:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def load_parts(self):
        cur = dict_cursor(self.conn)
        cur.execute("SELECT id, part_length_inches FROM cut_parts ORDER BY part_length_inches DESC")
        parts = cur.fetchall()
        cur.close()
        return parts

    def load_materials(self):
        cur = dict_cursor(self.conn)
        cur.execute("SELECT id, length_inches FROM materials ORDER BY length_inches DESC")
        mats = cur.fetchall()
        cur.close()
        return mats

    def optimize(self):
        parts = self.load_parts()
        mats = self.load_materials()

        assignments: list[tuple[int, int]] = []
        for part in parts:
            for mat in mats:
                if mat["length_inches"] >= part["part_length_inches"]:
                    assignments.append((part["id"], mat["id"]))
                    mat["length_inches"] -= part["part_length_inches"]
                    break
        return assignments


if __name__ == "__main__":
    optimizer = CutlistOptimizer()
    results = optimizer.optimize()
    for part_id, mat_id in results:
        print(f"Part {part_id} cut from material {mat_id}")
