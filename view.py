def exibir_menu(usuario_logado):
    """
    Exibe o menu principal da aplicação com opções para o usuário, após o login.

    Esta função imprime o menu principal da aplicação com várias opções, incluindo inserir um novo livro,
    inserir um novo usuário, exibir todos os usuários cadastrados, realizar um empréstimo, atualizar a data de
    devolução de um empréstimo, exibir todos os livros emprestados no momento, exibir todos os livros cadastrados
    no banco de dados e, se o usuário logado for administrador, uma opção exclusiva de administrador.
    """
    print("\nMenu Principal:")
    print("1. Inserir um novo livro")
    print("2. Inserir um novo usuário")
    print("3. Exibir todos os usuários cadastrados")
    print("4. Realizar um empréstimo")
    print("5. Atualizar data de devolução de um empréstimo")
    print("6. Exibir todos os livros emprestados no momento")
    print("7. Exibir todos os livros cadastrados no banco de dados")
    
    if usuario_logado[6] == "administrador":
        print("8. Opção exclusiva de administrador")

    print("0. Sair")
    
    opcao = input("Digite a opção desejada: ")
    return opcao