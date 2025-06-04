# app.py
from flask import Flask, jsonify, render_template, request
from models  import *

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
from database.spacesAndClass import *
@app.route('/dungeon_master')
def dungeon_master():
    players=get_all_the_players()
    classes=get_all_the_class()
    races=get_all_the_races()
    return render_template('dungeon_master.html',players=players,classes=classes,races=races)


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




@app.route('/combat')
def combat():
    return render_template('combat.html')


if __name__ == '__main__':
    app.run(debug=True)