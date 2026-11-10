from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return """<!doctype html><html lang='pt-BR'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Frete Stone</title><body style='margin:0;min-height:100vh;display:grid;place-items:center;background:#f3f7f4;color:#043c27;font-family:Arial,sans-serif'><main style='text-align:center;padding:32px'><h1>Frete Stone</h1><p>Estrutura inicial publicada. A aplicação está em desenvolvimento.</p></main></body></html>"""

@app.get("/api/status")
def status():
    return jsonify({"status": "ok", "app": "Frete Stone"})
