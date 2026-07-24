import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')

if not os.path.exists(db_path):
    print(f"Database file not found at: {db_path}")
    exit(1)

print(f"Connecting to database: {db_path}\n")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print(f"{'Table Name':<45} | {'Row Count':<10}")
print("-" * 60)

for (table_name,) in tables:
    if table_name.startswith('sqlite_'):
        continue
    try:
        cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\";")
        count = cursor.fetchone()[0]
        print(f"{table_name:<45} | {count:<10}")
    except Exception as e:
        print(f"{table_name:<45} | Error: {e}")

conn.close()
