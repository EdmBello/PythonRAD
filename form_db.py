import sqlite3 as sql

# Conectar ao banco de dados
con = sql.connect('form_db.db')
cur = con.cursor()

# Excluir tabelas se existirem
cur.execute('DROP TABLE IF EXISTS usuarios')
cur.execute('DROP TABLE IF EXISTS users')
cur.execute('DROP TABLE IF EXISTS casos')
cur.execute('DROP TABLE IF EXISTS atividades')
cur.execute('DROP TABLE IF EXISTS despesas')
cur.execute('DROP TABLE IF EXISTS avaliacoes')

# Criar a tabela de usuários
cur.execute('''
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
cur.executemany('INSERT INTO usuarios (tplog, username, password) VALUES (?, ?, ?)', usuarios)

# Criar a tabela de users
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME TEXT,
        IDADE TEXT,
        RUA TEXT,
        CIDADE TEXT,
        NUMERO TEXT,
        ESTADO TEXT,
        EMAIL TEXT
    )
''')

# Criar a tabela de casos
cur.execute('''
    CREATE TABLE IF NOT EXISTS casos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CLIENTE_ID INTEGER,
        CLIENTE TEXT,
        TIPO TEXT,
        DATAS TEXT,
        DETALHES TEXT,
        PARTES TEXT,
        FOREIGN KEY(CLIENTE_ID) REFERENCES users(ID)
    )
''')

# Criar a tabela de atividades
cur.execute('''
    CREATE TABLE IF NOT EXISTS atividades (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CLIENTE_ID INTEGER,
        DESCRICAO TEXT,
        DATA TEXT,
        FOREIGN KEY(CLIENTE_ID) REFERENCES users(ID)
    )
''')

# Criar a tabela de despesas
cur.execute('''
    CREATE TABLE IF NOT EXISTS despesas (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CLIENTE_ID INTEGER,
        TIPO TEXT,
        DESCRICAO TEXT,
        VALOR REAL,
        FOREIGN KEY(CLIENTE_ID) REFERENCES users(ID)
    )
''')

# Criar a tabela de avaliacoes
cur.execute('''
    CREATE TABLE IF NOT EXISTS avaliacoes (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        CLIENTE_ID INTEGER,
        DESCRICAO TEXT,
        DATA TEXT,
        STATUS TEXT,
        PASSOS TEXT,
        FOREIGN KEY(CLIENTE_ID) REFERENCES users(ID)
    )
''')

# Salvar (commit) as alterações e fechar a conexão
con.commit()
con.close()
