import sqlite3
import threading

db_lock = threading.Lock()

def conectar_bd():
    conn = sqlite3.connect('biblioteca.db')
    criar_tabelas(conn)
    return conn

def criar_tabelas(conn):
    with conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        endereco TEXT,
                        email TEXT,
                        telefone TEXT,
                        senha TEXT NOT NULL,
                        tipo TEXT NOT NULL
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS livros (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titulo TEXT NOT NULL,
                        autor TEXT NOT NULL,
                        editora TEXT NOT NULL,
                        ano_publicacao INTEGER NOT NULL,
                        isbn TEXT NOT NULL,
                        quantidade INTEGER DEFAULT 1
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_usuario INTEGER,
                        id_livro INTEGER,
                        data_emprestimo TEXT NOT NULL,
                        data_devolucao TEXT,
                        FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
                        FOREIGN KEY (id_livro) REFERENCES livros (id)
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS reservas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_usuario INTEGER,
                        id_livro INTEGER,
                        data_reserva TEXT NOT NULL,
                        FOREIGN KEY (id_usuario) REFERENCES usuarios (id),
                        FOREIGN KEY (id_livro) REFERENCES livros (id)
                    )''')

def consultar_tipo_usuario_por_nome(nome_usuario):
    conn = conectar_bd()
    with db_lock:
        with conn:
            c = conn.cursor()
            c.execute("SELECT tipo FROM usuarios WHERE nome = ?", (nome_usuario,))
            resultado = c.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None

def consultar_usuario_por_credenciais(conn, nome_usuario, senha):
    with db_lock:
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome_usuario, senha))
            return c.fetchone()
