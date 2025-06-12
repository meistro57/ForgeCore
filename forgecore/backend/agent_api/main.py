"""Internal API placeholder for AI agents."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class AgentAPI:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def list_drawings(self):
        cur = dict_cursor(self.conn)
        cur.execute("SELECT id, filename, parsed FROM drawings")
        drawings = cur.fetchall()
        cur.close()
        return drawings


if __name__ == "__main__":
    api = AgentAPI()
    for d in api.list_drawings():
        print(d)
