"""Basic job tracking functions."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class JobTracker:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def list_jobs(self):
        cur = dict_cursor(self.conn)
        cur.execute("SELECT id, name, created_at FROM jobs ORDER BY created_at DESC")
        jobs = cur.fetchall()
        cur.close()
        return jobs


if __name__ == "__main__":
    jt = JobTracker()
    for job in jt.list_jobs():
        print(job)
