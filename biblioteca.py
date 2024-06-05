from banco_de_dados import conectar_bd, db_lock, consultar_tipo_usuario_por_nome
from datetime import datetime

# Classe Usuario
class Usuario:
    def __init__(self, nome_usuario, senha, endereco="", email="", telefone="", tipo="comum"):
        self.__nome_usuario = nome_usuario
        self.__senha = senha
        self.__endereco = endereco
        self.__email = email
        self.__telefone = telefone
        self.__tipo = tipo

    @property
    def nome_usuario(self):
        return self.__nome_usuario

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    @property
    def endereco(self):
        return self.__endereco
    
    @endereco.setter
    def endereco(self, endereco):
        self.__endereco = endereco

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def telefone(self):
        return self.__telefone
    
    @telefone.setter
    def telefone(self, telefone):
        self.__telefone = telefone

    @property
    def tipo(self):
        return self.__tipo

    def inserir_usuario_bd(self, conn):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("INSERT INTO usuarios (nome, endereco, email, telefone, senha, tipo) VALUES (?, ?, ?, ?, ?, ?)", 
                          (self.__nome_usuario, self.__endereco, self.__email, self.__telefone, self.__senha, self.__tipo))

    def __str__(self):
        return self.__nome_usuario

# Classe Administrador
class Administrador(Usuario):
    def __init__(self, nome_usuario, senha):
        super().__init__(nome_usuario, senha, tipo="administrador")

# Classe Livro
class Livro:
    def __init__(self, titulo, autor, editora, ano, isbn):
        self.__titulo = titulo
        self.__autor = autor
        self.__editora = editora
        self.__ano = ano
        self.__isbn = isbn

    @property
    def titulo(self):
        return self.__titulo

    @property
    def autor(self):
        return self.__autor

    @property
    def editora(self):
        return self.__editora

    @property
    def ano(self):
        return self.__ano

    @property
    def isbn(self):
        return self.__isbn

    def inserir_livro_bd(self, conn):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn) VALUES (?, ?, ?, ?, ?)", 
                          (self.__titulo, self.__autor, self.__editora, self.__ano, self.__isbn))

# Classe LivroFisico
class LivroFisico(Livro):
    def __init__(self, titulo, autor, editora, ano, isbn, quantidade):
        super().__init__(titulo, autor, editora, ano, isbn)
        self.__quantidade = quantidade

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, nova_quantidade):
        self.__quantidade = nova_quantidade

    def emprestar(self):
        if self.__quantidade > 0:
            self.__quantidade -= 1
            return True
        else:
            return False

    def devolver(self):
        self.__quantidade += 1

# Classe Emprestimo
class Emprestimo:
    def __init__(self, id_usuario, id_livro, data_emprestimo=None, data_devolucao=None):
        self.__id_usuario = id_usuario
        self.__id_livro = id_livro
        self.__data_emprestimo = data_emprestimo or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__data_devolucao = data_devolucao

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def id_livro(self):
        return self.__id_livro

    @property
    def data_emprestimo(self):
        return self.__data_emprestimo

    @property
    def data_devolucao(self):
        return self.__data_devolucao

    def realizar_emprestimo_bd(self, conn):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)", 
                          (self.__id_usuario, self.__id_livro, self.__data_emprestimo, self.__data_devolucao))

    def atualizar_data_devolucao_bd(self, conn, nova_data_devolucao):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id_usuario = ? AND id_livro = ?", 
                          (nova_data_devolucao, self.__id_usuario, self.__id_livro))

# Classe Biblioteca, que gerencia as operações da biblioteca
class Biblioteca:
    def __init__(self):
        self.__conn = conectar_bd()  # Conecta ao banco de dados ao inicializar a classe

    def inserir_livro(self, titulo, autor, editora, ano_publicacao, isbn):
        livro = Livro(titulo, autor, editora, ano_publicacao, isbn)
        livro.inserir_livro_bd(self.__conn)
        print("Livro inserido com sucesso!")

    def inserir_usuario(self, nome, endereco, email, telefone, senha, tipo):
        usuario = Usuario(nome, senha, endereco, email, telefone, tipo)
        usuario.inserir_usuario_bd(self.__conn)
        print("Usuário inserido com sucesso!")

    def exibir_usuarios(self):
        usuarios = self.consultar_usuarios_bd()
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Endereço: {usuario[2]}, Email: {usuario[3]}, Telefone: {usuario[4]}, Tipo: {usuario[5]}")

    def realizar_emprestimo(self, id_usuario, id_livro):
        emprestimo = Emprestimo(id_usuario, id_livro)
        emprestimo.realizar_emprestimo_bd(self.__conn)
        print("Empréstimo realizado com sucesso!")

    def devolver_livro(self, id_usuario, id_livro):
        emprestimo = Emprestimo(id_usuario, id_livro)
        emprestimo.atualizar_data_devolucao_bd(self.__conn, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("Livro devolvido com sucesso!")

    def exibir_livros_emprestados(self):
        livros_emprestados = self.consultar_livros_emprestados_bd()
        for livro in livros_emprestados:
            print(f"ID Empréstimo: {livro[0]}, Título: {livro[1]}, Nome do usuário: {livro[2]}, Data de Empréstimo: {livro[3]}, Data de Devolução: {livro[4]}")

    def exibir_todos_os_livros(self):
        livros = self.consultar_livros_bd()
        for livro in livros:
            print(f"Título: {livro[1]}, Autor: {livro[2]}, Editora: {livro[3]}, Ano: {livro[4]}, ISBN: {livro[5]}")

    def consultar_usuarios_bd(self):
        with db_lock:
            with self.__conn:
                c = self.__conn.cursor()
                c.execute("SELECT * FROM usuarios")
                usuarios = c.fetchall()
                return usuarios

    def consultar_livros_emprestados_bd(self):
        with db_lock:
            with self.__conn:
                c = self.__conn.cursor()
                c.execute('''SELECT emprestimos.id, livros.titulo, usuarios.nome, emprestimos.data_emprestimo, emprestimos.data_devolucao 
                           FROM livros 
                           INNER JOIN emprestimos ON livros.id = emprestimos.id_livro 
                           INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario 
                            ''')
                livros_emprestados = c.fetchall()
                return livros_emprestados

    def consultar_livros_bd(self):
        with db_lock:
            with self.__conn:
                c = self.__conn.cursor()
                c.execute("SELECT * FROM livros")
                livros = c.fetchall()
                return livros

    def consultar_usuario_por_id(self, id_usuario):
        with db_lock:
            with self.__conn:
                c = self.__conn.cursor()
                c.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
                usuario = c.fetchone()
                return usuario

    def consultar_livro_por_id(self, id_livro):
        with db_lock:
            with self.__conn:
                c = self.__conn.cursor()
                c.execute("SELECT * FROM livros WHERE id = ?", (id_livro,))
                livro = c.fetchone()
                return livro

    def consultar_emprestimo_por_id(self, id_emprestimo):
        with db_lock:
            with self.__conn:
                c = self.__conn.cursor()
                c.execute("SELECT * FROM emprestimos WHERE id = ?", (id_emprestimo,))
                emprestimo = c.fetchone()
                return emprestimo

