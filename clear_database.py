import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()
cur.execute('PRAGMA foreign_keys = OFF;')
cur.execute('DELETE FROM jogador_time;')
cur.execute('DELETE FROM jogadores;')
cur.execute('DELETE FROM partidas;')
cur.execute('DELETE FROM usuarios;')
try:
    cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('jogador_time','jogadores','partidas','usuarios');")
except sqlite3.OperationalError:
    pass
conn.commit()
cur.execute('VACUUM;')
conn.close()
print('database cleared and autoincrement reset')
