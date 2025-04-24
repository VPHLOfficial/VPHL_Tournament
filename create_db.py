import sqlite3

conn = sqlite3.connect('tournament.db')  # Путь к вашей базе данных
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    points INTEGER DEFAULT 0,
    goals_for INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    games INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    overtime_wins INTEGER DEFAULT 0,
    overtime_losses INTEGER DEFAULT 0,
    rank INTEGER DEFAULT 0
)''')

conn.commit()
conn.close()
