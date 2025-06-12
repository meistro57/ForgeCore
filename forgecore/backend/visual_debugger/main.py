"""Placeholder visual debugger."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class VisualDebugger:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def summarize_jobs(self):
        cur = dict_cursor(self.conn)
        cur.execute("SELECT id, name FROM jobs")
        jobs = cur.fetchall()
        cur.close()
        for job in jobs:
            print(f"Job {job['id']}: {job['name']}")


if __name__ == "__main__":
    vd = VisualDebugger()
    vd.summarize_jobs()
