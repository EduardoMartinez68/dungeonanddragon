import sqlite3
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path_db = os.path.join(BASE_DIR, 'db.sqlite3')  # sube un nivel si db está en raíz
print(f"Database path: {path_db}")


def get_all_the_class():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row  # Para obtener los datos como diccionarios
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()

    conn.close()

    return classes

def get_all_the_races():
    conn = sqlite3.connect(path_db)
    conn.row_factory = sqlite3.Row  # Para obtener los datos como diccionarios
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM races")
    races = cursor.fetchall()

    conn.close()

    return races

def create_a_new_class(data):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO classes (
                name, description
            ) VALUES (?, ?)
        """, (
            data['name'],
            data['description']
        ))

        conn.commit()
        return cursor.lastrowid  # Devuelve el ID insertado

    except Exception as e:
        print(f"Error al crear la clase: {e}")
        return None  # Falla

    finally:
        conn.close()

def edit_class(class_id, data):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE classes
            SET name = ?, description = ?
            WHERE id = ?
        """, (
            data['name'],
            data['description'],
            class_id
        ))

        conn.commit()
        return True

    except Exception as e:
        print(f"Error al editar la clase: {e}")
        return False

    finally:
        conn.close()

def delete_class(class_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        conn.commit()
        return True

    except Exception as e:
        print(f"Error al eliminar la clase: {e}")
        return False

    finally:
        conn.close()

def create_a_new_races(data):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO races (
                name, description
            ) VALUES (?, ?)
        """, (
            data['name'],
            data['description']
        ))

        conn.commit()
        return cursor.lastrowid 

    except Exception as e:
        print(f"Error al crear el jugador: {e}")
        return False  # Falla

    finally:
        conn.close()


def edit_race(race_id, data):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            UPDATE races
            SET name = ?, description = ?
            WHERE id = ?
        """, (
            data['name'],
            data['description'],
            race_id
        ))

        conn.commit()
        return True

    except Exception as e:
        print(f"Error al editar la raza: {e}")
        return False

    finally:
        conn.close()

def delete_race(race_id):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM races WHERE id = ?", (race_id,))
        conn.commit()
        return True

    except Exception as e:
        print(f"Error al eliminar la raza: {e}")
        return False

    finally:
        conn.close()
