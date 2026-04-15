from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")

# Google Drive direct download links
DISK_IMG_LINK = os.environ.get("DISK_IMG_LINK", "https://drive.google.com/drive/folders/1p6JdkFsSEZYmtl94Ax8XYzHlTTWwN3M3")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disk Partition - Forensics Challenge</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Exo 2', sans-serif;
            background: #0d0d0d;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
            background-image: radial-gradient(ellipse at 20% 50%, rgba(255,100,0,0.05) 0%, transparent 60%),
                              radial-gradient(ellipse at 80% 20%, rgba(255,50,0,0.05) 0%, transparent 60%);
        }
        .container { max-width: 780px; margin: 0 auto; }
        .header {
            border-left: 4px solid #ff6400;
            padding-left: 20px;
            margin-bottom: 36px;
        }
        .badge {
            display: inline-block;
            background: rgba(255,100,0,0.15);
            color: #ff6400;
            border: 1px solid #ff6400;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        h1 { font-size: 2rem; font-weight: 700; color: #ff6400; margin-bottom: 6px; }
        .meta { color: #666; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; }
        .card {
            background: #111;
            border: 1px solid #222;
            border-radius: 12px;
            padding: 28px;
            margin-bottom: 24px;
        }
        .card-title {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #ff6400;
            margin-bottom: 16px;
            font-family: 'Share Tech Mono', monospace;
        }
        .description {
            line-height: 1.9;
            color: #bbb;
            font-size: 0.95rem;
        }
        .description strong { color: #ff8533; }
        .hint-box {
            background: rgba(255,100,0,0.05);
            border: 1px solid rgba(255,100,0,0.2);
            border-radius: 8px;
            padding: 16px 20px;
            margin-top: 20px;
        }
        .hint-box .hint-title { color: #ff6400; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
        .hint-box ul { list-style: none; }
        .hint-box ul li { padding: 4px 0; color: #aaa; font-size: 0.88rem; }
        .hint-box ul li::before { content: '→ '; color: #ff6400; }
        code { font-family: 'Share Tech Mono', monospace; background: #1a1a1a; color: #ff8533; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; }
        .download-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: linear-gradient(135deg, #ff6400, #cc4a00);
            color: white;
            padding: 14px 28px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.2s;
            margin-bottom: 12px;
        }
        .download-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255,100,0,0.35); }
        .file-info {
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.8rem;
            color: #555;
            margin-top: 8px;
        }
        .flag-form { display: flex; gap: 12px; flex-wrap: wrap; }
        .flag-input {
            flex: 1; min-width: 260px;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 12px 18px;
            color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }
        .flag-input:focus { border-color: #ff6400; }
        .flag-input::placeholder { color: #444; }
        .submit-btn {
            background: linear-gradient(135deg, #ff6400, #cc4a00);
            color: white;
            border: none;
            padding: 12px 28px;
            border-radius: 8px;
            font-family: inherit;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(255,100,0,0.4); }
        .result-correct {
            margin-top: 16px;
            padding: 16px 20px;
            background: rgba(34,197,94,0.1);
            border: 1px solid #22c55e;
            border-radius: 8px;
            color: #4ade80;
            font-family: 'Share Tech Mono', monospace;
        }
        .result-wrong {
            margin-top: 16px;
            padding: 16px 20px;
            background: rgba(239,68,68,0.1);
            border: 1px solid #ef4444;
            border-radius: 8px;
            color: #f87171;
            font-family: 'Share Tech Mono', monospace;
        }
        .disk-visual {
            display: flex;
            gap: 4px;
            margin: 20px 0;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.75rem;
        }
        .partition {
            flex: 1;
            padding: 10px 6px;
            text-align: center;
            border-radius: 4px;
            border: 1px solid #333;
        }
        .p1 { background: rgba(255,100,0,0.1); border-color: #ff6400; color: #ff6400; }
        .p2 { background: rgba(100,100,255,0.1); border-color: #6464ff; color: #6464ff; }
        .p3 { background: rgba(100,255,100,0.1); border-color: #64ff64; color: #64ff64; }
        .p4 { background: rgba(255,255,100,0.1); border-color: #ffff64; color: #ffff64; }
        .p-label { font-size: 0.65rem; color: #555; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="badge">🕵️ Forensics / Hard</div>
        <h1>💽 Disk Partition</h1>
        <p class="meta">Author: Walky &nbsp;|&nbsp; Points: 500 &nbsp;|&nbsp; Category: Forensics</p>
    </div>

    <div class="card">
        <div class="card-title">📋 Mission Briefing</div>
        <p class="description">
            <strong>Too many flags... but only one is real.</strong><br><br>
            You have been given a raw disk image. Inside it, there are multiple partitions — and scattered across the disk are strings that look like flags.
            But here's the catch: <strong>only one of them is the real deal</strong>. The rest are decoys planted to throw you off.<br><br>
            Your mission is to mount the disk image, analyze all partitions, and determine which flag is legitimate.
        </p>
        <div class="disk-visual">
            <div class="partition p1">sda1<br><span class="p-label">FAT32</span></div>
            <div class="partition p2">sda2<br><span class="p-label">ext4</span></div>
            <div class="partition p3">sda3<br><span class="p-label">NTFS</span></div>
            <div class="partition p4">sda4<br><span class="p-label">???</span></div>
        </div>
        <div class="hint-box">
            <div class="hint-title">💡 Suggested Tools</div>
            <ul>
                <li>Mount image: <code>fdisk -l disk.img</code> then <code>mount -o loop,offset=...</code></li>
                <li>GUI tool: <strong>Autopsy</strong> or <strong>FTK Imager</strong></li>
                <li>Linux quick scan: <code>strings disk.img | grep GDUCTF</code></li>
                <li>Volatility / Sleuth Kit for deep partition analysis</li>
            </ul>
        </div>
    </div>

    <div class="card">
        <div class="card-title">⬇️ Challenge File</div>
        <a href="{{ disk_link }}" target="_blank" class="download-btn">
            ⬇️ Download disk.img
        </a>
        <p class="file-info">📦 disk.img &nbsp;|&nbsp; ~305 MB &nbsp;|&nbsp; Hosted on Google Drive</p>
    </div>

    <div class="card">
        <div class="card-title">🚩 Submit Flag</div>
        <form method="POST" class="flag-form">
            <input type="text" name="flag" class="flag-input" placeholder="GDUCTF{...}" autocomplete="off" value="{{ submitted or '' }}">
            <button type="submit" class="submit-btn">Submit Flag</button>
        </form>
        {% if result == 'correct' %}
        <div class="result-correct">✅ Correct! Well done — you found the real flag among the decoys!</div>
        {% elif result == 'wrong' %}
        <div class="result-wrong">❌ Wrong flag. That might be one of the decoys. Keep digging!</div>
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
    return render_template_string(TEMPLATE, result=result, submitted=submitted, disk_link=DISK_IMG_LINK)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
