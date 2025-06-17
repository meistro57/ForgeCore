"""CSV inventory import utility."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config
from inventory_manager.main import InventoryManager


class CSVImporter:
    def __init__(self) -> None:
        self.inv = InventoryManager()

    def import_file(self, filepath: str) -> int:
        """Import materials from a CSV file.

        The CSV must contain a header with at least a ``length`` column.
        Optional columns: ``source``, ``is_remnant`` and ``job_id``.
        Returns the number of inserted records.
        """
        count = 0
        with open(filepath, newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                try:
                    length = int(row["length"])
                except (KeyError, ValueError) as exc:
                    raise ValueError("length column required and must be int") from exc
                source = row.get("source", "")
                is_remnant_str = row.get("is_remnant", "0").strip().lower()
                is_remnant = is_remnant_str in {"1", "true", "yes", "y"}
                job_id = row.get("job_id")
                job_id_int = int(job_id) if job_id not in (None, "") else None
                self.inv.add_material(length, source, is_remnant=is_remnant, job_id=job_id_int)
                count += 1
        return count


def cli() -> None:
    parser = argparse.ArgumentParser(description="Import inventory from CSV")
    parser.add_argument("csvfile", help="Path to CSV file")
    args = parser.parse_args()
    importer = CSVImporter()
    num = importer.import_file(args.csvfile)
    print(f"Imported {num} materials")


if __name__ == "__main__":
    cli()
