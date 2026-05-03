from utils.banco import carregar, salvar
from utils.validacoes import ler_int, ler_string
from datetime import datetime

def registrar_perda():
    perdas = carregar("perdas")

    produto    = ler_string("Produto: ")
    quantidade = ler_int("Quantidade perdida: ")
    motivo     = ler_string("Motivo: ")

    perda = {
        "id":         max((p.get("id", 0) for p in perdas), default=0) + 1,
        "produto":    produto,
        "quantidade": quantidade,
        "motivo":     motivo,
        "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    perdas.append(perda)
    salvar("perdas", perdas)

    print("Perda registrada!")