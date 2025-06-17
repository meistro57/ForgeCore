"""Customer management utilities."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2] / "config"))

from config import config


def dict_cursor(conn):
    return conn.cursor(dictionary=True)


class CustomerManager:
    def __init__(self) -> None:
        self.conn = config.get_connection()

    def list_customers(self):
        cur = dict_cursor(self.conn)
        cur.execute(
            "SELECT id, name, email, phone, address, created_at FROM customers ORDER BY created_at DESC"
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def add_customer(
        self,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        address: str | None = None,
    ) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO customers (name, email, phone, address) VALUES (%s,%s,%s,%s)",
            (name, email, phone, address),
        )
        self.conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id


def cli() -> None:
    parser = argparse.ArgumentParser(description="Manage customer records")
    sub = parser.add_subparsers(dest="cmd", required=True)

    list_p = sub.add_parser("list", help="List customers")

    add_p = sub.add_parser("add", help="Add a new customer")
    add_p.add_argument("name", help="Customer name")
    add_p.add_argument("--email", default=None, help="Email address")
    add_p.add_argument("--phone", default=None, help="Phone number")
    add_p.add_argument("--address", default=None, help="Street address")

    args = parser.parse_args()
    cm = CustomerManager()

    if args.cmd == "list":
        customers = cm.list_customers()
        for cust in customers:
            print(cust)
    elif args.cmd == "add":
        cid = cm.add_customer(args.name, email=args.email, phone=args.phone, address=args.address)
        print(f"Inserted customer {cid}")


if __name__ == "__main__":
    cli()
