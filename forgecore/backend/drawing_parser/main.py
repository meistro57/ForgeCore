"""Simulated drawing parser."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


class DrawingParser:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def parse(self, filepath: str) -> int:
        # Dummy parser that pretends every drawing has a single 120" cut
        length = 120
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO drawings (job_id, filename, parsed, flagged) VALUES (%s,%s,%s,%s)",
            (1, os.path.basename(filepath), 1, 0),
        )
        self.conn.commit()
        cur.close()
        print(f"Parsed {filepath} -> found part length {length} inches")
        return length


def cli() -> None:
    parser = argparse.ArgumentParser(description="Parse a drawing file")
    parser.add_argument("filepath")
    args = parser.parse_args()
    dp = DrawingParser()
    dp.parse(args.filepath)


if __name__ == "__main__":
    cli()
