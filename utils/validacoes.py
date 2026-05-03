def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro válido.")

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Digite um número válido.")

def ler_string(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("Não pode ser vazio.")