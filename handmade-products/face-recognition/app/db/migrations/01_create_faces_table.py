from dotenv import dotenv_values, load_dotenv
import sqlite3

load_dotenv()
config = dotenv_values(".env")

if "DATABASE_NAME" not in config:
    raise Exception("CONFIG_NOT_FOUND")

con = sqlite3.connect(config["DATABASE_NAME"])
cur = con.cursor()

cur.execute("""
    CREATE TABLE people(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        avatar TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
""")
con.commit()
con.close()
