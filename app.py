# app.py
from flask import Flask, jsonify, render_template, request
from models  import *
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

@app.route('/cart')
def cart():
    return render_template('cart.html')



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


if __name__ == '__main__':
    app.run(debug=True)