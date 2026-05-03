from flask import Flask, render_template, request, redirect, url_for
from utils.banco import carregar, salvar, inicializar_dados
from config import ESTOQUE_MINIMO
from datetime import datetime, date, timedelta

# ── helpers de conversão segura ────────────────────────────────────────────────
def safe_int(valor, default=0):
    try:
        return int(valor)
    except (ValueError, TypeError):
        return default

def safe_float(valor, default=0.0):
    try:
        return float(valor)
    except (ValueError, TypeError):
        return default

app = Flask(__name__)
inicializar_dados()

DIAS_AVISO_VENCIMENTO = 7   

def calcular_vencimento(data_str, hoje):
    if not data_str:
        return None, None

    try:
        data = date.fromisoformat(data_str)
        dias = (data - hoje).days

        if dias < 0:
            status = "vencido"
        elif dias <= DIAS_AVISO_VENCIMENTO:
            status = "alerta"
        else:
            status = "ok"

        return dias, status

    except ValueError:
        return None, None
# ══════════════════════════════════════════════════════════════════════════════
#  PRODUTOS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/")
def produtos():
    lista   = carregar("produtos")
    hoje    = date.today()
    baixo   = [p for p in lista if p["quantidade"] <= ESTOQUE_MINIMO]
    # produtos com vencimento próximo ou vencidos
    venc    = []
    for p in lista:
        val = p.get("validade", "")
        if val:
            try:
                d = date.fromisoformat(val)
                dias = (d - hoje).days
                if dias <= DIAS_AVISO_VENCIMENTO:
                    venc.append({**p, "_dias_venc": dias})
            except ValueError:
                pass
    return render_template("index.html",
        secao    = "produtos",
        produtos = lista,
        total    = len(lista),
        baixo    = len(baixo),
        venc     = len(venc),
    )

@app.route("/cadastrar-produto", methods=["POST"])
def cadastrar_produto():
    nome      = request.form.get("nome", "").strip()
    preco     = request.form.get("preco")
    qtd       = request.form.get("quantidade")
    validade  = request.form.get("validade", "").strip()

    if nome and preco and qtd:
        preco_val = safe_float(preco)
        qtd_val   = safe_int(qtd)
        if preco_val < 0 or qtd_val < 0:
            return redirect(url_for("produtos"))
        lista = carregar("produtos")
        lista.append({
            "id":         max((p["id"] for p in lista), default=0) + 1,
            "nome":       nome,
            "preco":      preco_val,
            "quantidade": qtd_val,
            "validade":   validade,
        })
        salvar("produtos", lista)
    return redirect(url_for("produtos"))

@app.route("/excluir-produto/<int:pid>", methods=["POST"])
def excluir_produto(pid):
    lista = carregar("produtos")
    lista = [p for p in lista if p["id"] != pid]
    salvar("produtos", lista)
    return redirect(url_for("produtos"))


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRADA DE ESTOQUE
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/entrada")
def entrada():
    return render_template("index.html", secao="entrada", produtos=carregar("produtos"))

@app.route("/entrada", methods=["POST"])
def registrar_entrada():
    produto_id = safe_int(request.form.get("produto_id"))
    quantidade = safe_int(request.form.get("quantidade"))
    if produto_id <= 0 or quantidade <= 0:
        return redirect(url_for("entrada"))
    lista = carregar("produtos")
    for p in lista:
        if p["id"] == produto_id:
            p["quantidade"] += quantidade
            break
    salvar("produtos", lista)
    return redirect(url_for("entrada"))


# ══════════════════════════════════════════════════════════════════════════════
#  SAÍDA DE ESTOQUE
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/saida", methods=["GET", "POST"])
def registrar_saida():
    lista = carregar("produtos")
    if request.method == "POST":
        produto_id = safe_int(request.form.get("produto_id"))
        quantidade = safe_int(request.form.get("quantidade"))
        if produto_id <= 0 or quantidade <= 0:
            return redirect(url_for("registrar_saida"))
        for p in lista:
            if p["id"] == produto_id:
                if quantidade <= p["quantidade"]:
                    p["quantidade"] -= quantidade
                    salvar("produtos", lista)
                    return redirect(url_for("registrar_saida"))
                else:
                    return render_template("index.html",
                        secao="saida", produtos=lista,
                        erro="Estoque insuficiente!")
    return render_template("index.html", secao="saida", produtos=lista, erro=None)


