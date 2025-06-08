import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_db = os.path.join(BASE_DIR, 'db.sqlite3')  # sube un nivel si db está en raíz
print(f"Database path: {path_db}")


def get_all_the_players():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row  # Para obtener los datos como diccionarios
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()

    conn.close()

    return players

def create_a_new_player(data):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO players (
                name, attack, speed, defense, life,
                intelligence, charisma, race_id, class_id,
                armor_id, inventory_id, personality_traits, ideals, bonds, flaws
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['name'],
            data['attack'],
            data['speed'],
            data['defense'],
            data['life'],
            data['intelligence'],
            data['charisma'],
            data['race_id'],
            data['class_id'],
            data.get('armor_id'),        # Puede ser NULL
            data.get('inventory_id'),    # Puede ser NULL
            data.get('personality_traits', ''),
            data.get('ideals', ''),
            data.get('bonds', ''),
            data.get('flaws', '')
        ))

        conn.commit()
        return True  # Éxito

    except Exception as e:
        print(f"Error al crear el jugador: {e}")
        return False  # Falla

    finally:
        conn.close()