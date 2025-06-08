# app.py
from flask import Flask, jsonify, render_template, request, redirect
from models  import *
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__) #run the app

#-----------------------------------------database-----------------------------------------



#-------------login------------------
@app.route('/')
def home():
    return render_template('login.html')







#-------------cart------------------
from database.playerdb import *
@app.route('/selectCard')
def selectCard():
    return render_template('selectCard.html')

@app.route('/cart/<int:player_id>')
def cart(player_id):
    player=get_data_of_the_player(player_id)
    return render_template('cart.html',player=player)

@app.route('/choose-hero', methods=['GET'])
def choose_hero():
    player_id = request.args.get('player_id')
    
    if not player_id:
        return "Por favor, ingresa el número del jugador", 400

    try:
        player_id = int(player_id)
    except ValueError:
        return "El ID del jugador no es válido", 400

    player = get_data_of_the_player_for_the_card(player_id)
    
    if not player:
        return "Jugador no encontrado", 404

    return render_template('cart.html',player=player)


def get_data_of_the_player_for_the_card(player_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.*,
            r.name AS race,
            c.name AS class
        FROM players p
        JOIN races r ON p.race_id = r.id
        JOIN classes c ON p.class_id = c.id
        WHERE p.id = ?
    """, (player_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return {
            "id": player_id,
            "name": "Desconocido",
            "life": 0,
            "defense": 0,
            "race": "Desconocida",
            "class": "Desconocida"
        }

    columns = [column[0] for column in cursor.description]
    player = dict(zip(columns, row))
    return player


#-------------form------------------
def mission_get_all():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Para obtener los datos como diccionarios
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM missions")
    rows = cursor.fetchall()

    conn.close()
    missions = [dict(row) for row in rows]
    return missions

from database.spacesAndClass import *
@app.route('/dungeon_master')
def dungeon_master():
    players=get_all_the_players()
    classes=get_all_the_class()
    races=get_all_the_races()
    missions=mission_get_all()
    return render_template('dungeon_master.html',players=players,classes=classes,races=races,missions=missions)

#------------------------------create player
@app.route('/create-player', methods=['GET', 'POST'])
def create_player():
    if request.method == 'POST':
        data = request.form

        name = data.get('name')
        attack = int(data.get('attack', 0))
        speed = int(data.get('speed', 0))
        defense = int(data.get('defense', 0))
        life = int(data.get('life', 0))
        intelligence = int(data.get('intelligence', 0))
        charisma = int(data.get('charisma', 0))
        race_id = int(data.get('race_id'))
        class_id = int(data.get('class_id'))
        armor_id = data.get('armor_id')
        personality_traits = data.get('personality_traits')
        ideals = data.get('ideals')
        bonds = data.get('bonds')
        flaws = data.get('flaws')
        armor = int(request.form['armor'])
        mana = int(request.form['mana'])
        # Convert armor_id to int or None
        armor_id = int(armor_id) if armor_id else None

        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Crear el inventario vacío
        cursor.execute("INSERT INTO inventories DEFAULT VALUES")
        inventory_id = cursor.lastrowid  # Obtiene el ID del inventario recién creado

        # 2. Insertar al jugador con el ID del inventario creado
        cursor.execute("""
            INSERT INTO players 
            (name, attack, speed, defense, life, intelligence, charisma, race_id, class_id, armor_id, inventory_id, personality_traits, ideals, bonds, flaws, armor, mana)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
        """, (name, attack, speed, defense, life, intelligence, charisma, race_id, class_id, armor_id, inventory_id, personality_traits, ideals, bonds, flaws,armor,mana))

        conn.commit()
        conn.close()

        return redirect('/dungeon_master')

    # Si es GET, mostrar el formulario:
    classes = get_all_the_class()
    races = get_all_the_races()
    return render_template('create_player.html', classes=classes, races=races)

@app.route('/edit-player/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.form

        name = data.get('name')
        attack = int(data.get('attack', 0))
        speed = int(data.get('speed', 0))
        defense = int(data.get('defense', 0))
        life = int(data.get('life', 0))
        intelligence = int(data.get('intelligence', 0))
        charisma = int(data.get('charisma', 0))
        race_id = int(data.get('race_id'))
        class_id = int(data.get('class_id'))
        armor_id = data.get('armor_id')
        armor_id = int(armor_id) if armor_id else None
        armor = int(data.get('armor', 0))
        mana = int(data.get('mana', 0))
        personality_traits = data.get('personality_traits')
        ideals = data.get('ideals')
        bonds = data.get('bonds')
        flaws = data.get('flaws')

        cursor.execute("""
            UPDATE players
            SET name=?, attack=?, speed=?, defense=?, life=?, intelligence=?, charisma=?,
                race_id=?, class_id=?, armor_id=?, armor=?, mana=?,
                personality_traits=?, ideals=?, bonds=?, flaws=?
            WHERE id=?
        """, (name, attack, speed, defense, life, intelligence, charisma,
              race_id, class_id, armor_id, armor, mana,
              personality_traits, ideals, bonds, flaws, player_id))

        conn.commit()
        conn.close()

        return redirect('/dungeon_master')

    player = get_data_of_the_player(player_id)
    races = get_all_the_races()
    classes = get_all_the_class()
    return render_template("edit_player.html", player=player, races=races, classes=classes)


def get_data_of_the_player(player_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Si es GET, mostrar el formulario con datos actuales
    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    row = cursor.fetchone()
    player = dict(zip([column[0] for column in cursor.description], row))

    conn.close()
    return player
#------------------------------class and especie
@app.route('/create-class', methods=['POST'])
def create_class_route():
    data = request.json
    new_id = create_a_new_class(data)

    if new_id:  # Si se insertó correctamente y tiene un ID
        return jsonify({"success": True, "id": new_id})
    else:
        return jsonify({"success": False, "error": "No se pudo crear la clase"}), 500

@app.route('/delete-class/<int:id>', methods=['DELETE'])
def delete_class_route(id):
    success = delete_class(id)
    return jsonify({'success': success})

@app.route('/edit-class/<int:id>', methods=['POST'])
def edit_class_route(id):
    data = request.json
    success = edit_class(id, data)
    return jsonify({'success': success})


@app.route('/create-races', methods=['POST'])
def create_races_route():
    data = request.json
    new_id = create_a_new_races(data)

    if new_id:  # Si se insertó correctamente y tiene un ID
        return jsonify({"success": True, "id": new_id})
    else:
        return jsonify({"success": False, "error": "No se pudo crear la clase"}), 500

@app.route('/delete-races/<int:id>', methods=['DELETE'])
def delete_races_route(id):
    success = delete_race(id)
    return jsonify({'success': success})

@app.route('/edit-races/<int:id>', methods=['POST'])
def edit_races_route(id):
    data = request.json
    success = edit_race(id, data)
    return jsonify({'success': success})


#----------------------------------------------mission
def get_db_connection():
    path_db = os.path.join(BASE_DIR, 'db.sqlite3') 
    conn = sqlite3.connect(path_db)
    #conn.row_factory = sqlite3.Row
    return conn

@app.route('/create-mission', methods=['POST'])
def create_mission():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO missions (name, location_id, reward)
        VALUES (?, ?, ?)
    """, (data['name'], data['location_id'], data['reward']))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({"success": True, "id": new_id})

@app.route('/update-mission/<int:mission_id>', methods=['PUT'])
def mission_update(mission_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE missions SET name = ?, location_id = ?, reward = ?
        WHERE id = ?
    """, (data['name'], data['location_id'], data['reward'], mission_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/delete-mission/<int:mission_id>', methods=['DELETE'])
def mission_delete(mission_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE id = ?", (mission_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})



@app.route('/combat')
def combat():
    return render_template('combat.html')

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No se conecta realmente, solo fuerza a sacar la IP local
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except:
        return '127.0.0.1'
    finally:
        s.close()




if __name__ == '__main__':
    ip = get_local_ip()
    print(f"Servidor disponible en: http://{ip}:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

