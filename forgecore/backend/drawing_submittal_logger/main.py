"""Command line utilities for logging drawing submittals."""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class DrawingSubmittalLogger:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def list_submittals(self):
        cur = dict_cursor(self.conn)
        cur.execute(
            "SELECT id, drawing_number, job_number, description, submitted_by, submission_date, status, created_at "
            "FROM drawing_submittals ORDER BY submission_date DESC"
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def log_submittal(
        self,
        drawing_number: str,
        job_number: str,
        submitted_by: str,
        description: str | None = None,
        submission_date: str | None = None,
        status: str = "Submitted",
    ) -> int:
        date_val = submission_date or datetime.date.today().isoformat()
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO drawing_submittals (drawing_number, job_number, description, submitted_by, submission_date, status) "
            "VALUES (%s,%s,%s,%s,%s,%s)",
            (drawing_number, job_number, description, submitted_by, date_val, status),
        )
        self.conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id


def cli() -> None:
    parser = argparse.ArgumentParser(description="Log drawing submittals")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List drawing submittals")

    add_p = sub.add_parser("add", help="Record a new drawing submittal")
    add_p.add_argument("drawing_number")
    add_p.add_argument("job_number")
    add_p.add_argument("submitted_by")
    add_p.add_argument("--description", default=None)
    add_p.add_argument("--date", default=None, help="Submission date YYYY-MM-DD")
    add_p.add_argument("--status", default="Submitted")

    args = parser.parse_args()
    dsl = DrawingSubmittalLogger()

    if args.cmd == "list":
        for row in dsl.list_submittals():
            print(row)
    elif args.cmd == "add":
        sid = dsl.log_submittal(
            args.drawing_number,
            args.job_number,
            args.submitted_by,
            description=args.description,
            submission_date=args.date,
            status=args.status,
        )
        print(f"Recorded submittal {sid}")


if __name__ == "__main__":
    cli()
