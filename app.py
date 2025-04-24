from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Это нужно для работы с сессиями

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('tournament.db')
    conn.row_factory = sqlite3.Row  # Чтобы можно было обращаться к строкам как к словарям
    return conn

@app.route('/')
def standings():
    conn = get_db_connection()
    teams = conn.execute('SELECT * FROM teams').fetchall()
    conn.close()

    return render_template('standings.html', teams=teams, length=len(teams))

# Добавление результатов матча
@app.route('/add', methods=['GET', 'POST'])
def add_match():
    if 'logged_in' not in session:  # Проверка, если админ не залогинен
        return redirect(url_for('login'))

    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        score1 = int(request.form['score1'])
        score2 = int(request.form['score2'])

        conn = get_db_connection()
        try:
            # Вставка результата матча в таблицу матчей
            conn.execute('''INSERT INTO matches (team1, team2, score1, score2) VALUES (?, ?, ?, ?)''',
                         (team1, team2, score1, score2))

            # Обновление статистики команд
            conn.execute('UPDATE teams SET games = games + 1 WHERE name = ?', (team1,))
            conn.execute('UPDATE teams SET games = games + 1 WHERE name = ?', (team2,))

            if score1 > score2:  # Победа команды 1
                conn.execute('UPDATE teams SET wins = wins + 1, points = points + 2 WHERE name = ?', (team1,))
                conn.execute('UPDATE teams SET losses = losses + 1 WHERE name = ?', (team2,))
            elif score2 > score1:  # Победа команды 2
                conn.execute('UPDATE teams SET wins = wins + 1, points = points + 2 WHERE name = ?', (team2,))
                conn.execute('UPDATE teams SET losses = losses + 1 WHERE name = ?', (team1,))
            else:  # Ничья
                conn.execute('UPDATE teams SET overtime_wins = overtime_wins + 1, points = points + 1 WHERE name = ?', (team1,))
                conn.execute('UPDATE teams SET overtime_losses = overtime_losses + 1 WHERE name = ?', (team2,))

            # Обновляем голы забитые и пропущенные
            conn.execute('UPDATE teams SET goals_for = goals_for + ?, goals_against = goals_against + ? WHERE name = ?',
                         (score1, score2, team1))
            conn.execute('UPDATE teams SET goals_for = goals_for + ?, goals_against = goals_against + ? WHERE name = ?',
                         (score2, score1, team2))

            conn.commit()

            # Пересортировать команды по очкам и разнице голов
            teams = conn.execute('SELECT * FROM teams').fetchall()

            # Обновляем ранг команд
            for idx, team in enumerate(teams):
                conn.execute('UPDATE teams SET rank = ? WHERE id = ?', (idx + 1, team['id']))

            conn.commit()
        except Exception as e:
            print(f"Ошибка при добавлении матча: {e}")
            conn.rollback()
        finally:
            conn.close()

        return redirect('/')  # После добавления матча перенаправляем обратно на турнирную таблицу
    return render_template('add_match.html')

# Статистика
@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

# Рекорды
@app.route('/records')
def records():
    return render_template('records.html')

# Страница логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Здесь можно заменить на настоящий механизм аутентификации
        if username == 'admin' and password == 'password':  # Пример простого логина
            session['logged_in'] = True
            return redirect('/')

        else:
            return 'Неверный логин или пароль', 401

    return render_template('login.html')

# Логика выхода из системы
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)

