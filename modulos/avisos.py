from utils.banco import carregar
from config import ESTOQUE_MINIMO

def verificar_estoque_baixo():
    produtos = carregar("produtos")

    if not produtos:
        return

    print("\n=== ALERTAS ===")

    alerta = False

    for produto in produtos:
        if produto["quantidade"] <= ESTOQUE_MINIMO:
            print(f"⚠️ Estoque baixo: {produto['nome']} (Qtd: {produto['quantidade']})")
            alerta = True

    if not alerta:
        print("Nenhum alerta no momento.")