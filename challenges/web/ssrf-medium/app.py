from flask import Flask, request, render_template_string, jsonify
import urllib.request
import urllib.parse
import os
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")

# ─────────────────────────────────────────
# Internal metadata server on port 8888
# Simulates a cloud metadata API (like AWS IMDSv1)
# ─────────────────────────────────────────
class InternalMetadataHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logs

    def do_GET(self):
        if self.path == "/latest/meta-data/":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"ami-id\nhostname\ninstance-type\niam/\nsecurity-credentials/\n")
        elif self.path == "/latest/meta-data/hostname":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"internal-server.ctf.local")
        elif self.path == "/latest/meta-data/instance-type":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"t2.micro")
        elif self.path == "/latest/meta-data/iam/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"security-credentials/\n")
        elif self.path == "/latest/meta-data/iam/security-credentials/":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"gdu-ctf-role\n")
        elif self.path == "/latest/meta-data/iam/security-credentials/gdu-ctf-role":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            secret = json.dumps({
                "Code": "Success",
                "Type": "AWS-HMAC",
                "AccessKeyId": "AKIAIOSFODNN7CTFTEST",
                "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYCTFSECRETKEY",
                "Token": FLAG,
                "Expiration": "2099-01-01T00:00:00Z"
            }, indent=2)
            self.wfile.write(secret.encode())
        elif self.path == "/internal/admin":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = json.dumps({"status": "ok", "flag": FLAG, "users": ["admin", "root"]})
            self.wfile.write(data.encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def start_internal_server():
    server = HTTPServer(("127.0.0.1", 8888), InternalMetadataHandler)
    server.serve_forever()

# Start internal server in background thread
t = threading.Thread(target=start_internal_server, daemon=True)
t.start()

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDU Fetch Tool - SSRF Challenge</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: radial-gradient(ellipse at top, #0d1b33 0%, #040d1a 60%);
            min-height: 100vh;
            color: #cdd6f4;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 60px 20px;
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }
        .logo-icon {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #89b4fa, #cba6f7);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        h1 {
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(90deg, #89b4fa, #cba6f7, #f38ba8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            color: #6c7086;
            font-size: 0.9rem;
            margin-bottom: 40px;
            text-align: center;
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(249, 168, 212, 0.12);
            color: #f38ba8;
            border: 1px solid rgba(243, 139, 168, 0.3);
            padding: 5px 14px;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            margin-top: 10px;
            letter-spacing: 0.05em;
        }
        .main-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(137, 180, 250, 0.15);
            border-radius: 20px;
            padding: 36px;
            width: 100%;
            max-width: 780px;
            backdrop-filter: blur(10px);
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
        }
        .form-label {
            display: block;
            font-size: 0.82rem;
            font-weight: 600;
            color: #89b4fa;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }
        .url-row {
            display: flex;
            gap: 10px;
            margin-bottom: 16px;
        }
        .url-row input {
            flex: 1;
            padding: 13px 16px;
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(137, 180, 250, 0.2);
            border-radius: 10px;
            color: #cdd6f4;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.88rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        .url-row input:focus {
            border-color: #89b4fa;
            box-shadow: 0 0 0 3px rgba(137, 180, 250, 0.1);
        }
        .url-row button {
            padding: 13px 26px;
            background: linear-gradient(135deg, #89b4fa, #cba6f7);
            border: none;
            border-radius: 10px;
            color: #1e1e2e;
            font-weight: 700;
            font-size: 0.88rem;
            cursor: pointer;
            transition: opacity 0.2s, transform 0.1s;
            white-space: nowrap;
        }
        .url-row button:hover { opacity: 0.9; transform: translateY(-1px); }

        .hint-section {
            background: rgba(249, 168, 212, 0.06);
            border: 1px solid rgba(243, 139, 168, 0.2);
            border-radius: 12px;
            padding: 18px 20px;
            margin-bottom: 24px;
            font-size: 0.82rem;
            color: #f2cdcd;
            line-height: 1.6;
        }
        .hint-section strong { color: #f38ba8; }
        .hint-section code {
            background: rgba(0,0,0,0.4);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: #cba6f7;
        }
        .examples {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 12px;
        }
        .example-chip {
            background: rgba(137, 180, 250, 0.08);
            border: 1px solid rgba(137, 180, 250, 0.2);
            color: #89b4fa;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-family: 'JetBrains Mono', monospace;
            cursor: pointer;
            transition: background 0.15s;
        }
        .example-chip:hover { background: rgba(137, 180, 250, 0.15); }

        .response-section { margin-top: 24px; }
        .response-meta {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }
        .response-label {
            font-size: 0.8rem;
            color: #6c7086;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }
        .status-ok {
            background: rgba(166, 227, 161, 0.15);
            color: #a6e3a1;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            border: 1px solid rgba(166,227,161,0.3);
        }
        .status-err {
            background: rgba(243, 139, 168, 0.15);
            color: #f38ba8;
            padding: 2px 10px;
            border-radius: 999px;
            font-size: 0.72rem;
            font-weight: 600;
            border: 1px solid rgba(243,139,168,0.3);
        }
        .response-body {
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 20px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #a6e3a1;
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 400px;
            overflow-y: auto;
            line-height: 1.6;
        }
        .response-body::-webkit-scrollbar { width: 6px; }
        .response-body::-webkit-scrollbar-track { background: transparent; }
        .response-body::-webkit-scrollbar-thumb { background: #313244; border-radius: 3px; }
        .error-body {
            background: rgba(243, 139, 168, 0.08);
            border: 1px solid rgba(243,139,168,0.2);
            border-radius: 12px;
            padding: 14px 18px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            color: #f38ba8;
        }
        .divider {
            height: 1px;
            background: rgba(255,255,255,0.06);
            margin: 24px 0;
        }
    </style>
    <script>
        function fillURL(url) {
            document.getElementById('url-input').value = url;
        }
    </script>
</head>
<body>
    <div class="logo">
        <div class="logo-icon">🌐</div>
        <h1>GDU Fetch Tool</h1>
    </div>
    <p class="subtitle">Server-Side Request Forwarder — Fetch any public URL</p>
    <span class="badge">🔴 Challenge: SSRF [Medium]</span>
    <br><br>

    <div class="main-card">


        <label class="form-label" for="url-input">URL to Fetch</label>
        <form method="GET">
            <div class="url-row">
                <input type="text" name="url" id="url-input"
                    placeholder="https://example.com"
                    value="{{ url | e }}">
                <button type="submit">Fetch →</button>
            </div>
        </form>

        {% if url %}
        <div class="divider"></div>
        <div class="response-section">
            <div class="response-meta">
                <span class="response-label">Response</span>
                {% if error %}
                <span class="status-err">ERROR</span>
                {% else %}
                <span class="status-ok">200 OK</span>
                {% endif %}
            </div>
            {% if error %}
            <div class="error-body">{{ error }}</div>
            {% else %}
            <div class="response-body">{{ content }}</div>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

BLOCKED_SCHEMES = []  # No blacklist — fully vulnerable for demo

@app.route("/", methods=["GET"])
def index():
    url = request.args.get("url", "")
    content = None
    error = None

    if url:
        try:
            # VULNERABLE: No SSRF protection — allows internal requests
            req = urllib.request.Request(url, headers={"User-Agent": "GDU-Fetch/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                content = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            error = str(e)

    return render_template_string(TEMPLATE, url=url, content=content, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
