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
CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    temperature INTEGER,
    wind TEXT,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS races (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS spells (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    mana_cost INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location_id INTEGER NOT NULL,
    reward INTEGER DEFAULT 0,
    FOREIGN KEY (location_id) REFERENCES locations(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventories (
    id INTEGER PRIMARY KEY AUTOINCREMENT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS objects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    value INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inventory_id INTEGER NOT NULL,
    object_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (inventory_id) REFERENCES inventories(id),
    FOREIGN KEY (object_id) REFERENCES objects(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS armors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    defense_bonus INTEGER DEFAULT 0,
    weight INTEGER DEFAULT 0,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    attack INTEGER NOT NULL DEFAULT 0,
    speed INTEGER NOT NULL DEFAULT 0,
    defense INTEGER NOT NULL DEFAULT 0,
    life INTEGER NOT NULL DEFAULT 0,
    intelligence INTEGER NOT NULL DEFAULT 0,
    charisma INTEGER NOT NULL DEFAULT 0,
    race_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    armor_id INTEGER,
    inventory_id INTEGER,
    personality_traits TEXT,
    ideals TEXT,
    bonds TEXT,
    flaws TEXT,
    FOREIGN KEY (race_id) REFERENCES races(id),
    FOREIGN KEY (class_id) REFERENCES classes(id),
    FOREIGN KEY (armor_id) REFERENCES armors(id),
    FOREIGN KEY (inventory_id) REFERENCES inventories(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enemies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    life INTEGER NOT NULL DEFAULT 0,
    level INTEGER NOT NULL DEFAULT 1,
    is_boss INTEGER NOT NULL DEFAULT 0, -- 0 = normal, 1 = jefe
    description TEXT,
    weaknesses TEXT, -- Ej: "fire, lightning"
    location_id INTEGER NOT NULL,

    FOREIGN KEY (location_id) REFERENCES locations(id)
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS config (
    id INTEGER PRIMARY KEY CHECK (id = 1), -- Solo debe haber una fila
    max_life INTEGER NOT NULL DEFAULT 100,
    initial_life INTEGER NOT NULL DEFAULT 50,
    max_armor INTEGER NOT NULL DEFAULT 50,
    min_armor INTEGER NOT NULL DEFAULT 0,
    max_mana INTEGER NOT NULL DEFAULT 100,
    initial_mana INTEGER NOT NULL DEFAULT 50,
    mana_gain_small_battle INTEGER NOT NULL DEFAULT 10,
    mana_gain_boss_battle INTEGER NOT NULL DEFAULT 30,
    max_enemies_per_battle INTEGER NOT NULL DEFAULT 5,
    min_enemies_per_battle INTEGER NOT NULL DEFAULT 1
)
""")

# save the changes
conn.commit()


print("Tablas creadas con éxito")










# close the connection
conn.close()
