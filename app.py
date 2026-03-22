from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            servers INTEGER,
            storage INTEGER,
            maintenance INTEGER,
            on_prem INTEGER,
            cloud INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    servers = int(request.form['servers'])
    storage = int(request.form['storage'])
    maintenance = int(request.form['maintenance'])

    on_prem_cost = (servers * 5000) + (storage * 10) + maintenance
    cloud_cost = (servers * 3000) + (storage * 8)

    if cloud_cost < on_prem_cost:
        suggestion = "Cloud migration is cost-effective."
    else:
        suggestion = "On-premise system may be better for now."

    # Save to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (servers, storage, maintenance, on_prem, cloud)
        VALUES (?, ?, ?, ?, ?)
    ''', (servers, storage, maintenance, on_prem_cost, cloud_cost))
    conn.commit()
    conn.close()

    return render_template('result.html',
                           on_prem=on_prem_cost,
                           cloud=cloud_cost,
                           suggestion=suggestion)

if __name__ == '__main__':
    app.run(debug=True)