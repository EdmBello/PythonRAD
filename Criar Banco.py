import sqlite3

# Conectar ao banco de dados SQLite (se não existir, será criado)
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criar a tabela de usuários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tplog TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Inserir alguns dados de exemplo
usuarios = [
    ('Admin', 'admin', 'admin'),
    ('Advogado', 'advogado', 'advogado'),
    ('Cliente', 'cliente', 'cliente')
]

cursor.executemany('INSERT INTO usuarios (tplog, username, password) VALUES (?, ?, ?)', usuarios)

# Commit e fechar a conexão com o banco de dados
conn.commit()
conn.close()
