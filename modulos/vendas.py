from utils.banco import carregar, salvar
from utils.validacoes import ler_int
from modulos.estoque import listar_produtos
from datetime import datetime

def registrar_venda():
    produtos = carregar("produtos")
    vendas   = carregar("vendas")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    listar_produtos()
    id_produto = ler_int("Digite o ID do produto: ")

    for produto in produtos:
        if produto["id"] == id_produto:
            quantidade = ler_int("Quantidade vendida: ")

            if quantidade > produto["quantidade"]:
                print("Estoque insuficiente!")
                return

            total = quantidade * produto["preco"]

            venda = {
                "id":         max((v["id"] for v in vendas), default=0) + 1,
                "produto_id": id_produto,
                "produto":    produto["nome"],
                "quantidade": quantidade,
                "total":      round(total, 2),
                "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            produto["quantidade"] -= quantidade

            vendas.append(venda)
            salvar("vendas", vendas)
            salvar("produtos", produtos)

            print(f"Venda registrada! Total: R$ {total:.2f}")
            return

    print("Produto não encontrado.")