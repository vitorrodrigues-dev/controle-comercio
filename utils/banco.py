import json
import os
from config import DADOS_DIR, ARQUIVOS

def inicializar_dados():
    os.makedirs(DADOS_DIR, exist_ok=True)
    
    for nome, caminho in ARQUIVOS.items():
        if not os.path.exists(caminho):
            salvar(nome, [])
            print(f"Arquivo criado: {nome}.json")

def carregar(nome):
    caminho = ARQUIVOS.get(nome)
    
    if not caminho:
        print(f"Erro: arquivo '{nome}' não existe no config.")
        return []
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Erro: {nome}.json está corrompido.")
        return []

def salvar(nome, dados):
    caminho = ARQUIVOS.get(nome)
    
    if not caminho:
        print(f"Erro: arquivo '{nome}' não existe no config.")
        return False
    
    try:
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Erro ao salvar {nome}: {e}")
        return False