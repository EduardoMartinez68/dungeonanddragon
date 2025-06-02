# app.py
from flask import Flask, jsonify, render_template
from models  import *
from db_functions import insertar_jugador, insertar_escenario, obtener_jugadores
import os

app = Flask(__name__) #run the app

#-----------------------------------------database-----------------------------------------



#-------------login------------------
@app.route('/')
def home():
    return render_template('login.html')







#-------------cart------------------
@app.route('/cart')
def cart():
    return render_template('cart.html')

#-------------cart------------------
@app.route('/dungeon_master')
def dungeon_master():
    return render_template('dungeon_master.html')

@app.route('/combat')
def combat():
    return render_template('combat.html')


if __name__ == '__main__':
    app.run(debug=True)