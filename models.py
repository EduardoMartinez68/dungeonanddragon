import sqlite3
import os

# We connect (if the file does not exist, it is created)
path_db = os.path.join('database', 'db.sqlite3')
conn = sqlite3.connect(path_db)

# To use SQL statements
cursor = conn.cursor()

# Enable support for foreign keys (important for relationships)
cursor.execute("PRAGMA foreign_keys = ON;")

#Create table 'players'
cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    atack Integer NOT NULL,
    speed Integer NOT NULL,
    defense Integer NOT NULL,
    life Integer NOT NULL,
    intelligence Integer NOT NULL,
    charisma Integer NOT NULL,
    history TEXT UNIQUE NOT NULL
);
""")


# save the changes
conn.commit()


print("Tablas creadas con éxito")










# close the connection
conn.close()
