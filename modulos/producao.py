from utils.banco import carregar, salvar
from utils.validacoes import ler_int, ler_string
from datetime import datetime

def registrar_producao():
    producao = carregar("producao")

    produto    = ler_string("Produto: ")
    quantidade = ler_int("Quantidade produzida: ")

    nova_producao = {
        "id":         max((p.get("id", 0) for p in producao), default=0) + 1,
        "produto":    produto,
        "quantidade": quantidade,
        "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    producao.append(nova_producao)
    salvar("producao", producao)

    print("Produção registrada com sucesso!")