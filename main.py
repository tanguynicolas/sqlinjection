from flask import Flask, request, jsonify
import sqlite3
import threading

app = Flask(__name__)

DATABASE = 'employes.db'
db_lock = threading.Lock()

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT NOT NULL,
            rancon INTEGER,
            is_hacker BOOL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET'])
def index():
    with open('index.html', 'r') as file:
        return file.read()

@app.route('/add_employee', methods=['POST'])
def add_employee():
    nom = request.form['nom']
    prenom = request.form['prenom']
    email = request.form['email']
    rancon = request.form['rancon']

    with db_lock:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employes (nom, prenom, email, rancon, is_hacker) VALUES (?, ?, ?, ?, ?)
        ''', (nom, prenom, email, rancon, False))
        conn.commit()
        conn.close()

    return jsonify(message="Employé ajouté avec succès!")

@app.route('/search_employee', methods=['POST'])
def search_employee():
    search_email = request.form['search_email']
    with db_lock:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM employes WHERE is_hacker = false AND email LIKE "%{search_email}%"')
        employees = cursor.fetchall()
        conn.close()

    employees_list = [{'nom': emp[1], 'prenom': emp[2], 'email': emp[3], 'rancon': emp[4]} for emp in employees]

    return jsonify(employees=employees_list)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
