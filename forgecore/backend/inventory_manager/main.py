"""Inventory management utilities."""
from __future__ import annotations

import argparse
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

    def add_material(
        self,
        length_inches: int,
        source: str,
        is_remnant: bool = False,
        job_id: int | None = None,
    ) -> int:
        """Insert a new material record and return its id."""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO materials (length_inches, source, is_remnant, job_id)"
            " VALUES (%s,%s,%s,%s)",
            (length_inches, source, int(is_remnant), job_id),
        )
        self.conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id

    def assign_to_job(self, material_id: int, job_id: int) -> None:
        """Assign an existing material to a job."""
        cur = self.conn.cursor()
        cur.execute(
            "UPDATE materials SET job_id = %s WHERE id = %s",
            (job_id, material_id),
        )
        self.conn.commit()
        cur.close()

    def cut_material(self, material_id: int, cut_length: int, job_id: int | None = None) -> int:
        """Cut a length from a material.

        Returns the id of the created part record.
        """
        cur = dict_cursor(self.conn)
        cur.execute("SELECT length_inches FROM materials WHERE id = %s", (material_id,))
        row = cur.fetchone()
        if row is None:
            cur.close()
            raise ValueError("Material not found")
        if row["length_inches"] < cut_length:
            cur.close()
            raise ValueError("Cut length exceeds available length")

        remaining = row["length_inches"] - cut_length
        if remaining > 0:
            cur.execute(
                "UPDATE materials SET length_inches = %s, is_remnant = 1 WHERE id = %s",
                (remaining, material_id),
            )
        else:
            cur.execute("DELETE FROM materials WHERE id = %s", (material_id,))

        cur.execute(
            "INSERT INTO cut_parts (part_length_inches, material_id, job_id) VALUES (%s,%s,%s)",
            (cut_length, material_id, job_id),
        )
        part_id = cur.lastrowid
        self.conn.commit()
        cur.close()
        return part_id

    def remove_material(self, material_id: int) -> None:
        """Delete a material record."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM materials WHERE id = %s", (material_id,))
        self.conn.commit()
        cur.close()

    def total_length(self, remnants_only: bool = False) -> int:
        """Return the total available length in inches."""
        cur = dict_cursor(self.conn)
        if remnants_only:
            cur.execute("SELECT SUM(length_inches) AS total FROM materials WHERE is_remnant = 1")
        else:
            cur.execute("SELECT SUM(length_inches) AS total FROM materials")
        row = cur.fetchone()
        cur.close()
        return int(row["total"] or 0)


def cli() -> None:
    parser = argparse.ArgumentParser(description="Manage inventory records")
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_p = sub.add_parser("list", help="List materials")
    list_p.add_argument("--remnants", action="store_true", help="Show only remnants")

    add_p = sub.add_parser("add", help="Add a new material")
    add_p.add_argument("length", type=int, help="Length in inches")
    add_p.add_argument("source", help="Source description")
    add_p.add_argument("--remnant", action="store_true", help="Mark as remnant")
    add_p.add_argument("--job", type=int, default=None, help="Associated job id")

    assign_p = sub.add_parser("assign", help="Assign material to job")
    assign_p.add_argument("material_id", type=int)
    assign_p.add_argument("job_id", type=int)

    del_p = sub.add_parser("remove", help="Remove a material")
    del_p.add_argument("material_id", type=int)

    cut_p = sub.add_parser("cut", help="Cut a length from a material")
    cut_p.add_argument("material_id", type=int)
    cut_p.add_argument("length", type=int, help="Length to cut in inches")
    cut_p.add_argument("--job", type=int, default=None, help="Associated job id")

    stats_p = sub.add_parser("stats", help="Show total available length")
    stats_p.add_argument("--remnants", action="store_true", help="Only count remnants")

    args = parser.parse_args()
    inv = InventoryManager()

    if args.cmd == "list":
        items = inv.list_stock(remnants_only=args.remnants)
        for item in items:
            print(item)
    elif args.cmd == "add":
        new_id = inv.add_material(
            args.length, args.source, is_remnant=args.remnant, job_id=args.job
        )
        print(f"Inserted material {new_id}")
    elif args.cmd == "assign":
        inv.assign_to_job(args.material_id, args.job_id)
        print("Assignment complete")
    elif args.cmd == "remove":
        inv.remove_material(args.material_id)
        print("Material removed")
    elif args.cmd == "cut":
        part_id = inv.cut_material(args.material_id, args.length, job_id=args.job)
        print(f"Recorded cut part {part_id}")
    elif args.cmd == "stats":
        total = inv.total_length(remnants_only=args.remnants)
        print(f"Total length: {total} inches")


if __name__ == "__main__":
    cli()
