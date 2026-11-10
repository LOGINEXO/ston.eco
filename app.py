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
<meta name="description" content="Entregas locais e nacionais para sua loja, com rastreamento em tempo real e integração com plataformas de mercado.">
<title>Frete Stone | Você vende. A Stone entrega.</title>
<style>
:root{--green:#075334;--deep:#043c27;--lime:#9eff00;--paper:#f3f7f4;--ink:#163528;--muted:#64756b;--white:#fff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#fff;color:var(--ink);font-family:Inter,system-ui,-apple-system,Segoe UI,Arial,sans-serif}
header{position:sticky;top:0;z-index:5;background:#fffffff2;border-bottom:1px solid #e2ebe5;backdrop-filter:blur(12px)}
.nav{max-width:1160px;margin:auto;padding:15px 22px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{font-weight:900;letter-spacing:-1px;color:var(--green);font-size:22px;text-decoration:none}.brand span{color:#7cbd00}
nav{display:flex;gap:9px;align-items:center;flex-wrap:wrap}nav a{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:10px 15px;border-radius:12px;background:#e5f2e9;color:var(--green);text-decoration:none;font-size:14px;font-weight:800;border:1px solid #cfe3d5;transition:.18s}nav a:hover{background:#d4eadb;transform:translateY(-1px)}nav a.navbtn{background:var(--lime);color:var(--deep);border-color:var(--lime);padding:11px 19px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;background:var(--lime);color:var(--deep);border:0;border-radius:13px;padding:15px 21px;font-weight:900;text-decoration:none;cursor:pointer;box-shadow:0 8px 22px #9eff0030;transition:transform .18s,box-shadow .18s}.btn:hover{transform:translateY(-2px);box-shadow:0 12px 25px #9eff0045}.btn.secondary{background:#fff;color:var(--green);box-shadow:none;border:1px solid #cfe3d5}
.hero{background:radial-gradient(circle at 82% 20%,#176c45 0,#075334 38%,#043c27 80%);color:#fff;overflow:hidden}.hero-in{max-width:1160px;margin:auto;padding:82px 22px 78px;display:grid;grid-template-columns:1.08fr .92fr;gap:42px;align-items:center}.eyebrow{color:var(--lime);font-weight:850;text-transform:uppercase;letter-spacing:1.5px;font-size:12px}.hero h1{font-size:clamp(42px,6vw,68px);line-height:1.02;letter-spacing:-2.8px;margin:16px 0}.hero h1 span{color:var(--lime)}.hero p{font-size:18px;line-height:1.65;color:#e1eee6;max-width:590px;margin:0 0 23px}.benefits{list-style:none;padding:0;margin:24px 0 28px;display:grid;gap:13px}.benefits li{display:flex;align-items:center;gap:11px;font-weight:700;color:#f4fff7}.check{width:23px;height:23px;flex:0 0 23px;border-radius:50%;background:var(--lime);color:var(--deep);display:grid;place-items:center;font-size:14px;font-weight:950}
.hero-art{min-height:340px;border:1px solid #ffffff2b;border-radius:30px;background:linear-gradient(145deg,#ffffff16,#ffffff06);display:grid;place-items:center;position:relative;overflow:hidden}.hero-art:before{content:"";position:absolute;width:72%;height:120px;border-bottom:8px solid #ffffff70;border-radius:50%;transform:rotate(-10deg);bottom:42px}.parcel{font-size:122px;filter:drop-shadow(0 18px 14px #001c1266);z-index:1}.pin{position:absolute;right:18%;top:16%;font-size:44px;color:var(--lime)}.art-caption{position:absolute;bottom:22px;left:0;right:0;text-align:center;color:#e2f2e8;font-size:12px;font-weight:750;letter-spacing:1.4px;text-transform:uppercase}

.video-section{background:#fff}.video-frame{max-width:940px;margin:0 auto;aspect-ratio:16/9;border-radius:24px;overflow:hidden;background:#062b1c;box-shadow:0 20px 55px #043c2724;border:1px solid #dce9e0}.video-frame iframe{display:block;width:100%;height:100%;border:0}.video-caption{max-width:760px;margin:18px auto 0;text-align:center;color:var(--muted);line-height:1.6;font-size:14px}
.trust{border-bottom:1px solid #e7eee9;background:#fff}.trust-in{max-width:1160px;margin:auto;padding:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.trust-item{display:flex;align-items:center;gap:10px;color:var(--green);font-weight:800;font-size:14px}.trust-icon{width:34px;height:34px;border-radius:11px;background:#e9f5ed;display:grid;place-items:center;color:var(--green);font-size:17px}
.wrap{max-width:1160px;margin:auto;padding:72px 22px}.section-head{max-width:720px;margin:0 auto 32px;text-align:center}.section-head .eyebrow{color:#568500}.section-head h2{font-size:clamp(30px,4vw,43px);letter-spacing:-1.4px;color:var(--deep);margin:10px 0}.section-head p{color:var(--muted);line-height:1.65;font-size:16px}
.services{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.service{background:#fff;border:1px solid #e1ebe4;border-radius:22px;padding:26px;box-shadow:0 12px 35px #0b40200a}.service .symbol{width:48px;height:48px;border-radius:15px;background:#e9f5ed;color:var(--green);display:grid;place-items:center;font-size:24px;margin-bottom:18px}.service h3{margin:0 0 9px;color:var(--deep);font-size:21px}.service p{color:var(--muted);line-height:1.6;margin:0 0 16px}.service ul{padding-left:18px;margin:0;color:#315542;line-height:1.9;font-size:14px}.service strong{color:var(--green)}

.control{background:#f4f8f5;overflow:hidden}.control-grid{display:grid;grid-template-columns:1fr 1fr;gap:38px;align-items:center}.control-copy h2{font-size:clamp(30px,4vw,43px);line-height:1.08;letter-spacing:-1.4px;color:var(--deep);margin:10px 0 16px}.control-copy p{color:var(--muted);line-height:1.7}.control-visual{padding:14px;border-radius:24px;background:#fff;border:1px solid #e1ebe4;box-shadow:0 16px 40px #0b402012}.control-visual img{display:block;width:100%;height:auto;border-radius:14px}.support{background:var(--deep);color:#fff}.support-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:30px;align-items:center}.support h2{font-size:clamp(29px,4vw,42px);letter-spacing:-1.2px;margin:10px 0}.support p{color:#e0eee5;line-height:1.7;font-size:16px}.support-pill{display:inline-flex;align-items:center;gap:10px;border:1px solid #ffffff38;background:#ffffff12;border-radius:14px;padding:16px 18px;color:#fff;font-weight:800}.support-pill b{color:var(--lime)}.results{background:#f3f7f4}.results-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.metric{background:#fff;border:1px solid #e1ebe4;border-radius:22px;padding:28px;box-shadow:0 12px 35px #0b40200a}.metric-value{font-size:clamp(42px,6vw,60px);font-weight:950;letter-spacing:-2px;color:var(--green);line-height:1}.metric h3{color:var(--deep);font-size:20px;margin:12px 0 8px}.metric p{color:var(--muted);line-height:1.65;margin:0}.results-note{font-size:12px;color:var(--muted);text-align:center;margin-top:18px}
.steps{background:var(--paper)}.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.step{background:#fff;border-radius:18px;padding:24px;border:1px solid #e2ebe5}.step-num{font-size:12px;font-weight:900;color:#568500;letter-spacing:1px}.step h3{color:var(--deep);margin:10px 0 8px}.step p{color:var(--muted);line-height:1.6;margin:0}
.cta{background:linear-gradient(120deg,#e9f5ed,#f4f8f4);border:1px solid #dcebe1;border-radius:26px;padding:34px;display:flex;align-items:center;justify-content:space-between;gap:24px}.cta h2{color:var(--deep);font-size:clamp(26px,4vw,36px);margin:8px 0}.cta p{color:var(--muted);line-height:1.6;margin:0}.cta .eyebrow{color:#568500}
footer{background:var(--deep);color:#d6e5dc;padding:30px 22px;text-align:center;font-size:13px}
@media(max-width:800px){.hero-in{grid-template-columns:1fr;padding-top:60px}.hero-art{min-height:250px}.trust-in{grid-template-columns:1fr 1fr}.services{grid-template-columns:1fr}.steps-grid{grid-template-columns:1fr}.control-grid,.support-grid{grid-template-columns:1fr}.results-grid{grid-template-columns:1fr}.cta{display:block}.cta .btn{margin-top:20px}}
@media(max-width:520px){.nav{padding:12px 14px;gap:8px}.brand{font-size:19px}nav{gap:5px}nav a{min-height:37px;padding:8px 10px;font-size:12px}.hero h1{letter-spacing:-1.8px}.hero-in{padding-left:18px;padding-right:18px}.trust-in{padding:18px;gap:12px}.trust-item{font-size:12px}.trust-icon{width:30px;height:30px;flex-basis:30px}.wrap{padding:55px 18px}.cta{padding:25px}}
</style></head>
<body>
<header><div class="nav"><a class="brand" href="/" aria-label="Frete Stone início">FRETE <span>STONE</span></a><nav aria-label="Navegação principal"><a href="#inicio">Início</a><a href="#servicos">Serviços</a><a href="#como-funciona">Como funciona</a><a class="navbtn" href="#cadastro">Cadastro</a></nav></div></header>
<main>
<section class="hero" id="inicio"><div class="hero-in">
<div><div class="eyebrow">Logística para o seu negócio</div><h1>Você vende.<br><span>A Stone entrega.</span></h1><p>Entregas locais e nacionais, com rastreamento em tempo real e integração com as principais plataformas do mercado.</p>
<ul class="benefits"><li><span class="check">✓</span>Ative hoje mesmo, em poucos minutos</li><li><span class="check">✓</span>Sem mensalidade</li><li><span class="check">✓</span>Melhores preços do mercado</li><li><span class="check">✓</span>Atendimento com qualidade Stone</li></ul>
<a class="btn" href="#cadastro">Quero começar <span aria-hidden="true">→</span></a>
</div><div class="hero-art" role="img" aria-label="Pacote pronto para seguir em uma rota de entrega"><div class="parcel">📦</div><div class="pin">⌖</div><div class="art-caption">Sua loja em movimento</div></div>
</div></section>

<section class="video-section wrap" id="demonstracao"><div class="section-head"><div class="eyebrow">Conheça a plataforma</div><h2>Veja como a Stone simplifica suas entregas.</h2><p>Uma demonstração da experiência de gestão e acompanhamento dos seus envios.</p></div><div class="video-frame"><iframe src="https://player.mux.com/my8KNRY8IRLbuZxqV4beiUmohkOFLlZRBaKi5MMM028U?metadata-video-title=Frete%20Stone%20-%20Demonstra%C3%A7%C3%A3o&amp;video-title=Frete%20Stone" title="Demonstração da plataforma Stone Entrega" loading="lazy" allow="accelerometer; gyroscope; autoplay; encrypted-media; picture-in-picture;" allowfullscreen></iframe></div><p class="video-caption">Conheça os recursos da plataforma para organizar e acompanhar as entregas do seu negócio.</p></section>
<section class="trust"><div class="trust-in"><div class="trust-item"><span class="trust-icon">⌖</span>Entregas locais</div><div class="trust-item"><span class="trust-icon">↗</span>Envios nacionais</div><div class="trust-item"><span class="trust-icon">◎</span>Rastreamento em tempo real</div><div class="trust-item"><span class="trust-icon">⇄</span>Integrações de mercado</div></div></section>
<section class="wrap" id="servicos"><div class="section-head"><div class="eyebrow">Soluções de entrega</div><h2>Escolha a entrega ideal para cada pedido</h2><p>Atenda seus clientes na sua região ou envie produtos para qualquer lugar do Brasil.</p></div>
<div class="services">
<article class="service"><div class="symbol">⚡</div><h3>Entrega Turbo</h3><p>Agilidade para pedidos locais, com motorista dedicado que coleta na sua loja e leva diretamente ao cliente.</p><ul><li>Prazo de até <strong>2 horas</strong></li><li>Alcance de até <strong>25 km</strong></li><li>Sem volume mínimo</li></ul></article>
<article class="service"><div class="symbol">☀</div><h3>No mesmo dia</h3><p>Uma coleta consolidada no seu endereço para lojas com maior volume de pedidos.</p><ul><li>Entrega no mesmo dia para pedidos até 13h</li><li>Alcance de até <strong>40 km</strong></li><li>A partir de <strong>10 pedidos por dia</strong></li></ul></article>
<article class="service"><div class="symbol">✈</div><h3>Entrega nacional</h3><p>Envie para todo o Brasil com opções expressas ou econômicas e acompanhe seus pedidos.</p><ul><li>Cobertura em todo o território nacional</li><li>Modalidades expressa e econômica</li><li>Sem volume mínimo para postagem</li></ul></article>
</div></section>

<section class="control" id="painel"><div class="wrap"><div class="control-grid">
<div class="control-copy"><div class="eyebrow" style="color:#568500">Torre de controle</div><h2>Sua operação inteira, em um só painel.</h2><p>Acompanhe seus pedidos ponta a ponta, consulte status e prazos estimados, visualize informações da entrega e mantenha a gestão da sua loja organizada em uma única plataforma.</p><p>Tenha mais visibilidade sobre os envios locais e nacionais, com recursos para acompanhar a operação e administrar usuários e contas.</p></div>
<div class="control-visual"><img src="https://any.stone.com.br/_next/static/media/multi_contas.0~ev6-np0t-2t.gif" width="100%" height="100%" alt="Demonstração de gestão de usuários e contas na plataforma Stone Entrega" loading="lazy"></div>
</div></div></section>
<section class="support"><div class="wrap"><div class="support-grid"><div><div class="eyebrow">Atendimento de qualidade Stone</div><h2>Envios locais e nacionais, com suporte quando você precisar.</h2><p>Se alguma etapa precisar da gente, conte com atendimento direto pela plataforma ou pelo WhatsApp. A primeira resposta chega em menos de 1 minuto.</p></div><div class="support-pill"><span aria-hidden="true">◷</span><span>Primeira resposta em <b>menos de 1 minuto</b></span></div></div></div></section>
<section class="results"><div class="wrap"><div class="section-head"><div class="eyebrow">Resultados para sua loja</div><h2>Mais vendas, menos custo com frete.</h2><p>Entregar mais rápido, em mais lugares e pelo melhor preço aparece direto no resultado da sua loja.</p></div>
<div class="results-grid"><article class="metric"><div class="metric-value">−28%</div><h3>nos custos de frete</h3><p>O tamanho da Stone e o acesso a mais de 10 transportadoras ajudam a encontrar preços competitivos para cada envio.</p></article><article class="metric"><div class="metric-value">+24%</div><h3>na taxa de conversão</h3><p>Entregando em mais lugares, mais rápido e mais barato, mais clientes podem concluir a compra no checkout.</p></article></div><div class="results-note">Indicadores de resultado divulgados pela Stone Entrega.</div>
</div></section>
<section class="steps" id="como-funciona"><div class="wrap"><div class="section-head"><div class="eyebrow">Simples para sua rotina</div><h2>Mais facilidade do pedido à entrega</h2><p>Organize os envios da sua loja com uma operação conectada e acompanhamento em cada etapa.</p></div><div class="steps-grid"><article class="step"><div class="step-num">01 · PREPARE</div><h3>Venda e prepare o pedido</h3><p>Continue vendendo pelos seus canais e deixe o pacote pronto para envio.</p></article><article class="step"><div class="step-num">02 · ENVIE</div><h3>Escolha a modalidade</h3><p>Conte com opções locais e nacionais para atender cada destino.</p></article><article class="step"><div class="step-num">03 · ACOMPANHE</div><h3>Rastreie a entrega</h3><p>Acompanhe o andamento do pedido e mantenha seu cliente informado.</p></article></div></div></section>
<section class="wrap" id="cadastro"><div class="cta"><div><div class="eyebrow">Comece hoje</div><h2>Sua loja pronta para entregar mais.</h2><p>Entre em contato para conhecer as opções de entrega para o seu negócio.</p></div><a class="btn" href="mailto:contato@ston.eco?subject=Quero%20conhecer%20o%20Frete%20Stone">Tenho interesse <span aria-hidden="true">→</span></a></div></section>
</main><footer>Frete Stone · Soluções de entrega para o seu negócio</footer>
</body></html>"""

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
