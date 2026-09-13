import re
from datetime import datetime
from validacoes import validar_cpf, formatar_cpf
from gerenciador_dados import carregar_dados, salvar_dados

def autenticar_usuario(dados):
    """Autentica usuário por CPF com validação rigorosa"""
    while True:
        cpf_input = input("\nDigite o CPF (somente números): ").strip()
        cpf_limpo = re.sub(r'[^0-9]', '', cpf_input)
        
        if not validar_cpf(cpf_limpo):
            print("CPF inválido! Digite um CPF válido.")
            continue
        
        if cpf_limpo not in dados['usuarios']:
            usuario = input("\nDigite o Nome para Novo Registro: ").strip()
            print("\n=== Novo usuário registrado! ===")
            dados['usuarios'][cpf_limpo] = {
                'nome': usuario,
                'cpf_formatado': formatar_cpf(cpf_limpo),
                'livros': [],
                'livros doados': 0,
                'divida': 0.0,
                'creditos': 0.0
            }
            salvar_dados(dados)
        
        return cpf_limpo

def gerenciar_emprestimo(dados, usuario):
    """Lógica da Opção 1: Empréstimo de Livros"""
    if not any(categoria['itens'] for categoria in dados['livros']):
        print("\nNão há livros disponíveis no momento!")
        return

    print("\nLivros disponíveis:")
    print("-------------------------------------------")
    for i, categoria in enumerate(dados["livros"], 1):
        print(f"{i}. {categoria['categoria']}")
    print("-------------------------------------------")
    
    try:
        escolha_categoria = int(input("\nQual categoria?: ")) - 1
        if 0 <= escolha_categoria < len(dados['livros']):
            cat = dados['livros'][escolha_categoria]
            print(f"\nLivros em {cat['categoria']}:")
            for j, livro in enumerate(cat['itens'], 1):
                print(f"{j}. {livro}")
                
            escolha_livro = int(input("\nEscolha o número do livro: ")) - 1
            if 0 <= escolha_livro < len(cat['itens']):
                livro_escolhido = cat['itens'].pop(escolha_livro)
                
                usuario['livros'].append({
                    'titulo': livro_escolhido,
                    'data_emprestimo': datetime.now().strftime("%d/%m/%Y %H:%M")
                })
                print(f"\nSucesso! '{livro_escolhido}' emprestado.")
                salvar_dados(dados)
            else:
                print("Livro inválido.")
        else:
            print("Categoria inválida.")
    except ValueError:
        print("Entrada inválida. Digite números.")

def menu_principal(dados, cpf):
    """Interface principal do sistema"""
    while True:
        usuario = dados['usuarios'][cpf]
        print(f"\n{' MENU PRINCIPAL ':=^40}")
        print(f"\nNome: {usuario['nome']}")
        print(f"CPF: {usuario['cpf_formatado']}")
        print(f"Livros emprestados: {len(usuario['livros'])}")
        print(f"Dívida atual: R$ {usuario['divida']:.2f}")
        print(f"Livros doados: {usuario['livros doados']}")
        print(f"Créditos disponíveis: R$ {usuario['creditos']:.2f}")
        print("-------------------------------------------")
        print("1. Emprestimo de livro")
        print("2. Devolução de livro (Não implementado)")
        print("3. Doar livro (Não implementado)")
        print("4. Pagar dívida (Não implementado)")
        print("5. Tela Inicial Sistema (Sair do Menu)")
        print("6. Apagar usuário (Não implementado)")
        print("7. Mudar nome de Usuario (Não implementado)")
        print("-------------------------------------------")

        opcao = input("\nEscolha uma opção: ")
        
        if opcao == '1':
            gerenciar_emprestimo(dados, usuario)
        elif opcao == '5':
            print("Retornando à tela inicial...")
            break
        elif opcao in ['2', '3', '4', '6', '7']:
            print(f"\nA opção {opcao} ainda não foi implementada neste menu.")
        else:
            print("Opção inválida!")

def main():
    """Fluxo principal do programa"""
    dados = carregar_dados()
    print("=== BEM-VINDO AO SISTEMA DE BIBLIOTECA ===")
    cpf_logado = autenticar_usuario(dados)
    menu_principal(dados, cpf_logado)

if __name__ == "__main__":
    main()