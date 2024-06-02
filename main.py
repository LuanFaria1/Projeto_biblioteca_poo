from view import exibir_menu
from biblioteca import Biblioteca, Usuario, Administrador
from banco_de_dados import conectar_bd, consultar_usuario_por_credenciais, consultar_usuario_por_nome

def fazer_login(conn):
    nome_usuario = input("Nome de usuário: ").strip()
    senha = input("Senha: ").strip()
    
    usuario = consultar_usuario_por_credenciais(conn, nome_usuario, senha)
    if usuario:
        if usuario[6] == "administrador":
            print("Login de administrador bem-sucedido!")
        else:
            print("Login bem-sucedido!")
        return usuario
    else:
        print("Nome de usuário ou senha incorretos. Tente novamente.")
        return None

def cadastrar_usuario(conn):
    nome = input("Nome: ").strip()
    sobrenome = input("Sobrenome: ").strip()
    endereco = input("Endereço: ").strip()
    email = input("Email: ").strip()
    telefone = input("Telefone: ").strip()
    senha = input("Senha: ").strip()
    usuario = Usuario(nome, senha, endereco, email, telefone, "comum")
    usuario.inserir_usuario_bd(conn)
    print("Usuário cadastrado com sucesso!")

def main():
    # Conectar-se ao banco de dados
    conn = conectar_bd()
    if conn is None:
        # Se não conseguir conectar, encerre o programa
        print("Erro ao conectar ao banco de dados.")
        return

    # Inicializa o sistema de biblioteca
    sistema_biblioteca = Biblioteca()

    while True:
        print("Digite 1 caso você for um usuário administrador")
        print("Digite 2 caso seja um usuário comum")
        opcao_tipo_usuario = input("Digite a opção desejada: ").strip()

        if opcao_tipo_usuario == "1":
            usuario_logado = fazer_login(conn)
            if usuario_logado and usuario_logado[6] == "administrador":
                break
            else:
                print("Somente administradores podem acessar esta opção.")
                continue

        elif opcao_tipo_usuario == "2":
            possui_cadastro = input("Você possui cadastro? (s/n): ").strip().lower()
            if possui_cadastro == "s":
                usuario_logado = fazer_login(conn)
                if usuario_logado:
                    break
                else:
                    continue
            elif possui_cadastro == "n":
                cadastrar_usuario(conn)
                continue
            else:
                print("Opção inválida. Por favor, selecione uma opção válida.")
                continue

        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")
            continue

    while True:
        print("Bem Vindo ao Menu Principal")

        # Exibe o menu e captura a opção escolhida pelo usuário
        opcao = exibir_menu(usuario_logado).strip()  # Corrige a captura da opção do menu removendo espaços em branco

        if opcao == "1":
            # Chama o método específico para inserir um livro
            titulo = input("Título do Livro: ").strip()
            autor = input("Autor do Livro: ").strip()
            editora = input("Editora do Livro: ").strip()
            ano_publicacao = int(input("Ano de Publicação: ").strip())
            isbn = input("ISBN do Livro: ").strip()
            sistema_biblioteca.inserir_livro(titulo, autor, editora, ano_publicacao, isbn)
        
        elif opcao == "2":
            # Chama o método específico para inserir um usuário
            nome = input("Nome: ").strip()
            sobrenome = input("Sobrenome: ").strip()
            endereco = input("Endereço: ").strip()
            email = input("Email: ").strip()
            telefone = input("Telefone: ").strip()
            senha = input("Senha: ").strip()
            tipo = input("Tipo (comum/administrador): ").strip().lower()
            sistema_biblioteca.inserir_usuario(nome, sobrenome, endereco, email, telefone, senha, tipo)

        elif opcao == "3":
            # Chama o método específico para exibir todos os usuários cadastrados
            sistema_biblioteca.exibir_usuarios()
        
        elif opcao == "4":
            # Chama o método específico para realizar um empréstimo
            id_usuario = int(input("ID do Usuário: ").strip())
            id_livro = int(input("ID do Livro: ").strip())
            data_emprestimo = input("Data de Empréstimo (AAAA-MM-DD): ").strip()
            data_devolucao = input("Data de Devolução (AAAA-MM-DD): ").strip()
            sistema_biblioteca.realizar_emprestimo(id_usuario, id_livro, data_emprestimo, data_devolucao)
        
        elif opcao == "5":
            # Chama o método específico para atualizar a data de devolução de um empréstimo
            id_emprestimo = int(input("ID do Empréstimo: ").strip())
            nova_data_devolucao = input("Nova Data de Devolução (AAAA-MM-DD): ").strip()
            sistema_biblioteca.atualizar_data_devolucao(id_emprestimo, nova_data_devolucao)
        
        elif opcao == "6":
            # Chama o método específico para exibir todos os livros emprestados no momento
            sistema_biblioteca.exibir_livros_emprestados()
        
        elif opcao == "7":
            # Chama o método específico para exibir todos os livros cadastrados no banco de dados
            sistema_biblioteca.exibir_todos_os_livros()
        
        elif opcao == "8" and usuario_logado[6] == "administrador":
            # Código para a opção exclusiva de administrador
            print("Opção exclusiva de administrador executada.")
        
        elif opcao == "0":
            # Encerra o loop e termina o programa
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

if __name__ == "_main_":
    main()
    input("Pressione Enter para sair...")