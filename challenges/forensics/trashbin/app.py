from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
PCAP_LINK = os.environ.get("PCAP_LINK", "https://drive.google.com/drive/folders/1p6JdkFsSEZYmtl94Ax8XYzHlTTWwN3M3")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trashbin - Forensics Challenge</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Exo 2', sans-serif;
            background: #0f0d08;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
            background-image: radial-gradient(ellipse at 20% 80%, rgba(200,160,0,0.06) 0%, transparent 60%),
                              radial-gradient(ellipse at 80% 10%, rgba(200,100,0,0.04) 0%, transparent 60%);
        }
        .container { max-width: 780px; margin: 0 auto; }
        .header { border-left: 4px solid #e6b800; padding-left: 20px; margin-bottom: 36px; }
        .badge {
            display: inline-block; background: rgba(230,184,0,0.12); color: #e6b800;
            border: 1px solid #e6b800; padding: 3px 12px; border-radius: 20px;
            font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px;
        }
        h1 { font-size: 2rem; font-weight: 700; color: #e6b800; margin-bottom: 6px; }
        .meta { color: #666; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; }
        .card { background: #111009; border: 1px solid #1e1c0e; border-radius: 12px; padding: 28px; margin-bottom: 24px; }
        .card-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #e6b800; margin-bottom: 16px; font-family: 'Share Tech Mono', monospace; }
        .description { line-height: 1.9; color: #bbb; font-size: 0.95rem; }
        .description strong { color: #ffcf40; }
        code { font-family: 'Share Tech Mono', monospace; background: #1a180a; color: #e6b800; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; }
        .trash-icon {
            text-align: center; font-size: 4rem; margin: 16px 0;
            animation: shake 3s ease-in-out infinite;
        }
        @keyframes shake {
            0%, 90%, 100% { transform: rotate(0); }
            92% { transform: rotate(-5deg); }
            96% { transform: rotate(5deg); }
            98% { transform: rotate(-3deg); }
        }
        .hint-box { background: rgba(230,184,0,0.05); border: 1px solid rgba(230,184,0,0.2); border-radius: 8px; padding: 16px 20px; margin-top: 20px; }
        .hint-box .hint-title { color: #e6b800; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
        .hint-box ul { list-style: none; }
        .hint-box ul li { padding: 4px 0; color: #aaa; font-size: 0.88rem; }
        .hint-box ul li::before { content: '→ '; color: #e6b800; }
        .download-btn {
            display: inline-flex; align-items: center; gap: 10px;
            background: linear-gradient(135deg, #e6b800, #b38c00);
            color: #0f0d08; padding: 14px 28px; border-radius: 8px;
            text-decoration: none; font-weight: 700; font-size: 0.95rem;
            transition: all 0.2s; margin-bottom: 10px;
        }
        .download-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(230,184,0,0.4); }
        .file-info { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #555; margin-top: 8px; }
        .flag-form { display: flex; gap: 12px; flex-wrap: wrap; }
        .flag-input {
            flex: 1; min-width: 260px; background: #1a180a; border: 1px solid #2a2508;
            border-radius: 8px; padding: 12px 18px; color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace; font-size: 0.9rem; outline: none; transition: border-color 0.2s;
        }
        .flag-input:focus { border-color: #e6b800; }
        .flag-input::placeholder { color: #3a3208; }
        .submit-btn {
            background: linear-gradient(135deg, #e6b800, #b38c00); color: #0f0d08;
            border: none; padding: 12px 28px; border-radius: 8px;
            font-family: inherit; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: all 0.2s;
        }
        .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(230,184,0,0.45); }
        .result-correct { margin-top: 16px; padding: 16px 20px; background: rgba(34,197,94,0.1); border: 1px solid #22c55e; border-radius: 8px; color: #4ade80; font-family: 'Share Tech Mono', monospace; }
        .result-wrong { margin-top: 16px; padding: 16px 20px; background: rgba(239,68,68,0.1); border: 1px solid #ef4444; border-radius: 8px; color: #f87171; font-family: 'Share Tech Mono', monospace; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="badge">🗑️ Forensics / Hard</div>
        <h1>🗑️ Trashbin</h1>
        <p class="meta">Author: bachtam2001 &nbsp;|&nbsp; Points: 500 &nbsp;|&nbsp; Category: Forensics</p>
    </div>

    <div class="card">
        <div class="card-title">📋 Mission Briefing</div>
        <div class="trash-icon">🗑️</div>
        <p class="description">
            Someone's been treating my computer like a <strong>trash bin</strong>, constantly dumping useless files into it.
            But it seems he got careless and dropped a <strong>really important one</strong> in there.
            Even though he deleted it afterward, it might have been <strong>too late</strong> — hehe 😅<br><br>
            Analyze the network capture to find what was transferred, and recover the deleted file
            hidden somewhere in the packet stream. The flag is waiting inside.
        </p>
        <div class="hint-box">
            <div class="hint-title">💡 Suggested Approach</div>
            <ul>
                <li>Open <code>trash.pcap</code> in Wireshark and check all protocols</li>
                <li>Look for <strong>FTP</strong>, <strong>HTTP</strong>, or <strong>SMB</strong> file transfer sessions</li>
                <li>Use: <strong>File → Export Objects → HTTP</strong> (or FTP-DATA) to extract files</li>
                <li>Try <strong>NetworkMiner</strong> for automatic file reassembly from PCAP</li>
                <li>Check transferred file contents — the flag will be inside one of them</li>
            </ul>
        </div>
    </div>

    <div class="card">
        <div class="card-title">⬇️ Challenge File</div>
        <a href="{{ pcap_link }}" target="_blank" class="download-btn">⬇️ Download trash.pcap</a>
        <p class="file-info">📦 trash.pcap &nbsp;|&nbsp; ~484 KB &nbsp;|&nbsp; Hosted on Google Drive</p>
    </div>

    <div class="card">
        <div class="card-title">🚩 Submit Flag</div>
        <form method="POST" class="flag-form">
            <input type="text" name="flag" class="flag-input" placeholder="GDUCTF{...}" autocomplete="off" value="{{ submitted or '' }}">
            <button type="submit" class="submit-btn">Submit Flag</button>
        </form>
        {% if result == 'correct' %}
        <div class="result-correct">✅ Correct! You dug through the trash and found the treasure!</div>
        {% elif result == 'wrong' %}
        <div class="result-wrong">❌ Wrong flag. Keep digging through the trash — it's in there somewhere!</div>
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
    return render_template_string(TEMPLATE, result=result, submitted=submitted, pcap_link=PCAP_LINK)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
