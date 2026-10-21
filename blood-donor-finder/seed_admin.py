"""
seed_admin.py – LifeLine Blood Donor Finder
Creates or updates the default admin account.
Run once after setting up the database:
    python seed_admin.py
"""
import os
import sys
import mysql.connector
from werkzeug.security import generate_password_hash

# ── Config ────────────────────────────────────────────────────────────────────
DB_HOST     = os.environ.get("DB_HOST", "localhost")
DB_PORT     = int(os.environ.get("DB_PORT", 3306))
DB_USER     = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME     = os.environ.get("DB_NAME", "blood_donor_finder")

ADMIN_USERNAME  = "admin"
ADMIN_PASSWORD  = "Admin@123"
ADMIN_FULL_NAME = "LifeLine Administrator"

# ── Run ───────────────────────────────────────────────────────────────────────
def main():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset="utf8mb4",
        )
    except mysql.connector.Error as exc:
        print(f"[ERROR] Cannot connect to MySQL: {exc}", file=sys.stderr)
        sys.exit(1)

    hashed = generate_password_hash(ADMIN_PASSWORD)

    with conn.cursor() as cur:
        cur.execute("SELECT id FROM admins WHERE username = %s", (ADMIN_USERNAME,))
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE admins SET password_hash=%s, full_name=%s WHERE username=%s",
                (hashed, ADMIN_FULL_NAME, ADMIN_USERNAME),
            )
            print(f"[OK] Admin '{ADMIN_USERNAME}' password updated.")
        else:
            cur.execute(
                "INSERT INTO admins (username, password_hash, full_name) VALUES (%s, %s, %s)",
                (ADMIN_USERNAME, hashed, ADMIN_FULL_NAME),
            )
            print(f"[OK] Admin '{ADMIN_USERNAME}' created.")
        conn.commit()

    conn.close()
    print(f"[INFO] Login: username='{ADMIN_USERNAME}'  password='{ADMIN_PASSWORD}'")


if __name__ == "__main__":
    main()
