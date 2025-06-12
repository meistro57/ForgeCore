"""Database configuration and connection helpers for ForgeCore."""

from __future__ import annotations

import os
from typing import Any

import mysql.connector
from mysql.connector import pooling


class DBConfig:
    """Loads database credentials from environment variables and manages
    a connection pool for reuse across modules.
    """

    def __init__(self) -> None:
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_user = os.getenv("DB_USER", "forgecore")
        self.db_password = os.getenv("DB_PASSWORD", "")
        self.db_name = os.getenv("DB_NAME", "forgecore")
        self._pool: pooling.MySQLConnectionPool | None = None

    def init_pool(self, pool_name: str = "forgecore_pool", size: int = 3) -> None:
        """Initializes a MySQL connection pool."""
        if self._pool is None:
            self._pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=size,
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name,
                autocommit=True,
            )

    def get_connection(self) -> mysql.connector.MySQLConnection:
        """Returns a pooled database connection."""
        if self._pool is None:
            self.init_pool()
        assert self._pool is not None
        return self._pool.get_connection()


# Singleton configuration used by all modules
config = DBConfig()
