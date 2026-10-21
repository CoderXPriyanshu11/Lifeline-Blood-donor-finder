"""
db.py – LifeLine Blood Donor Finder
MySQL connection pool using mysql-connector-python.
All queries in the app use parameterized statements via this module.
"""
import mysql.connector
from mysql.connector import pooling, Error as MySQLError
from flask import current_app, g
from typing import Optional
import logging

logger = logging.getLogger(__name__)

_pool: Optional[pooling.MySQLConnectionPool] = None


def init_pool(app) -> None:
    """Create the connection pool once at application start-up."""
    global _pool
    cfg = app.config
    try:
        _pool = pooling.MySQLConnectionPool(
            pool_name=cfg["POOL_NAME"],
            pool_size=cfg["POOL_SIZE"],
            pool_reset_session=cfg["POOL_RESET_SESSION"],
            host=cfg["DB_HOST"],
            port=cfg["DB_PORT"],
            user=cfg["DB_USER"],
            password=cfg["DB_PASSWORD"],
            database=cfg["DB_NAME"],
            charset="utf8mb4",
            collation="utf8mb4_unicode_ci",
            use_unicode=True,
            autocommit=False,
        )
        logger.info("MySQL connection pool '%s' created (size=%d).",
                    cfg["POOL_NAME"], cfg["POOL_SIZE"])
    except MySQLError as exc:
        logger.error("Failed to create MySQL connection pool: %s", exc)
        raise


def get_db():
    """
    Return a connection attached to Flask's request context `g`.
    Reuses the connection if already opened for this request.
    """
    if "db" not in g:
        if _pool is None:
            raise RuntimeError("DB pool not initialised. Call init_pool(app) first.")
        g.db = _pool.get_connection()
    return g.db


def close_db(e=None) -> None:
    """Return the connection to the pool at the end of each request."""
    db = g.pop("db", None)
    if db is not None:
        try:
            db.close()
        except MySQLError:
            pass


# ── Convenience helpers ───────────────────────────────────────────────────────

def query(sql: str, params: tuple = (), fetchone: bool = False):
    """
    Execute a SELECT and return rows as dicts.
    Set fetchone=True to get a single dict (or None).
    """
    conn = get_db()
    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        return cur.fetchone() if fetchone else cur.fetchall()


def execute(sql: str, params: tuple = (), last_id: bool = False):
    """
    Execute an INSERT / UPDATE / DELETE inside a transaction.
    Returns lastrowid when last_id=True, otherwise rowcount.
    """
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(sql, params)
        conn.commit()
        return cur.lastrowid if last_id else cur.rowcount
