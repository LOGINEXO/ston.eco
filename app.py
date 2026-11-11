import os
from functools import wraps
import ipaddress
import secrets
from werkzeug.security import generate_password_hash
from datetime import timezone
import psycopg
from psycopg.rows import dict_row
from flask import abort
from flask import Flask, jsonify, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("FRETE_STONE_SECRET_KEY"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=60 * 60 * 12,
    MAX_CONTENT_LENGTH=32 * 1024,
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
.nav{max-width:1160px;margin:auto;padding:15px 22px;display:flex;align-items:center;justify-content:space-between;gap:18px}.brand{display:flex;align-items:center;gap:10px;font-weight:900;letter-spacing:-1px;color:var(--green);font-size:22px;text-decoration:none}.brand-name{white-space:nowrap}.brand-name span{color:#7cbd00}.brand-stone-logo{display:block;width:76px;height:auto;object-fit:contain}
nav{display:flex;gap:9px;align-items:center;flex-wrap:wrap}nav a{display:inline-flex;align-items:center;justify-content:center;min-height:42px;padding:10px 15px;border-radius:12px;background:#e5f2e9;color:var(--green);text-decoration:none;font-size:14px;font-weight:800;border:1px solid #cfe3d5;transition:.18s}nav a:hover{background:#d4eadb;transform:translateY(-1px)}nav a.navbtn{background:var(--lime);color:var(--deep);border-color:var(--lime);padding:11px 19px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;background:var(--lime);color:var(--deep);border:0;border-radius:13px;padding:15px 21px;font-weight:900;text-decoration:none;cursor:pointer;box-shadow:0 8px 22px #9eff0030;transition:transform .18s,box-shadow .18s}.btn:hover{transform:translateY(-2px);box-shadow:0 12px 25px #9eff0045}.btn.secondary{background:#fff;color:var(--green);box-shadow:none;border:1px solid #cfe3d5}
.hero{background:radial-gradient(circle at 82% 20%,#176c45 0,#075334 38%,#043c27 80%);color:#fff;overflow:hidden}.hero-in{max-width:1160px;margin:auto;padding:82px 22px 78px;display:grid;grid-template-columns:1.08fr .92fr;gap:42px;align-items:center}.eyebrow{color:var(--lime);font-weight:850;text-transform:uppercase;letter-spacing:1.5px;font-size:12px}.hero h1{font-size:clamp(42px,6vw,68px);line-height:1.02;letter-spacing:-2.8px;margin:16px 0}.hero h1 span{color:var(--lime)}.hero p{font-size:18px;line-height:1.65;color:#e1eee6;max-width:590px;margin:0 0 23px}.benefits{list-style:none;padding:0;margin:24px 0 28px;display:grid;gap:13px}.benefits li{display:flex;align-items:center;gap:11px;font-weight:700;color:#f4fff7}.check{width:23px;height:23px;flex:0 0 23px;border-radius:50%;background:var(--lime);color:var(--deep);display:grid;place-items:center;font-size:14px;font-weight:950}
.hero-art{min-height:340px;border:1px solid #ffffff2b;border-radius:30px;background:linear-gradient(145deg,#ffffff16,#ffffff06);display:grid;place-items:center;position:relative;overflow:hidden}.stone-logo-panel{width:min(88%,470px);min-height:190px;padding:30px 24px;border:1px solid #ffffff35;border-radius:24px;background:#ffffffed;display:grid;place-items:center;box-shadow:0 22px 50px #001c1233;z-index:1}.hero-stone-logo{display:block;width:100%;max-width:430px;height:auto;object-fit:contain}.art-caption{position:absolute;bottom:22px;left:0;right:0;text-align:center;color:#e2f2e8;font-size:12px;font-weight:750;letter-spacing:1.4px;text-transform:uppercase}

.video-section{background:#fff}.video-frame{max-width:940px;margin:0 auto;aspect-ratio:16/9;border-radius:24px;overflow:hidden;background:#062b1c;box-shadow:0 20px 55px #043c2724;border:1px solid #dce9e0}.video-frame iframe{display:block;width:100%;height:100%;border:0}.video-caption{max-width:760px;margin:18px auto 0;text-align:center;color:var(--muted);line-height:1.6;font-size:14px}
.trust{border-bottom:1px solid #e7eee9;background:#fff}.trust-in{max-width:1160px;margin:auto;padding:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.trust-item{display:flex;align-items:center;gap:10px;color:var(--green);font-weight:800;font-size:14px}.trust-icon{width:34px;height:34px;border-radius:11px;background:#e9f5ed;display:grid;place-items:center;color:var(--green);font-size:17px}
.wrap{max-width:1160px;margin:auto;padding:72px 22px}.section-head{max-width:720px;margin:0 auto 32px;text-align:center}.section-head .eyebrow{color:#568500}.section-head h2{font-size:clamp(30px,4vw,43px);letter-spacing:-1.4px;color:var(--deep);margin:10px 0}.section-head p{color:var(--muted);line-height:1.65;font-size:16px}
.services{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.service{background:#fff;border:1px solid #e1ebe4;border-radius:22px;padding:26px;box-shadow:0 12px 35px #0b40200a}.service .symbol{width:48px;height:48px;border-radius:15px;background:#e9f5ed;color:var(--green);display:grid;place-items:center;font-size:24px;margin-bottom:18px}.service h3{margin:0 0 9px;color:var(--deep);font-size:21px}.service p{color:var(--muted);line-height:1.6;margin:0 0 16px}.service ul{padding-left:18px;margin:0;color:#315542;line-height:1.9;font-size:14px}.service strong{color:var(--green)}

.control{background:#f4f8f5;overflow:hidden}.control-grid{display:grid;grid-template-columns:1fr 1fr;gap:38px;align-items:center}.control-copy h2{font-size:clamp(30px,4vw,43px);line-height:1.08;letter-spacing:-1.4px;color:var(--deep);margin:10px 0 16px}.control-copy p{color:var(--muted);line-height:1.7}.control-visual{padding:14px;border-radius:24px;background:#fff;border:1px solid #e1ebe4;box-shadow:0 16px 40px #0b402012}.control-visual img{display:block;width:100%;height:auto;border-radius:14px}.support{background:var(--deep);color:#fff}.support-grid{display:grid;grid-template-columns:1.1fr .9fr;gap:30px;align-items:center}.support h2{font-size:clamp(29px,4vw,42px);letter-spacing:-1.2px;margin:10px 0}.support p{color:#e0eee5;line-height:1.7;font-size:16px}.support-pill{display:inline-flex;align-items:center;gap:10px;border:1px solid #ffffff38;background:#ffffff12;border-radius:14px;padding:16px 18px;color:#fff;font-weight:800}.support-pill b{color:var(--lime)}.results{background:#f3f7f4}.results-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.metric{background:#fff;border:1px solid #e1ebe4;border-radius:22px;padding:28px;box-shadow:0 12px 35px #0b40200a}.metric-value{font-size:clamp(42px,6vw,60px);font-weight:950;letter-spacing:-2px;color:var(--green);line-height:1}.metric h3{color:var(--deep);font-size:20px;margin:12px 0 8px}.metric p{color:var(--muted);line-height:1.65;margin:0}.results-note{font-size:12px;color:var(--muted);text-align:center;margin-top:18px}
.steps{background:var(--paper)}.steps-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.step{background:#fff;border-radius:18px;padding:24px;border:1px solid #e2ebe5}.step-num{font-size:12px;font-weight:900;color:#568500;letter-spacing:1px}.step h3{color:var(--deep);margin:10px 0 8px}.step p{color:var(--muted);line-height:1.6;margin:0}
.cta{background:linear-gradient(120deg,#e9f5ed,#f4f8f4);border:1px solid #dcebe1;border-radius:26px;padding:34px;display:flex;align-items:center;justify-content:space-between;gap:24px}.cta h2{color:var(--deep);font-size:clamp(26px,4vw,36px);margin:8px 0}.cta p{color:var(--muted);line-height:1.6;margin:0}.cta .eyebrow{color:#568500}
footer{background:var(--deep);color:#d6e5dc;padding:30px 22px;text-align:center;font-size:13px}
.lead-form{max-width:850px;margin:auto;padding:28px;background:#f7faf8;border:1px solid #dfebe3;border-radius:22px}.lead-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}.lead-grid label{display:grid;gap:7px;color:var(--deep);font-size:13px;font-weight:800}.lead-grid input,.lead-grid select,.lead-grid textarea{width:100%;padding:13px;border:1px solid #d3e2d8;border-radius:11px;background:white;font:inherit}.lead-wide{grid-column:1/-1}.lead-consent{display:flex;gap:10px;margin:18px 0;color:var(--muted);font-size:13px}.lead-hp{position:absolute;left:-10000px}.lead-feedback{font-weight:700;min-height:22px}@media(max-width:600px){.lead-grid{grid-template-columns:1fr}.lead-wide{grid-column:auto}.lead-form{padding:18px}}
@media(max-width:800px){.hero-in{grid-template-columns:1fr;padding-top:60px}.hero-art{min-height:250px}.trust-in{grid-template-columns:1fr 1fr}.services{grid-template-columns:1fr}.steps-grid{grid-template-columns:1fr}.control-grid,.support-grid{grid-template-columns:1fr}.results-grid{grid-template-columns:1fr}.cta{display:block}.cta .btn{margin-top:20px}}
@media(max-width:520px){.nav{padding:12px 14px;gap:8px}.brand{font-size:17px;gap:6px}.brand-stone-logo{width:58px}nav{gap:5px}nav a{min-height:37px;padding:8px 10px;font-size:12px}.hero h1{letter-spacing:-1.8px}.hero-in{padding-left:18px;padding-right:18px}.trust-in{padding:18px;gap:12px}.trust-item{font-size:12px}.trust-icon{width:30px;height:30px;flex-basis:30px}.wrap{padding:55px 18px}.cta{padding:25px}}
</style></head>
<body>
<header><div class="nav"><a class="brand" href="/" aria-label="Frete Stone início"><span class="brand-name">FRETE <span>STONE</span></span><img class="brand-stone-logo" src="https://any.stone.com.br/_next/static/media/logo-stone-entrega.0uzjvkd.bt4kx.png" alt="Stone Entrega"></a><nav aria-label="Navegação principal"><a href="#inicio">Início</a><a href="#servicos">Serviços</a><a href="#como-funciona">Como funciona</a><a class="navbtn" href="#cadastro">Cadastro</a></nav></div></header>
<main>
<section class="hero" id="inicio"><div class="hero-in">
<div><div class="eyebrow">Logística para o seu negócio</div><h1>Você vende.<br><span>A Stone entrega.</span></h1><p>Entregas locais e nacionais, com rastreamento em tempo real e integração com as principais plataformas do mercado.</p>
<ul class="benefits"><li><span class="check">✓</span>Ative hoje mesmo, em poucos minutos</li><li><span class="check">✓</span>Sem mensalidade</li><li><span class="check">✓</span>Melhores preços do mercado</li><li><span class="check">✓</span>Atendimento com qualidade Stone</li></ul>
<a class="btn" href="#cadastro">Quero começar <span aria-hidden="true">→</span></a>
</div><div class="hero-art" role="img" aria-label="Logotipo oficial Stone Entrega"><div class="stone-logo-panel"><img class="hero-stone-logo" src="https://any.stone.com.br/_next/static/media/logo-stone-entrega.0uzjvkd.bt4kx.png" alt="Stone Entrega"></div><div class="art-caption">Sua loja em movimento</div></div>
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
<section class="wrap" id="cadastro"><div class="section-head"><div class="eyebrow">Comece hoje</div><h2>Cadastre sua loja</h2><p>Preencha apenas os dados básicos para iniciar seu cadastro.</p></div>
<form id="lead-form" class="lead-form"><div class="lead-grid">
<label class="lead-wide">Nome completo *<input name="name" maxlength="120" autocomplete="name" required></label>
<label>CPF ou CNPJ *<input name="tax_id" maxlength="18" inputmode="numeric" autocomplete="off" placeholder="Digite CPF ou CNPJ" required></label>
<label>E-mail *<input name="email" type="email" maxlength="254" autocomplete="email" required></label>
<label>Senha de acesso<input name="access_password" type="password" minlength="8" maxlength="128" autocomplete="new-password" aria-label="Crie uma senha para acessar o Frete Stone" required></label>
<label>PIN de seis dígitos<input name="six_digit_pin" type="password" inputmode="numeric" pattern="[0-9]{6}" minlength="6" maxlength="6" autocomplete="off" aria-label="Crie um PIN de seis dígitos para o Frete Stone" required></label>
<label class="lead-hp" aria-hidden="true">Não preencher<input name="website" tabindex="-1" autocomplete="off"></label></div>
<label class="lead-consent"><input type="checkbox" name="consent" required> Autorizo o contato da equipe Frete Stone sobre este cadastro.</label>
<button class="btn" type="submit">Enviar cadastro →</button><p id="lead-feedback" role="status"></p></form></section>
</main><footer>Frete Stone · Soluções de entrega para o seu negócio</footer>
<script>(()=>{const f=document.getElementById('lead-form');if(!f)return;f.addEventListener('submit',async e=>{e.preventDefault();const b=f.querySelector('button'),m=document.getElementById('lead-feedback');b.disabled=true;b.textContent='Enviando...';const d=Object.fromEntries(new FormData(f).entries());d.consent=f.querySelector('[name=consent]').checked;try{const r=await fetch('/api/cadastro',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const x=await r.json();if(!r.ok)throw Error(x.error||'Falha no envio');f.reset();m.textContent='Cadastro enviado com sucesso! Nossa equipe entrará em contato.';}catch(x){m.textContent=x.message;}finally{b.disabled=false;b.textContent='Enviar cadastro →';}});})();</script></body></html>"""

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

ADMIN_DASHBOARD = r"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Painel Frete Stone</title><style>
*{box-sizing:border-box}body{margin:0;font-family:Arial;background:#f2f6f3;color:#173b2b}.top{background:#043c27;color:white;padding:20px 4%;display:flex;justify-content:space-between}.top button,.btn{background:#9eff00;color:#043c27;border:0;border-radius:9px;padding:11px 16px;font-weight:bold;cursor:pointer}.shell{max-width:1200px;margin:25px auto;padding:0 16px}.tabs{display:flex;gap:10px;margin-bottom:15px}.tabs button{padding:12px 18px;border:1px solid #d5e4da;border-radius:10px;background:white;color:#075334;font-weight:bold}.tabs .active{background:#075334;color:white}.panel{background:white;border:1px solid #e0eae3;border-radius:15px;padding:18px}.toolbar{display:flex;gap:9px;margin-bottom:14px;flex-wrap:wrap}.toolbar input{flex:1;min-width:180px;padding:11px;border:1px solid #d5e4da;border-radius:8px}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;min-width:700px}th,td{text-align:left;padding:11px;border-bottom:1px solid #e8eee9;font-size:13px}tr[data-id]{cursor:pointer}tr[data-id]:hover{background:#f2f9f4}.active{color:#087443}.blocked{color:#b42318}.modal{position:fixed;inset:0;background:#001c1277;display:none;align-items:center;justify-content:center;padding:15px}.modal.open{display:flex}.dialog{width:min(700px,100%);max-height:90vh;overflow:auto;background:white;border-radius:15px;padding:22px}.close{float:right}.fields{display:grid;grid-template-columns:1fr 1fr;gap:12px}.fields label{display:grid;gap:5px;font-size:13px;font-weight:bold}.fields input,.fields textarea,.fields select{padding:10px;border:1px solid #d5e4da;border-radius:8px}.wide{grid-column:1/-1}.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px}.actions button{padding:10px;border:0;border-radius:8px;cursor:pointer;font-weight:bold}.danger{background:#fee4e2;color:#b42318}.notice{color:#b42318}@media(max-width:600px){.fields{grid-template-columns:1fr}.wide{grid-column:auto}}
</style></head><body><header class="top"><h2>FRETE STONE · PAINEL ADMINISTRATIVO</h2><form method="post" action="/admin/sair"><button>Sair</button></form></header>
<main class="shell"><div class="tabs"><button class="active" data-tab="leads">Cadastros</button><button data-tab="ips">IPs bloqueados</button></div>
<section class="panel" id="leads-panel"><div class="toolbar"><input id="search" placeholder="Buscar nome, CPF/CNPJ ou e-mail"><button class="btn" id="refresh">Atualizar</button></div><div class="table-wrap"><table><thead><tr><th>Data</th><th>Nome</th><th>CPF/CNPJ</th><th>E-mail</th><th>Status</th></tr></thead><tbody id="lead-rows"></tbody></table></div></section>
<section class="panel" id="ips-panel" hidden><div class="toolbar"><input id="ip-address" placeholder="Endereço IP"><input id="ip-reason" placeholder="Motivo do bloqueio"><button class="btn" id="block-ip">Bloquear IP</button></div><div class="table-wrap"><table><thead><tr><th>IP</th><th>Motivo</th><th>Data</th><th></th></tr></thead><tbody id="ip-rows"></tbody></table></div></section></main>
<div class="modal" id="modal"><div class="dialog"><button class="close" id="close">Fechar ×</button><h2>Detalhes do cadastro</h2><p id="meta"></p><form id="edit"><input type="hidden" name="id"><div class="fields">
<label>Nome completo<input name="name" required></label><label>CPF ou CNPJ<input name="tax_id" required></label><label class="wide">E-mail<input name="email" type="email" required></label><label>Status<select name="status"><option value="active">Ativo</option><option value="blocked">Bloqueado</option></select></label></div><p id="credential-status" class="notice">As credenciais são armazenadas protegidas e não são exibidas.</p>
<div class="actions"><button class="btn" type="submit">Salvar alterações</button><button type="button" id="toggle">Bloquear / desbloquear</button><button type="button" class="danger" id="delete-lead">Excluir cadastro</button><button type="button" class="danger" id="block-lead-ip">Bloquear IP deste cadastro</button></div><p id="notice" class="notice"></p></form></div></div>
<script>
const csrf={{ csrf_token|tojson }};
async function api(url,opt={}){opt.headers=Object.assign({},opt.headers||{}, {'X-CSRF-Token':csrf});const r=await fetch(url,opt);const j=await r.json();if(!r.ok)throw Error(j.error||'Falha');return j}
let rows=[],selected=null;
const esc=v=>String(v==null?'':v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
async function load(){try{rows=(await api('/api/admin/cadastros')).items;draw()}catch(e){alert(e.message)}}
function draw(){const q=document.getElementById('search').value.toLowerCase();const a=rows.filter(x=>(x.name+' '+x.tax_id+' '+x.email).toLowerCase().includes(q));document.getElementById('lead-rows').innerHTML=a.map(x=>'<tr data-id="'+x.id+'"><td>'+esc(x.created_at)+'</td><td>'+esc(x.name)+'</td><td>'+esc(x.tax_id)+'</td><td>'+esc(x.email)+'</td><td class="'+x.status+'">'+(x.status==='blocked'?'Bloqueado':'Ativo')+'</td></tr>').join('');document.querySelectorAll('#lead-rows tr').forEach(t=>t.onclick=()=>openLead(Number(t.dataset.id)))}
async function openLead(id){try{selected=await api('/api/admin/cadastros/'+id);const f=document.getElementById('edit');Object.keys(selected).forEach(k=>{if(f.elements[k])f.elements[k].value=selected[k]||''});document.getElementById('meta').textContent='Cadastro #'+id+' · IP '+selected.ip+' · '+selected.created_at;document.getElementById('credential-status').textContent='Senha de acesso: '+(selected.access_password_set?'cadastrada':'não cadastrada')+' · PIN de seis dígitos: '+(selected.six_digit_pin_set?'cadastrado':'não cadastrado')+'. Os valores não são exibidos por segurança.';document.getElementById('modal').classList.add('open')}catch(e){alert(e.message)}}
document.getElementById('edit').onsubmit=async e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.target).entries());try{await api('/api/admin/cadastros/'+d.id,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});document.getElementById('notice').textContent='Cadastro atualizado';await load()}catch(x){document.getElementById('notice').textContent=x.message}};
document.getElementById('toggle').onclick=async()=>{if(!selected)return;try{await api('/api/admin/cadastros/'+selected.id+'/status',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({status:selected.status==='blocked'?'active':'blocked'})});document.getElementById('modal').classList.remove('open');await load()}catch(e){alert(e.message)}};
document.getElementById('delete-lead').onclick=async()=>{if(!selected)return;const ok=confirm('Excluir permanentemente o cadastro de '+selected.name+'? Esta ação não pode ser desfeita.');if(!ok)return;try{await api('/api/admin/cadastros/'+selected.id,{method:'DELETE'});selected=null;document.getElementById('modal').classList.remove('open');await load()}catch(e){alert(e.message)}};
document.getElementById('block-lead-ip').onclick=async()=>{if(!selected)return;const reason=prompt('Motivo do bloqueio','Spam ou envios repetidos');if(reason===null)return;try{await api('/api/admin/ips',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ip:selected.ip,reason})});alert('IP bloqueado');await loadIps()}catch(e){alert(e.message)}};
async function loadIps(){const d=await api('/api/admin/ips');document.getElementById('ip-rows').innerHTML=d.items.map(x=>'<tr><td>'+esc(x.ip)+'</td><td>'+esc(x.reason)+'</td><td>'+esc(x.created_at)+'</td><td><button data-ip="'+esc(x.ip)+'">Desbloquear</button></td></tr>').join('');document.querySelectorAll('#ip-rows button').forEach(b=>b.onclick=async()=>{await api('/api/admin/ips/'+encodeURIComponent(b.dataset.ip),{method:'DELETE'});loadIps()})}
document.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));document.getElementById('leads-panel').hidden=b.dataset.tab!=='leads';document.getElementById('ips-panel').hidden=b.dataset.tab!=='ips';if(b.dataset.tab==='ips')loadIps()});
document.getElementById('refresh').onclick=load;document.getElementById('search').oninput=draw;document.getElementById('close').onclick=()=>document.getElementById('modal').classList.remove('open');
document.getElementById('block-ip').onclick=async()=>{try{await api('/api/admin/ips',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({ip:document.getElementById('ip-address').value,reason:document.getElementById('ip-reason').value})});loadIps()}catch(e){alert(e.message)}};
load();
</script></body></html>"""

def get_db():
    url=os.getenv("DATABASE_URL","").strip()
    if not url: raise RuntimeError("DATABASE_URL não configurada")
    if url.startswith("postgres://"): url="postgresql://"+url[11:]
    return psycopg.connect(url,row_factory=dict_row,connect_timeout=5)

def init_db():
    with get_db() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS frete_leads(id BIGSERIAL PRIMARY KEY,name VARCHAR(120) NOT NULL,store VARCHAR(160),city VARCHAR(100),state CHAR(2),whatsapp VARCHAR(20),business_type VARCHAR(100),daily_orders VARCHAR(40),message VARCHAR(1000),tax_id VARCHAR(18),email VARCHAR(254),ip INET NOT NULL,status VARCHAR(12) NOT NULL DEFAULT 'active' CHECK(status IN ('active','blocked')),created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""")
        c.execute("ALTER TABLE frete_leads ADD COLUMN IF NOT EXISTS tax_id VARCHAR(18)")
        c.execute("ALTER TABLE frete_leads ADD COLUMN IF NOT EXISTS email VARCHAR(254)")
        c.execute("ALTER TABLE frete_leads ADD COLUMN IF NOT EXISTS access_password_hash TEXT")
        c.execute("ALTER TABLE frete_leads ADD COLUMN IF NOT EXISTS six_digit_pin_hash TEXT")
        c.execute("ALTER TABLE frete_leads ALTER COLUMN store DROP NOT NULL")
        c.execute("ALTER TABLE frete_leads ALTER COLUMN city DROP NOT NULL")
        c.execute("ALTER TABLE frete_leads ALTER COLUMN state DROP NOT NULL")
        c.execute("ALTER TABLE frete_leads ALTER COLUMN whatsapp DROP NOT NULL")
        c.execute("ALTER TABLE frete_leads ALTER COLUMN business_type DROP NOT NULL")
        c.execute("CREATE INDEX IF NOT EXISTS idx_frete_leads_ip_created ON frete_leads(ip,created_at DESC)")
        c.execute("""CREATE TABLE IF NOT EXISTS frete_ip_blocks(ip INET PRIMARY KEY,reason VARCHAR(250) NOT NULL,created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""")

def get_client_ip():
    raw=request.headers.get("X-Forwarded-For",request.remote_addr or "").split(",")[0].strip()
    return str(ipaddress.ip_address(raw))

def csrf_check():
    if not secrets.compare_digest(request.headers.get("X-CSRF-Token",""),session.get("csrf_token","")): abort(403)

@app.post("/api/cadastro")
def create_lead():
    d=request.get_json(silent=True) or {}
    if d.get("website"): return jsonify({"error":"Não foi possível validar o cadastro."}),400
    if d.get("consent") is not True: return jsonify({"error":"Autorize o contato para enviar o cadastro."}),400
    keys=("name","tax_id","email")
    v={k:str(d.get(k,"")).strip() for k in keys}
    if not all(v.values()): return jsonify({"error":"Preencha todos os campos obrigatórios."}),400
    tax_digits="".join(ch for ch in v["tax_id"] if ch.isdigit())
    if len(tax_digits) not in (11,14): return jsonify({"error":"Informe um CPF ou CNPJ válido."}),400
    access_password=str(d.get("access_password",""))
    six_digit_pin=str(d.get("six_digit_pin",""))
    if len(v["name"])>120 or len(v["email"])>254 or len(access_password)<8 or len(access_password)>128: return jsonify({"error":"Confira os campos. A senha de acesso deve ter entre 8 e 128 caracteres."}),400
    if len(six_digit_pin)!=6 or not six_digit_pin.isdigit(): return jsonify({"error":"O PIN deve conter exatamente seis números."}),400
    if "@" not in v["email"] or "." not in v["email"].split("@")[-1]: return jsonify({"error":"E-mail inválido."}),400
    v["tax_id"]=tax_digits
    try:
        # Garante a migração do esquema também no primeiro cadastro público.
        init_db()
        ip=get_client_ip()
        with get_db() as c:
            if c.execute("SELECT 1 FROM frete_ip_blocks WHERE ip=%s",(ip,)).fetchone(): return jsonify({"error":"Acesso temporariamente bloqueado."}),429
            count=c.execute("SELECT COUNT(*) AS n FROM frete_leads WHERE ip=%s AND created_at>NOW()-INTERVAL '10 minutes'",(ip,)).fetchone()["n"]
            if count>=3: return jsonify({"error":"Limite de envios atingido. Aguarde alguns minutos."}),429
            c.execute("INSERT INTO frete_leads(name,tax_id,email,ip,access_password_hash,six_digit_pin_hash) VALUES(%s,%s,%s,%s,%s,%s)",(v["name"],v["tax_id"],v["email"],ip,generate_password_hash(access_password),generate_password_hash(six_digit_pin)))
        return jsonify({"ok":True}),201
    except RuntimeError: return jsonify({"error":"Cadastro temporariamente indisponível. Tente novamente mais tarde."}),503
    except ValueError: return jsonify({"error":"Origem do envio inválida."}),400
    except Exception:
        app.logger.exception("Erro ao registrar cadastro")
        return jsonify({"error":"Erro interno ao receber cadastro."}),500

@app.get("/api/admin/cadastros")
@admin_required
def list_leads():
    with get_db() as c: rows=c.execute("SELECT id,name,tax_id,email,status,created_at FROM frete_leads ORDER BY created_at DESC LIMIT 1000").fetchall()
    return jsonify({"items":[{**dict(x),"created_at":x["created_at"].strftime("%d/%m/%Y %H:%M UTC")} for x in rows]})

@app.get("/api/admin/cadastros/<int:lead_id>")
@admin_required
def detail_lead(lead_id):
    with get_db() as c: x=c.execute("SELECT *,ip::text AS ip FROM frete_leads WHERE id=%s",(lead_id,)).fetchone()
    if not x:return jsonify({"error":"Cadastro não encontrado"}),404
    x=dict(x);x["created_at"]=x["created_at"].strftime("%d/%m/%Y %H:%M UTC")
    x["access_password_set"]=bool(x.pop("access_password_hash",None))
    x["six_digit_pin_set"]=bool(x.pop("six_digit_pin_hash",None))
    return jsonify(x)

@app.patch("/api/admin/cadastros/<int:lead_id>")
@admin_required
def edit_lead(lead_id):
    csrf_check();d=request.get_json(silent=True) or {};ks=("name","tax_id","email","status");v={k:str(d.get(k,"")).strip() for k in ks}
    tax_digits="".join(ch for ch in v["tax_id"] if ch.isdigit())
    if v["status"] not in ("active","blocked") or not v["name"] or len(v["name"])>120 or len(tax_digits) not in (11,14) or len(v["email"])>254 or "@" not in v["email"] or "." not in v["email"].split("@")[-1]:return jsonify({"error":"Preencha todos os campos corretamente."}),400
    with get_db() as c:
        q=c.execute("UPDATE frete_leads SET name=%s,tax_id=%s,email=%s,status=%s,updated_at=NOW() WHERE id=%s",(v["name"][:120],tax_digits,v["email"][:254],v["status"],lead_id))
    if not q.rowcount:return jsonify({"error":"Cadastro não encontrado"}),404
    return jsonify({"ok":True})

@app.delete("/api/admin/cadastros/<int:lead_id>")
@admin_required
def delete_lead(lead_id):
    csrf_check()
    with get_db() as c:
        q=c.execute("DELETE FROM frete_leads WHERE id=%s",(lead_id,))
    if not q.rowcount:return jsonify({"error":"Cadastro não encontrado"}),404
    return jsonify({"ok":True})


@app.post("/api/admin/cadastros/<int:lead_id>/status")
@admin_required
def lead_status(lead_id):
    csrf_check();d=request.get_json(silent=True) or {};st=d.get("status")
    if st not in ("active","blocked"):return jsonify({"error":"Status inválido"}),400
    with get_db() as c:q=c.execute("UPDATE frete_leads SET status=%s,updated_at=NOW() WHERE id=%s",(st,lead_id))
    if not q.rowcount:return jsonify({"error":"Cadastro não encontrado"}),404
    return jsonify({"ok":True})

@app.get("/api/admin/ips")
@admin_required
def ips_list():
    with get_db() as c:xs=c.execute("SELECT ip::text AS ip,reason,created_at FROM frete_ip_blocks ORDER BY created_at DESC").fetchall()
    return jsonify({"items":[{**dict(x),"created_at":x["created_at"].strftime("%d/%m/%Y %H:%M UTC")} for x in xs]})

@app.post("/api/admin/ips")
@admin_required
def ips_block():
    csrf_check();d=request.get_json(silent=True) or {}
    try:ip=str(ipaddress.ip_address(str(d.get("ip","")).strip()))
    except ValueError:return jsonify({"error":"IP inválido"}),400
    reason=str(d.get("reason","Bloqueio administrativo")).strip()[:250] or "Bloqueio administrativo"
    with get_db() as c:c.execute("INSERT INTO frete_ip_blocks(ip,reason) VALUES(%s,%s) ON CONFLICT(ip) DO UPDATE SET reason=EXCLUDED.reason,created_at=NOW()",(ip,reason))
    return jsonify({"ok":True})

@app.delete("/api/admin/ips/<path:ip_value>")
@admin_required
def ips_unblock(ip_value):
    csrf_check()
    try:ip=str(ipaddress.ip_address(ip_value))
    except ValueError:return jsonify({"error":"IP inválido"}),400
    with get_db() as c:c.execute("DELETE FROM frete_ip_blocks WHERE ip=%s",(ip,))
    return jsonify({"ok":True})

@app.get("/admin/painel")
@admin_required
def admin_dashboard():
    if not os.getenv("DATABASE_URL"): return "Banco Frete Stone não configurado. Configure DATABASE_URL no Render.",503
    if "csrf_token" not in session:session["csrf_token"]=secrets.token_urlsafe(32)
    try:init_db()
    except Exception:
        app.logger.exception("Falha ao inicializar banco Frete Stone")
        return "Não foi possível conectar ao banco de dados Frete Stone.",503
    return render_template_string(ADMIN_DASHBOARD,csrf_token=session["csrf_token"])


@app.post("/admin/sair")
def admin_logout():
    session.clear()
    return redirect(url_for("admin"))

@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "not_found"}), 404
