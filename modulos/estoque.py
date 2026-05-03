from utils.banco import carregar, salvar
from utils.validacoes import ler_int, ler_float, ler_string

def cadastrar_produto():
    produtos = carregar("produtos")

    nome = ler_string("Nome do produto: ")
    preco = ler_float("Preço: ")
    quantidade = ler_int("Quantidade inicial: ")

    novo_produto = {
       "id": max((p["id"] for p in produtos), default=0) + 1,
        "nome": nome,
        "preco": preco,
        "quantidade": quantidade
    }

    produtos.append(novo_produto)
    salvar("produtos", produtos)

    print("Produto cadastrado com sucesso!")

def listar_produtos():
    produtos = carregar("produtos")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("\n=== LISTA DE PRODUTOS ===")
    for produto in produtos:
        print(f"ID: {produto['id']}")
        print(f"Nome: {produto['nome']}")
        print(f"Preço: R$ {produto['preco']}")
        print(f"Quantidade: {produto['quantidade']}")
        print("-" * 20)

def entrada_estoque():
    produtos = carregar("produtos")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    listar_produtos()
    id_produto = ler_int("Digite o ID do produto: ")

    for produto in produtos:
        if produto["id"] == id_produto:
            quantidade = ler_int("Quantidade de entrada: ")
            produto["quantidade"] += quantidade
            salvar("produtos", produtos)
            print("Estoque atualizado com sucesso!")
            return

    print("Produto não encontrado.")

def saida_estoque():
    produtos = carregar("produtos")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    listar_produtos()
    id_produto = ler_int("Digite o ID do produto: ")

    for produto in produtos:
        if produto["id"] == id_produto:
            quantidade = ler_int("Quantidade de saída: ")

            if quantidade > produto["quantidade"]:
                print("Estoque insuficiente!")
                return

            produto["quantidade"] -= quantidade
            salvar("produtos", produtos)
            print("Saída registrada com sucesso!")
            return

    print("Produto não encontrado.")