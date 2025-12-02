import sqlite3

def get_conn():
    return sqlite3.connect("database.db")

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # tabela usuários
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        );
    """)

    # cria usuário admin se não existir
    cur.execute("SELECT * FROM users WHERE email = 'admin@admin.com'")
    if not cur.fetchone():
        cur.execute(
            "INSERT INTO users (nome, email, senha) VALUES (?, ?, ?)",
            ("Administrador", "admin@admin.com", "admin")
        )

    # tabela registros
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data TEXT
        );
    """)

    conn.commit()
    conn.close()
