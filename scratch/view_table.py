import sqlite3
import os
import sys

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"Database file not found at: {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

if len(sys.argv) < 2:
    print("Usage: python scratch/view_table.py <table_name> [limit]")
    print("\nAvailable tables:")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    for (t,) in tables:
        if not t.startswith('sqlite_'):
            print(f"  - {t}")
    conn.close()
    exit(0)

table_name = sys.argv[1]
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
if not cursor.fetchone():
    print(f"Table '{table_name}' does not exist.")
    conn.close()
    exit(1)

# Get column names
cursor.execute(f"PRAGMA table_info(\"{table_name}\");")
columns = cursor.fetchall()
col_names = [col[1] for col in columns]

print(f"\nSchema for Table: {table_name}")
print("=" * 60)
for col in columns:
    # col: (cid, name, type, notnull, dflt_value, pk)
    pk_str = " (PRIMARY KEY)" if col[5] else ""
    print(f"  {col[1]} ({col[2]}){' NOT NULL' if col[3] else ''}{pk_str}")
print("=" * 60)

# Fetch rows
cursor.execute(f"SELECT * FROM \"{table_name}\" LIMIT ?;", (limit,))
rows = cursor.fetchall()

print(f"\nShowing top {len(rows)} rows:")
print("-" * 60)
if not rows:
    print("No records found in this table.")
else:
    for idx, row in enumerate(rows, 1):
        print(f"Record #{idx}:")
        for col_name, val in zip(col_names, row):
            print(f"  {col_name}: {val}")
        print("-" * 40)

conn.close()
