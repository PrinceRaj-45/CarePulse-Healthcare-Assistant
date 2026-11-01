"""
Utility script to quickly inspect the SQLite database from the terminal.
Run: python view_db.py
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "carepulse.db")

def view_database():
    if not os.path.exists(DB_PATH):
        print(f"Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get list of user tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row["name"] for row in cursor.fetchall()]

    print("=" * 65)
    print(f"CarePulse Database Inspector: {os.path.basename(DB_PATH)}")
    print(f"Tables Found: {', '.join(tables)}")
    print("=" * 65)

    for table in tables:
        print(f"\n[TABLE: {table.upper()}]")
        print("-" * 65)
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        if not rows:
            print("  (Table is currently empty)")
            continue

        columns = rows[0].keys()
        print("  Columns: " + " | ".join(columns))
        print("  " + "-" * 60)
        
        for idx, row in enumerate(rows, 1):
            row_vals = [str(row[col]) if row[col] is not None else "NULL" for col in columns]
            print(f"  {idx}. " + " | ".join(row_vals))

    conn.close()
    print("\n" + "=" * 65)

if __name__ == "__main__":
    view_database()
