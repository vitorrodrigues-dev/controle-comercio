from utils.banco import carregar, salvar
from utils.validacoes import ler_float, ler_string
from datetime import datetime

def registrar_gasto():
    gastos = carregar("gastos")

    descricao = ler_string("Descrição do gasto: ")
    valor = ler_float("Valor do gasto: ")

    gasto = {
        "id": max((g["id"] for g in gastos), default=0) + 1,
        "descricao": descricao,
        "valor": valor,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    gastos.append(gasto)
    salvar("gastos", gastos)

    print(f"Gasto registrado: R$ {valor:.2f}")