from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('tournament.db')
    conn.row_factory = sqlite3.Row  # Чтобы можно было обращаться к строкам как к словарям
    return conn

@app.route('/')
def standings():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM teams ORDER BY points DESC, goals_for - goals_against DESC').fetchall()
    conn.close()
    return render_template('standings.html', teams=teams)

@app.route('/add', methods=['POST'])
def add_match():
    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        score1 = request.form['score1']
        score2 = request.form['score2']

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO teams (name, conference, points, goals_for, goals_against)
            VALUES (?, ?, ?, ?, ?)''', (team1, 'West', 0, score1, score2))
        conn.commit()
        conn.close()
        return redirect('/')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/records')
def records():
    return render_template('records.html')

if __name__ == '__main__':
    app.run(debug=True)