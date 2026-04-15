from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
PCAP_LINK = os.environ.get("PCAP_LINK", "https://drive.google.com/drive/folders/1p6JdkFsSEZYmtl94Ax8XYzHlTTWwN3M3")
KEYLOG_LINK = os.environ.get("KEYLOG_LINK", "https://drive.google.com/drive/folders/1p6JdkFsSEZYmtl94Ax8XYzHlTTWwN3M3")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TLS Challenge - Forensics</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Exo 2', sans-serif;
            background: #050f0f;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
            background-image: radial-gradient(ellipse at 20% 50%, rgba(0,200,150,0.06) 0%, transparent 60%),
                              radial-gradient(ellipse at 80% 20%, rgba(0,150,200,0.05) 0%, transparent 60%);
        }
        .container { max-width: 780px; margin: 0 auto; }
        .header { border-left: 4px solid #00c896; padding-left: 20px; margin-bottom: 36px; }
        .badge {
            display: inline-block; background: rgba(0,200,150,0.12); color: #00c896;
            border: 1px solid #00c896; padding: 3px 12px; border-radius: 20px;
            font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;
        }
        h1 { font-size: 2rem; font-weight: 700; color: #00c896; margin-bottom: 6px; }
        .meta { color: #666; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; }
        .card { background: #0a1a18; border: 1px solid #0e2a24; border-radius: 12px; padding: 28px; margin-bottom: 24px; }
        .card-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #00c896; margin-bottom: 16px; font-family: 'Share Tech Mono', monospace; }
        .description { line-height: 1.9; color: #bbb; font-size: 0.95rem; }
        .description strong { color: #00e0a8; }
        code { font-family: 'Share Tech Mono', monospace; background: #071a16; color: #00c896; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; }
        .tls-flow {
            display: flex; align-items: center; gap: 8px;
            font-family: 'Share Tech Mono', monospace; font-size: 0.75rem;
            margin: 20px 0; flex-wrap: wrap;
        }
        .tls-box {
            padding: 8px 14px; border-radius: 6px; border: 1px solid;
            text-align: center; flex: 1; min-width: 80px;
        }
        .tls-client { background: rgba(0,200,150,0.1); border-color: #00c896; color: #00c896; }
        .tls-enc    { background: rgba(255,100,0,0.1); border-color: #ff6400; color: #ff6400; }
        .tls-server { background: rgba(100,150,255,0.1); border-color: #6496ff; color: #6496ff; }
        .tls-arrow  { color: #444; font-size: 1.2rem; }
        .hint-box { background: rgba(0,200,150,0.05); border: 1px solid rgba(0,200,150,0.2); border-radius: 8px; padding: 16px 20px; margin-top: 20px; }
        .hint-box .hint-title { color: #00c896; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
        .hint-box ul { list-style: none; }
        .hint-box ul li { padding: 4px 0; color: #aaa; font-size: 0.88rem; }
        .hint-box ul li::before { content: '→ '; color: #00c896; }
        .download-btn {
            display: inline-flex; align-items: center; gap: 10px;
            background: linear-gradient(135deg, #00c896, #008c66);
            color: white; padding: 13px 24px; border-radius: 8px;
            text-decoration: none; font-weight: 600; font-size: 0.9rem;
            transition: all 0.2s; margin-right: 12px; margin-bottom: 10px;
        }
        .download-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,200,150,0.35); }
        .file-info { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #555; margin-top: 8px; }
        .flag-form { display: flex; gap: 12px; flex-wrap: wrap; }
        .flag-input {
            flex: 1; min-width: 260px; background: #071a16; border: 1px solid #153828;
            border-radius: 8px; padding: 12px 18px; color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace; font-size: 0.9rem; outline: none; transition: border-color 0.2s;
        }
        .flag-input:focus { border-color: #00c896; }
        .flag-input::placeholder { color: #2a4a40; }
        .submit-btn {
            background: linear-gradient(135deg, #00c896, #008c66); color: white;
            border: none; padding: 12px 28px; border-radius: 8px;
            font-family: inherit; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: all 0.2s;
        }
        .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,200,150,0.4); }
        .result-correct { margin-top: 16px; padding: 16px 20px; background: rgba(34,197,94,0.1); border: 1px solid #22c55e; border-radius: 8px; color: #4ade80; font-family: 'Share Tech Mono', monospace; }
        .result-wrong { margin-top: 16px; padding: 16px 20px; background: rgba(239,68,68,0.1); border: 1px solid #ef4444; border-radius: 8px; color: #f87171; font-family: 'Share Tech Mono', monospace; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="badge">🔐 Forensics / Hard</div>
        <h1>🔐 TLS Challenge</h1>
        <p class="meta">Author: Walky &nbsp;|&nbsp; Points: 500 &nbsp;|&nbsp; Category: Forensics</p>
    </div>

    <div class="card">
        <div class="card-title">📋 Mission Briefing</div>
        <div class="tls-flow">
            <div class="tls-box tls-client">CLIENT</div>
            <div class="tls-arrow">⟶</div>
            <div class="tls-box tls-enc">[ ENCRYPTED HTTPS ]</div>
            <div class="tls-arrow">⟶</div>
            <div class="tls-box tls-server">SERVER</div>
        </div>
        <p class="description">
            Can you extract the flag from <strong>encrypted HTTPS traffic</strong>?<br><br>
            You have been given a packet capture (<code>capture.pcap</code>) that contains TLS-encrypted
            HTTPS sessions. The traffic is encrypted — but you also have a TLS <strong>pre-master secret key log</strong>
            file (<code>keylog.log</code>) that was extracted from the browser during the session.<br><br>
            Use this key log to <strong>decrypt the TLS traffic</strong> in Wireshark and find the hidden flag
            inside the decrypted HTTP payload.
        </p>
        <div class="hint-box">
            <div class="hint-title">💡 Step-by-Step Guide</div>
            <ul>
                <li>Open Wireshark → Edit → Preferences → Protocols → TLS</li>
                <li>In "(Pre)-Master-Secret log filename", load <code>keylog.log</code></li>
                <li>Apply filter: <code>http</code> or <code>http2</code> to see decrypted traffic</li>
                <li>Follow → HTTP Stream and search for the flag string</li>
                <li>Flag format: <code>GDUCTF{...}</code></li>
            </ul>
        </div>
    </div>

    <div class="card">
        <div class="card-title">⬇️ Challenge Files</div>
        <a href="{{ pcap_link }}" target="_blank" class="download-btn">⬇️ capture.pcap</a>
        <a href="{{ keylog_link }}" target="_blank" class="download-btn">🔑 keylog.log</a>
        <p class="file-info">📦 capture.pcap (~16 KB) &nbsp;+&nbsp; keylog.log (~4 KB) &nbsp;|&nbsp; Hosted on Google Drive</p>
    </div>

    <div class="card">
        <div class="card-title">🚩 Submit Flag</div>
        <form method="POST" class="flag-form">
            <input type="text" name="flag" class="flag-input" placeholder="GDUCTF{...}" autocomplete="off" value="{{ submitted or '' }}">
            <button type="submit" class="submit-btn">Submit Flag</button>
        </form>
        {% if result == 'correct' %}
        <div class="result-correct">✅ Correct! You successfully decrypted the HTTPS traffic!</div>
        {% elif result == 'wrong' %}
        <div class="result-wrong">❌ Wrong flag. Check your Wireshark decryption settings and search again.</div>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    submitted = None
    if request.method == "POST":
        submitted = request.form.get("flag", "").strip()
        if submitted == FLAG:
            result = "correct"
        else:
            result = "wrong"
    return render_template_string(TEMPLATE, result=result, submitted=submitted, pcap_link=PCAP_LINK, keylog_link=KEYLOG_LINK)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
