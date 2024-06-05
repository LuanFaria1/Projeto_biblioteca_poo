from view import exibir_menu_administrador, exibir_menu_comum
from biblioteca import Biblioteca, Usuario, Administrador
from banco_de_dados import conectar_bd, consultar_usuario_por_credenciais

def cadastrar_usuario(conn):
    nome = input("Nome: ").strip()
    sobrenome = input("Sobrenome: ").strip()
    endereco = input("Endereço: ").strip()
    email = input("Email: ").strip()
    telefone = input("Telefone: ").strip()
    senha = input("Senha: ").strip()
    tipo = input("Tipo de usuário (comum/administrador): ").strip().lower()

    if tipo not in ["comum", "administrador"]:
        print("Tipo de usuário inválido.")
        return

    usuario = Usuario(nome, senha, endereco, email, telefone, tipo) if tipo == "comum" else Administrador(nome, senha)
    usuario.inserir_usuario_bd(conn)
    print("Usuário cadastrado com sucesso!")

def fazer_login(conn):
    nome_usuario = input("Nome de usuário: ").strip()
    senha = input("Senha: ").strip()
    
    usuario = consultar_usuario_por_credenciais(conn, nome_usuario, senha)
    if usuario:
        print(f"Usuário encontrado") 
        return usuario
    else:
        print("Nome de usuário ou senha incorretos. Tente novamente.")
        return None

def menu_administrador(sistema_biblioteca):
    while True:
        exibir_menu_administrador()
        opcao = input("Digite a opção desejada: ").strip()
        
        if opcao == "1":
            titulo = input("Título do Livro: ").strip()
            autor = input("Autor do Livro: ").strip()
            editora = input("Editora do Livro: ").strip()
            ano_publicacao = int(input("Ano de Publicação: ").strip())
            isbn = input("ISBN do Livro: ").strip()
            sistema_biblioteca.inserir_livro(titulo, autor, editora, ano_publicacao, isbn)
            
        elif opcao == "2":
            nome = input("Nome: ").strip()
            sobrenome = input("Sobrenome: ").strip()
            endereco = input("Endereço: ").strip()
            email = input("Email: ").strip()
            telefone = input("Telefone: ").strip()
            senha = input("Senha: ").strip()
            tipo = input("Tipo (comum/administrador): ").strip().lower()
            sistema_biblioteca.inserir_usuario(nome, sobrenome, endereco, email, telefone, senha, tipo)
            
        elif opcao == "3":
            sistema_biblioteca.exibir_usuarios()
            
        elif opcao == "4":
            id_usuario = int(input("ID do Usuário: ").strip())
            id_livro = int(input("ID do Livro: ").strip())
            data_emprestimo = input("Data de Empréstimo (AAAA-MM-DD): ").strip()
            data_devolucao = input("Data de Devolução (AAAA-MM-DD): ").strip()
            sistema_biblioteca.realizar_emprestimo(id_usuario, id_livro, data_emprestimo, data_devolucao)
            
        elif opcao == "5":
            id_emprestimo = int(input("ID do Empréstimo: ").strip())
            nova_data_devolucao = input("Nova Data de Devolução (AAAA-MM-DD): ").strip()
            sistema_biblioteca.atualizar_data_devolucao(id_emprestimo, nova_data_devolucao)
            
        elif opcao == "6":
            sistema_biblioteca.exibir_livros_emprestados()
            
        elif opcao == "7":
            sistema_biblioteca.exibir_todos_os_livros()
            
        elif opcao == "0":
            print("Saindo do sistema...")
            break
            
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

def menu_comum(sistema_biblioteca, usuario_logado):
    while True:
        exibir_menu_comum()
        opcao = input("Digite a opção desejada: ").strip()
        
        if opcao == "1":
            id_livro = int(input("ID do Livro: ").strip())
            data_emprestimo = input("Data de Empréstimo (AAAA-MM-DD): ").strip()
            data_devolucao = input("Data de Devolução (AAAA-MM-DD): ").strip()
            sistema_biblioteca.realizar_emprestimo(usuario_logado[0], id_livro, data_emprestimo, data_devolucao)
            
        elif opcao == "2":
            sistema_biblioteca.exibir_todos_os_livros()
            
        elif opcao == "3":
            id_emprestimo = int(input("ID do Empréstimo: ").strip())
            nova_data_devolucao = input("Nova Data de Devolução (AAAA-MM-DD): ").strip()
            sistema_biblioteca.atualizar_data_devolucao(id_emprestimo, nova_data_devolucao)
            
        elif opcao == "4":
            sistema_biblioteca.excluir_usuario(usuario_logado[0])
            print("Usuário excluído com sucesso.")
            break
            
        elif opcao == "0":
            print("Saindo do sistema...")
            break
            
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

def main():
    conn = conectar_bd()
    if conn is None:
        print("Erro ao conectar ao banco de dados.")
        return

    sistema_biblioteca = Biblioteca()

    while True:
        print("Bem vindo a nossa biblioteca!")
        print("Digite 1 caso você for um usuário administrador")
        print("Digite 2 caso seja um usuário comum")    
        opcao_tipo_usuario = input("Digite a opção desejada: ").strip()

        if opcao_tipo_usuario == "1":
            usuario_logado = fazer_login(conn)
            if usuario_logado and usuario_logado[7] == "administrador":
                print("Login de administrador bem-sucedido!")
                menu_administrador(sistema_biblioteca)
                break
            else:
                print("Somente administradores podem acessar esta opção.")
                
        elif opcao_tipo_usuario == "2":
            possui_cadastro = input("Você possui cadastro? (s/n): ").strip().lower()
            if possui_cadastro == "s":
                usuario_logado = fazer_login(conn)
                if usuario_logado:
                    menu_comum(sistema_biblioteca, usuario_logado)
                    break
                else:
                    print("Erro no login. Tente novamente.")
            elif possui_cadastro == "n":
                cadastrar_usuario(conn)
            else:
                print("Opção inválida. Por favor, selecione uma opção válida.")
        else:
            print("Opção inválida. Por favor, selecione uma opção válida.")

if __name__ == "__main__":
    main()
