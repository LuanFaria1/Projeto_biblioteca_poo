import sqlite3
import threading

# Semáforo para controlar o acesso ao banco de dados
db_lock = threading.Lock()

# Função para conectar ao banco de dados SQLite
def conectar_bd():
    conn = sqlite3.connect('biblioteca.db')
    return conn

# Função para criar as tabelas necessárias no banco de dados
def criar_tabelas():
    with db_lock:
        conn = conectar_bd()
        with conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            sobrenome TEXT,
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
                            editora TEXT,
                            ano_publicacao INTEGER,
                            isbn TEXT
                        )''')
            c.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_usuario INTEGER NOT NULL,
                            id_livro INTEGER NOT NULL,
                            data_emprestimo TEXT NOT NULL,
                            data_devolucao TEXT NOT NULL,
                            FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
                            FOREIGN KEY(id_livro) REFERENCES livros(id)
                        )''')
        conn.close()

# Função para consultar um usuário por nome de usuário e senha
def consultar_usuario_por_credenciais(conn, nome_usuario, senha):
    with db_lock:
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome_usuario, senha))
            usuario = c.fetchone()
            return usuario

# Função para consultar um usuário por nome de usuário
def consultar_usuario_por_nome(conn, nome_usuario):
    with db_lock:
        with conn:
            c = conn.cursor()
            c.execute("SELECT * FROM usuarios WHERE nome = ?", (nome_usuario,))
            usuario = c.fetchone()
            return usuario

criar_tabelas()