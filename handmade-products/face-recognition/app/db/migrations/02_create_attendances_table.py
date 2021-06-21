from dotenv import dotenv_values, load_dotenv
import sqlite3

load_dotenv()
config = dotenv_values(".env")

if "DATABASE_PATH" not in config:
    raise Exception("CONFIG_NOT_FOUND")

con = sqlite3.connect(config["DATABASE_PATH"])
cur = con.cursor()

cur.execute("""
    CREATE TABLE attendances(
        id INTEGER PRIMARY KEY,
        person_id INTEGER NOT NULL,
        avatar TEXT NOT NULL,
        confidence INTEGER NOT NULL,
        attended_at TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(person_id) REFERENCES people(id)
    )
""")
con.commit()
con.close()
