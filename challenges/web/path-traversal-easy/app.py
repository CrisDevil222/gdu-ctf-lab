from flask import Flask, request, render_template_string, abort
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{p4th_tr4v3rs4l_d1rect0ry_l34k}")

# Tạo file bí mật chứa flag
os.makedirs("/tmp/files/public", exist_ok=True)
os.makedirs("/tmp/secret", exist_ok=True)
with open("/tmp/files/public/welcome.txt", "w") as f:
    f.write("Welcome to GDU Library! Browse our public documents below.")
with open("/tmp/files/public/about.txt", "w") as f:
    f.write("GDU Library - A digital archive for students and staff.")
with open("/tmp/files/public/rules.txt", "w") as f:
    f.write("1. Do not share your credentials.\n2. Respect copyright.\n3. Report bugs to admin.")
with open("/tmp/secret/flag.txt", "w") as f:
    f.write(FLAG)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GDU Library - File Viewer</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(90deg, #a78bfa, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }
        .header p { color: #9ca3af; font-size: 0.9rem; }
        .badge {
            display: inline-block;
            background: linear-gradient(90deg, #065f46, #047857);
            color: #6ee7b7;
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 8px;
            border: 1px solid #34d399;
        }
        .card {
            background: rgba(255,255,255,0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 32px;
            width: 100%;
            max-width: 700px;
            margin-bottom: 24px;
        }
        .card h2 {
            font-size: 1rem;
            font-weight: 600;
            color: #a78bfa;
            margin-bottom: 16px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .file-list { list-style: none; }
        .file-list li {
            margin-bottom: 8px;
        }
        .file-list a {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #93c5fd;
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 8px;
            background: rgba(96, 165, 250, 0.05);
            border: 1px solid rgba(96, 165, 250, 0.1);
            transition: all 0.2s;
            font-size: 0.9rem;
        }
        .file-list a:hover {
            background: rgba(96, 165, 250, 0.15);
            border-color: rgba(96, 165, 250, 0.3);
            transform: translateX(4px);
        }
        .hint-box {
            background: rgba(251, 191, 36, 0.08);
            border: 1px solid rgba(251, 191, 36, 0.3);
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 24px;
            width: 100%;
            max-width: 700px;
            font-size: 0.85rem;
            color: #fcd34d;
        }
        .hint-box strong { color: #fbbf24; }
        .content-box {
            background: rgba(0,0,0,0.4);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            color: #d1fae5;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.6;
        }
        .file-title {
            font-size: 0.8rem;
            color: #6b7280;
            margin-bottom: 8px;
            font-family: 'Courier New', monospace;
        }
        .error-box {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 12px;
            padding: 16px 20px;
            color: #fca5a5;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 GDU Library</h1>
        <p>Digital Document Archive</p>
        <span class="badge">Challenge: Path Traversal [Easy]</span>
    </div>

    <div class="hint-box">
        💡 <strong>Hint:</strong> The server reads files from <code>/tmp/files/public/</code>.
        Try to navigate outside the intended directory...
        The endpoint is <code>/?file=welcome.txt</code>
    </div>

    <div class="card">
        <h2>📂 Public Documents</h2>
        <ul class="file-list">
            <li><a href="/?file=welcome.txt">📄 welcome.txt</a></li>
            <li><a href="/?file=about.txt">📄 about.txt</a></li>
            <li><a href="/?file=rules.txt">📄 rules.txt</a></li>
        </ul>
    </div>

    {% if filename %}
    <div class="card">
        <h2>📖 File Viewer</h2>
        <p class="file-title">Reading: {{ filename }}</p>
        {% if content %}
        <div class="content-box">{{ content }}</div>
        {% else %}
        <div class="error-box">❌ {{ error }}</div>
        {% endif %}
    </div>
    {% endif %}
</body>
</html>
"""

BASE_DIR = "/tmp/files/public"

@app.route("/", methods=["GET"])
def index():
    filename = request.args.get("file", None)
    content = None
    error = None

    if filename:
        # VULNERABLE: No sanitization of path traversal sequences
        filepath = os.path.join(BASE_DIR, filename)
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except FileNotFoundError:
            error = f"File not found: {filepath}"
        except Exception as e:
            error = str(e)

    return render_template_string(
        TEMPLATE,
        filename=filename,
        content=content,
        error=error
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