# ══════════════════════════════════════════════════════════════════════════════
#  VENDAS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/venda")
def venda():
    return render_template("index.html", secao="venda", produtos=carregar("produtos"))

@app.route("/venda", methods=["POST"])
def registrar_venda():
    produto_id = safe_int(request.form.get("produto_id"))
    quantidade = safe_int(request.form.get("quantidade"))
    if produto_id <= 0 or quantidade <= 0:
        return redirect(url_for("venda"))
    lista  = carregar("produtos")
    vendas = carregar("vendas")
    for p in lista:
        if p["id"] == produto_id:
            if quantidade <= p["quantidade"]:
                total = round(quantidade * p["preco"], 2)
                vendas.append({
                    "id":         max((v["id"] for v in vendas), default=0) + 1,
                    "produto_id": produto_id,
                    "produto":    p["nome"],
                    "quantidade": quantidade,
                    "total":      total,
                    "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                p["quantidade"] -= quantidade
                salvar("vendas", vendas)
                salvar("produtos", lista)
            break
    return redirect(url_for("rel_vendas"))

@app.route("/relatorio-vendas")
def rel_vendas():
    vendas     = carregar("vendas")
    hoje_str   = datetime.now().strftime("%Y-%m-%d")
    mes_str    = datetime.now().strftime("%Y-%m")
    total_geral = round(sum(v["total"] for v in vendas), 2)
    total_hoje  = round(sum(v["total"] for v in vendas if v["data"].startswith(hoje_str)), 2)
    total_mes   = round(sum(v["total"] for v in vendas if v["data"].startswith(mes_str)), 2)
    return render_template("index.html",
        secao       = "rel-vendas",
        vendas      = vendas,
        total       = total_geral,
        total_hoje  = total_hoje,
        total_mes   = total_mes,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  GASTOS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/gastos")
def gastos():
    return render_template("index.html", secao="gastos", gastos=carregar("gastos"))

@app.route("/gastos", methods=["POST"])
def registrar_gasto():
    descricao = request.form.get("descricao", "").strip()
    valor     = request.form.get("valor")
    if descricao and valor:
        lista = carregar("gastos")
        lista.append({
            "id":        max((g["id"] for g in lista), default=0) + 1,
            "descricao": descricao,
            "valor":     round(safe_float(valor), 2),
            "data":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        salvar("gastos", lista)
    return redirect(url_for("gastos"))


# ══════════════════════════════════════════════════════════════════════════════
#  CONTAS (boletos) — com vencimento
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/contas")
def contas():
    lista  = carregar("contas")
    hoje   = date.today()
    for c in lista:
    dias, status = calcular_vencimento(c.get("vencimento"), hoje)
    c["_dias_venc"] = dias
    c["_status"] = status
    total_entrada = round(sum(c["valor"] for c in lista if c.get("tipo") == "entrada"), 2)
    total_saida   = round(sum(c["valor"] for c in lista if c.get("tipo") == "saida"), 2)
    saldo         = round(total_entrada - total_saida, 2)
    return render_template("index.html",
        secao         = "contas",
        contas        = lista,
        total_entrada = total_entrada,
        total_saida   = total_saida,
        saldo         = saldo,
        dias_aviso    = DIAS_AVISO_VENCIMENTO,
    )

@app.route("/contas", methods=["POST"])
def registrar_conta():
    tipo       = request.form.get("tipo", "").strip()
    valor      = request.form.get("valor")
    descricao  = request.form.get("descricao", "").strip()
    vencimento = request.form.get("vencimento", "").strip()
    if tipo in ["entrada", "saida"] and valor and descricao:
        lista = carregar("contas")
        lista.append({
            "id":         max((c.get("id", 0) for c in lista), default=0) + 1,
            "tipo":       tipo,
            "valor":      round(safe_float(valor), 2),
            "descricao":  descricao,
            "vencimento": vencimento,
            "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        salvar("contas", lista)
    return redirect(url_for("contas"))


# ══════════════════════════════════════════════════════════════════════════════
#  LUCRO — por dia e mês
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/lucro")
def lucro():
    vendas = carregar("vendas")
    gastos = carregar("gastos")
    hoje_str = datetime.now().strftime("%Y-%m-%d")
    mes_str  = datetime.now().strftime("%Y-%m")

    tv_total = round(sum(v["total"] for v in vendas), 2)
    tg_total = round(sum(g["valor"] for g in gastos), 2)
    res_total = round(tv_total - tg_total, 2)

    tv_hoje = round(sum(v["total"] for v in vendas if v["data"].startswith(hoje_str)), 2)
    tg_hoje = round(sum(g["valor"] for g in gastos if g["data"].startswith(hoje_str)), 2)
    res_hoje = round(tv_hoje - tg_hoje, 2)

    tv_mes = round(sum(v["total"] for v in vendas if v["data"].startswith(mes_str)), 2)
    tg_mes = round(sum(g["valor"] for g in gastos if g["data"].startswith(mes_str)), 2)
    res_mes = round(tv_mes - tg_mes, 2)

    def tipo_resultado(r):
        return "lucro" if r > 0 else "prejuizo" if r < 0 else "empate"

    return render_template("index.html",
        secao        = "lucro",
        # hoje
        tv_hoje      = tv_hoje,
        tg_hoje      = tg_hoje,
        res_hoje     = res_hoje,
        tipo_hoje    = tipo_resultado(res_hoje),
        # mês
        tv_mes       = tv_mes,
        tg_mes       = tg_mes,
        res_mes      = res_mes,
        tipo_mes     = tipo_resultado(res_mes),
        # total geral
        total_vendas = tv_total,
        total_gastos = tg_total,
        resultado    = res_total,
        tipo         = tipo_resultado(res_total),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  PRODUÇÃO
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/producao")
def producao():
    return render_template("index.html", secao="producao")

@app.route("/producao", methods=["POST"])
def registrar_producao():
    produto    = request.form.get("produto", "").strip()
    quantidade = request.form.get("quantidade")
    if produto and quantidade:
        lista = carregar("producao")
        lista.append({
            "id":         max((p.get("id", 0) for p in lista), default=0) + 1,
            "produto":    produto,
            "quantidade": safe_int(quantidade),
            "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        salvar("producao", lista)
    return redirect(url_for("producao"))


# ══════════════════════════════════════════════════════════════════════════════
#  PERDAS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/perdas")
def perdas():
    return render_template("index.html", secao="perdas")

@app.route("/perdas", methods=["POST"])
def registrar_perda():
    produto    = request.form.get("produto", "").strip()
    quantidade = request.form.get("quantidade")
    motivo     = request.form.get("motivo", "").strip()
    if produto and quantidade and motivo:
        lista = carregar("perdas")
        lista.append({
            "id":         max((p.get("id", 0) for p in lista), default=0) + 1,
            "produto":    produto,
            "quantidade": safe_int(quantidade),
            "motivo":     motivo,
            "data":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
        salvar("perdas", lista)
    return redirect(url_for("perdas"))


# ══════════════════════════════════════════════════════════════════════════════
#  RELATÓRIO PRODUÇÃO x PERDAS
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/relatorio-producao")
def rel_producao():
    producao = carregar("producao")
    perdas   = carregar("perdas")
    total_p  = sum(p.get("quantidade", 0) for p in producao)
    total_l  = sum(p.get("quantidade", 0) for p in perdas)
    desp     = round((total_l / total_p) * 100, 2) if total_p > 0 else 0
    efic     = round(100 - desp, 2)
    return render_template("index.html",
        secao           = "rel-producao",
        total_produzido = total_p,
        total_perdido   = total_l,
        desperdicio     = desp,
        eficiencia      = efic,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  ALERTAS — estoque baixo + vencimentos próximos
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/alertas")
def alertas():
    produtos = carregar("produtos")
    contas   = carregar("contas")
    hoje     = date.today()

    baixo = [p for p in produtos if p["quantidade"] <= ESTOQUE_MINIMO]

    venc_produtos = []
    for p in produtos:
        val = p.get("validade", "")
        if val:
            try:
                d = date.fromisoformat(val)
                dias = (d - hoje).days
                if dias <= DIAS_AVISO_VENCIMENTO:
                    venc_produtos.append({**p, "_dias": dias})
            except ValueError:
                pass

    venc_contas = []
    for c in contas:
        val = c.get("vencimento", "")
        if val:
            try:
                d = date.fromisoformat(val)
                dias = (d - hoje).days
                if dias <= DIAS_AVISO_VENCIMENTO:
                    venc_contas.append({**c, "_dias": dias})
            except ValueError:
                pass

    return render_template("index.html",
        secao         = "alertas",
        alertas       = baixo,
        minimo        = ESTOQUE_MINIMO,
        venc_produtos = venc_produtos,
        venc_contas   = venc_contas,
        dias_aviso    = DIAS_AVISO_VENCIMENTO,
    )


# ══════════════════════════════════════════════════════════════════════════════
#  START
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
