from banco_de_dados import conectar_bd, db_lock

# Classe Usuario
class Usuario:
    def _init_(self, nome_usuario, senha, endereco="", email="", telefone="", tipo="comum"):
        self.nome_usuario = nome_usuario
        self.__senha = senha
        self.endereco = endereco
        self.email = email
        self.telefone = telefone
        self.tipo = tipo

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    def inserir_usuario_bd(self, conn):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("INSERT INTO usuarios (nome, sobrenome, endereco, email, telefone, senha, tipo) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                          (self.nome_usuario, '', self.endereco, self.email, self.telefone, self.__senha, self.tipo))

    def _str_(self):
        return self.nome_usuario

# Classe Administrador
class Administrador(Usuario):
    def _init_(self, nome_usuario, senha):
        super()._init_(nome_usuario, senha, tipo="administrador")

# Classe Livro
class Livro:
    def _init_(self, titulo, autor, editora, ano, isbn):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano = ano
        self.isbn = isbn

    def inserir_livro_bd(self, conn):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn) VALUES (?, ?, ?, ?, ?)", 
                          (self.titulo, self.autor, self.editora, self.ano, self.isbn))

# Classe Emprestimo
class Emprestimo:
    def _init_(self, id_usuario, id_livro, data_emprestimo, data_devolucao):
        self.id_usuario = id_usuario
        self.id_livro = id_livro
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao

    def realizar_emprestimo_bd(self, conn):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_devolucao) VALUES (?, ?, ?, ?)", 
                          (self.id_usuario, self.id_livro, self.data_emprestimo, self.data_devolucao))

    def atualizar_data_devolucao_bd(self, conn, nova_data_devolucao):
        with db_lock:
            with conn:
                c = conn.cursor()
                c.execute("UPDATE emprestimos SET data_devolucao = ? WHERE id = ?", 
                          (nova_data_devolucao, self.id_usuario))

# Classe Biblioteca, que gerencia as operações da biblioteca
class Biblioteca:
    def _init_(self):
        self.conn = conectar_bd()  # Conecta ao banco de dados ao inicializar a classe

    def inserir_livro(self, titulo, autor, editora, ano_publicacao, isbn):
        livro = Livro(titulo, autor, editora, ano_publicacao, isbn)
        livro.inserir_livro_bd(self.conn)
        print("Livro inserido com sucesso!")

    def inserir_usuario(self, nome, sobrenome, endereco, email, telefone, senha, tipo):
        usuario = Usuario(nome, senha, endereco, email, telefone, tipo)
        usuario.inserir_usuario_bd(self.conn)
        print("Usuário inserido com sucesso!")

    def exibir_usuarios(self):
        usuarios = self.consultar_usuarios_bd()
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]} {usuario[2]}, Endereço: {usuario[3]}, Email: {usuario[4]}, Telefone: {usuario[5]}")

    def realizar_emprestimo(self, id_usuario, id_livro, data_emprestimo, data_devolucao):
        emprestimo = Emprestimo(id_usuario, id_livro, data_emprestimo, data_devolucao)
        emprestimo.realizar_emprestimo_bd(self.conn)
        print("Empréstimo realizado com sucesso!")

    def atualizar_data_devolucao(self, id_emprestimo, data_devolucao):
        emprestimo = Emprestimo(id_emprestimo, None, None, data_devolucao)  # id_usuario e id_livro não são necessários para a atualização
        emprestimo.atualizar_data_devolucao_bd(self.conn, data_devolucao)
        print("Data de devolução atualizada com sucesso!")

    def exibir_livros_emprestados(self):
        livros_emprestados = self.consultar_livros_emprestados_bd()
        for livro in livros_emprestados:
            print(f"ID Empréstimo: {livro[0]}, Título: {livro[1]}, Nome do usuário: {livro[2]} {livro[3]}, Data de Empréstimo: {livro[4]}, Data de Devolução: {livro[5]}")

    def exibir_todos_os_livros(self):
        livros = self.consultar_livros_bd()
        for livro in livros:
            print(f"Título: {livro[1]}, Autor: {livro[2]}, Editora: {livro[3]}, Ano: {livro[4]}, ISBN: {livro[5]}")

    def consultar_usuarios_bd(self):
        with db_lock:
            with self.conn:
                c = self.conn.cursor()
                c.execute("SELECT * FROM usuarios")
                usuarios = c.fetchall()
                return usuarios

    def consultar_livros_emprestados_bd(self):
        with db_lock:
            with self.conn:
                c = self.conn.cursor()
                c.execute('''SELECT emprestimos.id, livros.titulo, usuarios.nome, usuarios.sobrenome, emprestimos.data_emprestimo, emprestimos.data_devolucao 
                           FROM livros 
                           INNER JOIN emprestimos ON livros.id = emprestimos.id_livro 
                           INNER JOIN usuarios ON usuarios.id = emprestimos.id_usuario 
                            ''')
                livros_emprestados = c.fetchall()
                return livros_emprestados

    def consultar_livros_bd(self):
        with db_lock:
            with self.conn:
                c = self.conn.cursor()
                c.execute("SELECT * FROM livros")
                livros = c.fetchall()
                return livros