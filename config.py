import os

# Caminhos do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

# Arquivos JSON
ARQUIVOS = {
    "produtos"   : os.path.join(DADOS_DIR, "produtos.json"),
    "vendas"     : os.path.join(DADOS_DIR, "vendas.json"),
    "producao"   : os.path.join(DADOS_DIR, "producao.json"),
    "contas"     : os.path.join(DADOS_DIR, "contas.json"),
    "perdas"     : os.path.join(DADOS_DIR, "perdas.json"),
    "gastos": os.path.join(DADOS_DIR, "gastos.json"),
}

# Informações do sistema
SISTEMA = {
    "nome"    : "Controle Comercio",
    "versao"  : "1.0.0",
    "autor"   : "Vitor",
}
# Configurações de alerta
ESTOQUE_MINIMO = 5