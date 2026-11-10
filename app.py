import os
from functools import wraps
from flask import Flask, jsonify, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("FRETE_STONE_SECRET_KEY"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 12,
)

PAGE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#075334">
<title>Frete Stone</title>
<style>
:root{--green:#075334;--deep:#043c27;--lime:#9eff00;--paper:#f3f7f4;--ink:#163528;--muted:#64756b;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,system-ui,-apple-system,Segoe UI,Arial,sans-serif}
header{position:sticky;top:0;z-index:5;background:#fffF;border-bottom:1px solid #e2ebe5;backdrop-filter:blur(12px)}
.nav{max-width:1160px;margin:auto;padding:15px 22px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{font-weight:900;letter-spacing:-1px;color:var(--green);font-size:22px}.brand span{color:#7cbd00}
nav{display:flex;gap:10px;align-items:center;flex-wrap:wrap}nav a{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:10px 16px;border-radius:12px;background:#e5f2e9;color:var(--green);text-decoration:none;font-size:14px;font-weight:800;border:1px solid #cfe3d5;transition:transform .18s ease,background .18s ease,box-shadow .18s ease}nav a:hover{background:#d4eadb;transform:translateY(-1px);box-shadow:0 5px 14px #07533418}nav a.navbtn{background:var(--lime);color:var(--deep);border-color:var(--lime);padding:11px 20px;box-shadow:0 6px 18px #9eff0038}.navbtn,.btn{display:inline-flex;align-items:center;justify-content:center;background:var(--lime);color:var(--deep);border:0;border-radius:12px;padding:13px 18px;font-weight:850;text-decoration:none;cursor:pointer;transition:transform .18s ease,box-shadow .18s ease}.btn:hover,.navbtn:hover{transform:translateY(-2px);box-shadow:0 8px 20px #9eff0045}
.hero{background:radial-gradient(circle at 80% 25%,#176c45 0,#075334 35%,#043c27 78%);color:white;overflow:hidden}.hero-in{max-width:1160px;margin:auto;padding:82px 22px 76px;display:grid;grid-template-columns:1.1fr .9fr;gap:38px;align-items:center}.eyebrow{color:var(--lime);font-weight:850;text-transform:uppercase;letter-spacing:1.5px;font-size:12px}.hero h1{font-size:clamp(38px,6vw,66px);line-height:1.02;letter-spacing:-2.5px;margin:16px 0}.hero p{font-size:18px;line-height:1.65;color:#e1eee6;max-width:580px}.hero-art{min-height:300px;border:1px solid #ffffff24;border-radius:28px;background:linear-gradient(145deg,#ffffff12,#ffffff05);display:grid;place-items:center;position:relative}.route{width:80%;height:145px;border-bottom:8px solid #ffffff70;border-radius:50%;transform:rotate(-9deg);position:absolute;bottom:42px}.parcel{font-size:110px;filter:drop-shadow(0 18px 14px #001c1266);z-index:1}.pin{position:absolute;right:19%;top:18%;font-size:42px;color:var(--lime)}
.wrap{max-width:1160px;margin:auto;padding:66px 22px}.section-head{max-width:700px;margin-bottom:28px}.section-head h2{font-size:clamp(28px,4vw,40px);letter-spacing:-1.2px;color:var(--deep);margin:8px 0}.section-head p{color:var(--muted);line-height:1.6}.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.card{background:white;border:1px solid #e2ebe5;border-radius:22px;padding:25px;box-shadow:0 12px 35px #0b40200a}.card h3{margin:0 0 8px;color:var(--deep);font-size:21px}.card p{color:var(--muted);line-height:1.55}.field{display:grid;gap:7px;margin:14px 0}.field label{font-size:13px;font-weight:750}.field input,.field select{width:100%;padding:14px;border:1px solid #d7e2da;border-radius:11px;background:#fff;font:inherit;outline-color:#70a900}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}.result{margin-top:16px;padding:16px;border-radius:14px;background:#eff8e7;color:var(--deep);font-weight:800}.muted{font-size:12px;color:var(--muted)}.cta{background:#e8f2eb}.cta-in{display:flex;justify-content:space-between;align-items:center;gap:22px}.cta h2{color:var(--deep);font-size:32px;margin:0 0 8px}footer{background:var(--deep);color:#d6e5dc;padding:28px 22px;text-align:center;font-size:13px}
.admin-page{min-height:100vh;display:grid;place-items:center;padding:24px;background:var(--paper)}.admin-box{width:min(430px,100%);background:white;padding:30px;border-radius:22px;box-shadow:0 20px 60px #00351d18}.admin-box h1{color:var(--deep)}.error{color:#b42318;font-size:13px}
@media(max-width:760px){.nav{padding:12px 14px;gap:10px}.brand{font-size:19px}nav{gap:6px}nav a{min-height:38px;padding:8px 10px;font-size:12px}.hero-in{grid-template-columns:1fr;padding-top:58px}.hero-art{min-height:220px}.cards{grid-template-columns:1fr}.cta-in{display:block}.grid2{grid-template-columns:1fr}}
</style></head>
<body>
<header><div class="nav"><a class="brand" href="/" style="text-decoration:none">FRETE <span>STONE</span></a><nav aria-label="Navegação principal"><a href="#inicio">Início</a><a href="#simuladores">Simulações</a><a class="navbtn" href="#cadastro">Cadastro</a></nav></div></header>
<main>
<section class="hero" id="inicio"><div class="hero-in"><div><div class="eyebrow">Sua operação, novas oportunidades</div><h1>Transforme entregas em novas possibilidades.</h1><p>Uma plataforma para organizar suas simulações, acompanhar oportunidades e iniciar seu cadastro no Frete Stone.</p><a class="btn" href="#simuladores">Começar agora</a></div><div class="hero-art" aria-label="Ilustração de pacote e rota de entrega"><div class="route"></div><div class="parcel">📦</div><div class="pin">⌖</div></div></div></section>
<section class="wrap" id="simuladores"><div class="section-head"><div class="eyebrow" style="color:#568500">Planeje sua operação</div><h2>Simuladores</h2><p>Faça estimativas independentes. Os valores de comissão e pagamento só serão exibidos quando as regras comerciais forem oficialmente definidas.</p></div>
<div class="cards">
<article class="card"><h3>Simulador de indicações</h3><p>Estime quantos clientes podem surgir a partir das suas indicações.</p><div class="field"><label for="ind">Número de indicações</label><input id="ind" type="number" min="0" value="20"></div><div class="field"><label for="conv">Taxa de conversão estimada (%)</label><input id="conv" type="number" min="0" max="100" value="25"></div><div class="result" id="indout">Clientes estimados: 5</div><div class="muted">Estimativa ilustrativa, sem promessa de resultado ou comissão.</div></article>
<article class="card"><h3>Simulador de entregas</h3><p>Registre separadamente os volumes recebidos e entregues e os dias trabalhados.</p><div class="grid2"><div class="field"><label for="received">Pacotes recebidos</label><input id="received" type="number" min="0" value="0"></div><div class="field"><label for="delivered">Pacotes entregues</label><input id="delivered" type="number" min="0" value="0"></div></div><div class="field"><label for="days">Dias trabalhados</label><input id="days" type="number" min="0" value="1"></div><div class="result" id="deliveryout">Total movimentado: 0 pacotes · Média diária: 0</div><div class="muted">Valores por pacote ainda não configurados.</div></article>
</div></section>
<section class="wrap cta" id="cadastro"><div class="cta-in"><div><div class="eyebrow" style="color:#568500">Faça parte</div><h2>Comece seu cadastro</h2><p>Deixe seus dados para iniciar seu relacionamento com o Frete Stone.</p></div><a class="btn" href="mailto:contato@ston.eco?subject=Cadastro%20Frete%20Stone">Tenho interesse</a></div></section>
</main><footer>Frete Stone · Plataforma em desenvolvimento</footer>
<script>
const $=id=>document.getElementById(id);
function calcInd(){const n=Math.max(0,Number($('ind').value)||0),c=Math.min(100,Math.max(0,Number($('conv').value)||0));$('indout').textContent='Clientes estimados: '+Math.round(n*c/100)}
function calcDelivery(){const r=Math.max(0,Number($('received').value)||0),d=Math.max(0,Number($('delivered').value)||0),days=Math.max(0,Number($('days').value)||0);$('deliveryout').textContent='Total movimentado: '+(r+d)+' pacotes · Média diária: '+(days?((r+d)/days).toFixed(1):'0')}
['ind','conv'].forEach(id=>$(id).addEventListener('input',calcInd));['received','delivered','days'].forEach(id=>$(id).addEventListener('input',calcDelivery));
</script></body></html>"""

ADMIN = r"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Administração · Frete Stone</title>
<style>body{margin:0;font-family:Arial,sans-serif;background:#f3f7f4;color:#163528}.box{max-width:420px;margin:10vh auto;background:white;padding:30px;border-radius:20px;box-shadow:0 18px 55px #00351d18}h1{color:#043c27}label{display:block;font-weight:bold;font-size:13px;margin:15px 0 7px}input{width:100%;padding:13px;border:1px solid #d7e2da;border-radius:10px;box-sizing:border-box}button{margin-top:20px;width:100%;padding:14px;background:#9eff00;border:0;border-radius:10px;font-weight:bold;cursor:pointer}.err{color:#b42318}</style>
<div class="box"><h1>Frete Stone</h1><p>Acesso administrativo</p>{% if error %}<p class="err">{{ error }}</p>{% endif %}<form method="post"><label>E-mail administrativo</label><input name="email" type="email" autocomplete="username" required><label>Senha</label><input name="password" type="password" autocomplete="current-password" required><button type="submit">Entrar</button></form><p><a href="/">Voltar ao site</a></p></div></html>"""

def admin_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("admin_master"):
            return redirect(url_for("admin"))
        return fn(*args, **kwargs)
    return wrapped

@app.get("/")
def home():
    return render_template_string(PAGE)

@app.get("/api/status")
def status():
    return jsonify({"status": "ok", "app": "Frete Stone"})

@app.route("/admin", methods=["GET", "POST"])
def admin():
    error = None
    if request.method == "POST":
        expected_email = os.getenv("FRETE_STONE_ADMIN_EMAIL", "").strip().lower()
        expected_password = os.getenv("FRETE_STONE_ADMIN_PASSWORD", "")
        if not app.config["SECRET_KEY"] or not expected_email or not expected_password:
            error = "Acesso administrativo ainda não foi configurado com segurança no servidor."
        else:
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            if email == expected_email and password == expected_password:
                session.clear()
                session["admin_master"] = True
                session.permanent = True
                return redirect(url_for("admin_dashboard"))
            error = "E-mail ou senha inválidos."
    return render_template_string(ADMIN, error=error)

@app.get("/admin/painel")
@admin_required
def admin_dashboard():
    return """<!doctype html><html lang='pt-BR'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Painel Frete Stone</title><body style='font-family:Arial;background:#f3f7f4;color:#043c27;padding:40px'><h1>FRETE STONE · ADMIN MASTER</h1><p>Autenticação confirmada. A estrutura de gestão será conectada ao banco de dados na próxima etapa.</p><form method='post' action='/admin/sair'><button>Sair</button></form></body></html>"""

@app.post("/admin/sair")
def admin_logout():
    session.clear()
    return redirect(url_for("admin"))

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "not_found"}), 404
