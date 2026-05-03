from utils.banco import carregar
from datetime import datetime

def relatorio_vendas():
    vendas = carregar("vendas")

    if not vendas:
        print("Nenhuma venda registrada.")
        return

    total = 0

    print("\n=== RELATÓRIO DE VENDAS ===")

    for venda in vendas:
        print(f"ID: {venda['id']} | Total: R$ {venda['total']:.2f} | Data: {venda['data']}")
        total += venda["total"]

    print("\n------------------------")
    print(f"TOTAL VENDIDO: R$ {total:.2f}")

def relatorio_vendas_hoje():
    vendas = carregar("vendas")

    if not vendas:
        print("Nenhuma venda registrada.")
        return

    hoje = datetime.now().strftime("%Y-%m-%d")
    total = 0

    print("\n=== VENDAS DE HOJE ===")

    for venda in vendas:
        if venda["data"].startswith(hoje):
            print(f"ID: {venda['id']} | Total: R$ {venda['total']:.2f}")
            total += venda["total"]

    print("\n------------------------")
    print(f"TOTAL HOJE: R$ {total:.2f}")

def relatorio_lucro():
    vendas = carregar("vendas")
    gastos = carregar("gastos")

    total_vendas = sum(v["total"] for v in vendas)
    total_gastos = sum(g["valor"] for g in gastos)

    lucro = total_vendas - total_gastos

    print("\n=== RELATÓRIO DE LUCRO ===")
    print(f"Total vendido: R$ {total_vendas:.2f}")
    print(f"Total gasto: R$ {total_gastos:.2f}")
    print("------------------------")

    if lucro > 0:
        print(f"LUCRO: R$ {lucro:.2f}")
    elif lucro < 0:
        print(f"PREJUÍZO: R$ {abs(lucro):.2f}")
    else:
        print("Empate (sem lucro)")

def relatorio_producao_perdas():
    producao = carregar("producao")
    perdas = carregar("perdas")

    if not isinstance(producao, list):
        producao = []

    if not isinstance(perdas, list):
        perdas = []

    if not producao and not perdas:
        print("Nenhum registro encontrado em produção e perdas.")
        return

    total_produzido = sum(p.get("quantidade", 0) for p in producao)
    total_perdido = sum(p.get("quantidade", 0) for p in perdas)

    if total_produzido > 0:
        desperdicio = (total_perdido / total_produzido) * 100
    else:
        desperdicio = 0

    eficiencia = 100 - desperdicio

    print("\n=== RELATÓRIO PRODUÇÃO x PERDAS ===")
    print(f"Total produzido: {total_produzido}")
    print(f"Total perdido: {total_perdido}")
    print(f"Desperdício: {desperdicio:.2f}%")
    print(f"Eficiência: {eficiencia:.2f}%")