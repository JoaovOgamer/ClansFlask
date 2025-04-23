import sqlite3

#conecta na database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

#cria uma tabela de user
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, senha TEXT NOT NULL)''')
conn.commit()
conn.close()
print("Database iniciou")