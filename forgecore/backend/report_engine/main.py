"""Reporting engine placeholder."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class ReportEngine:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def job_summary(self):
        cur = dict_cursor(self.conn)
        cur.execute("SELECT id, name FROM jobs")
        return cur.fetchall()


if __name__ == "__main__":
    re = ReportEngine()
    for job in re.job_summary():
        print(job)
