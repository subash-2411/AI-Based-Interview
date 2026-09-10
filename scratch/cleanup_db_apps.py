import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check socialaccount_socialapp rows
    try:
        cursor.execute("SELECT id, provider, name, client_id FROM socialaccount_socialapp WHERE provider='google'")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} Google SocialApp rows in database:")
        for r in rows:
            print(f"  ID: {r[0]}, Provider: {r[1]}, Name: '{r[2]}', Client ID: '{r[3]}'")
            
        if len(rows) > 1:
            # Delete extra rows, keep the first one
            keep_id = rows[0][0]
            cursor.execute("DELETE FROM socialaccount_socialapp_sites WHERE socialapp_id != ?", (keep_id,))
            cursor.execute("DELETE FROM socialaccount_socialapp WHERE id != ?", (keep_id,))
            conn.commit()
            print(f"Successfully cleaned up duplicates! Retained only SocialApp ID {keep_id}.")
        elif len(rows) == 1:
            print("Already only 1 SocialApp in DB. Looks good!")
        else:
            print("No SocialApp records in DB.")
    except sqlite3.OperationalError as e:
        print(f"Table check notice: {e}")
    finally:
        conn.close()
else:
    print("db.sqlite3 not found at", db_path)
