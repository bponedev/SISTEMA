import sqlite3
from flask import current_app

# ============================
# Funções auxiliares de banco
# ============================

def get_db():
    conn = sqlite3.connect(current_app.config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn

def execute(sql, params=()):
    db = get_db()
    db.execute(sql, params)
    db.commit()
    db.close()

def query(sql, params=(), one=False):
    db = get_db()
    cur = db.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    db.close()
    return (rows[0] if rows else None) if one else rows

# ============================
# Inicialização do banco
# ============================

def init_db():
    execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        role TEXT DEFAULT 'USER'
    );
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS offices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    );
    """)

    execute("""
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        escritorio TEXT,
        tipo_acao TEXT,
        data_fechamento TEXT,
        pendencias TEXT,
        numero_processo TEXT,
        data_protocolo TEXT,
        observacoes TEXT,
        captador TEXT
    );
    """)

    # Admin automático
    admin = query("SELECT * FROM users WHERE usuario='admin'", one=True)
    if not admin:
        execute("""
        INSERT INTO users (usuario, senha, role)
        VALUES ('admin', '123', 'ADMIN')
        """)
        print(">>> ADMIN criado automaticamente: usuario=admin / senha=123")
