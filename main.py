from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
DB_NAME= 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

#criar a página de registro no site 
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    senha = data.get('senha')

    if not username or not senha:
        return jsonify({'error': 'Insira nome de usuário e senha'})
#se não digitarem nada aparecera erro de não completo

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = generate_password_hash(senha) 
        cursor.execute("INSERT INTO users (username, senha) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registrado com sucesso'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuário já existe'})

@app.route ('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    senha = data.get('senha')

    if not username or not senha: 
        return jsonify({'error': 'Insira nome de usuário e senha'})
#se não escrever nada pedir para escrever
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['senha'], senha):
        return jsonify({'message': 'Login foi um sucesso'}), 
    else:
        return jsonify({'error': 'Usuário ou senha errado'}), 

if __name__ == '__main__':
    app.run(debug=True)