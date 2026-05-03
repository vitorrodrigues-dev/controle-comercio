from utils.banco import carregar, salvar
from utils.validacoes import ler_float, ler_string

def registrar_conta():
    contas = carregar("contas")

    tipo = ler_string("Tipo (entrada/saida): ")
    valor = ler_float("Valor: ")
    descricao = ler_string("Descrição: ")

    conta = {
        "id": max((c["id"] for c in contas), default=0) + 1,
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao
    }

    contas.append(conta)
    salvar("contas", contas)

    print("Conta registrada!")