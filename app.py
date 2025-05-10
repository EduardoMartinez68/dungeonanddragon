# app.py
from flask import Flask, jsonify, render_template
from db import get_connection

app = Flask(__name__)

#-------------login------------------
@app.route('/')
def home():
    return render_template('index.html')








#-------------cart------------------
@app.route('/cart')
def cart():
    return render_template('cart.html')









@app.route('/usuarios')
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM usuarios")  # Suponiendo una tabla `usuarios`
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    usuarios = [{'id': row[0], 'nombre': row[1]} for row in rows]
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(debug=True)