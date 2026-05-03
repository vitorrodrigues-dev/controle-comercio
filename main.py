from utils.banco import inicializar_dados
from modulos.estoque import cadastrar_produto, listar_produtos, entrada_estoque, saida_estoque
from modulos.vendas import registrar_venda
from modulos.relatorios import relatorio_vendas, relatorio_vendas_hoje, relatorio_lucro
from modulos.gastos import registrar_gasto
from modulos.avisos import verificar_estoque_baixo
from modulos.producao import registrar_producao
from modulos.perdas import registrar_perda
from modulos.contas import registrar_conta
from modulos.relatorios import relatorio_producao_perdas

def menu():
    print("\n=== MENU ===")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("3 - Entrada de estoque")
    print("4 - Saída de estoque")
    print("5 - Registrar venda")
    print("6 - Relatório de vendas")
    print("7 - Registrar gasto")
    print("8 - Relatório lucro")
    print("9 - Registrar produção")
    print("10 - Registrar perda")
    print("11 - Registrar conta")
    print("12 - Relatório produção x perdas")
    print("13 - Sair")

def main():
    print("Iniciando sistema...")
    inicializar_dados()
    print("Sistema pronto!")

    verificar_estoque_baixo()

    print("Sistema pronto!")

    while True:
        menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            listar_produtos()
        elif opcao == "3":
            entrada_estoque()
        elif opcao == "4":
            saida_estoque()
        elif opcao == "5":
            registrar_venda()
        elif opcao == "6":
            relatorio_vendas()
        elif opcao == "7":
            registrar_gasto()
        elif opcao == "8":
            relatorio_lucro()
        elif opcao == "9":
            registrar_producao()
        elif opcao == "10":
            registrar_perda()
        elif opcao == "11":
            registrar_conta()
        elif opcao == "12":
            relatorio_producao_perdas()
        elif opcao == "13":    
            print("Saindo...")    
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
