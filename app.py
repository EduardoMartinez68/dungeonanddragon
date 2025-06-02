# app.py
from flask import Flask, jsonify, render_template
from models  import *
from database.playerdb import *

app = Flask(__name__) #run the app

#-----------------------------------------database-----------------------------------------



#-------------login------------------
@app.route('/')
def home():
    return render_template('login.html')







#-------------cart------------------
@app.route('/selectCard')
def selectCard():
    return render_template('selectCard.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

#-------------cart------------------
@app.route('/dungeon_master')
def dungeon_master():
    players=get_all_the_players()
    return render_template('dungeon_master.html',players=players)

@app.route('/combat')
def combat():
    return render_template('combat.html')


if __name__ == '__main__':
    app.run(debug=True)