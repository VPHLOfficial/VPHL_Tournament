import sqlite3

def create_db():
    conn = sqlite3.connect('tournament.db')  # Создание базы данных
    cur = conn.cursor()
    # Создание таблицы teams
    cur.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            conference TEXT,
            points INTEGER,
            goals_for INTEGER,
            goals_against INTEGER
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
