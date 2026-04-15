from flask import Flask, render_template_string, request
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")
WAV_LINK = os.environ.get("WAV_LINK", "https://drive.google.com/drive/folders/1p6JdkFsSEZYmtl94Ax8XYzHlTTWwN3M3")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Hidden - Forensics Challenge</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Exo 2', sans-serif;
            background: #0a0a1a;
            color: #e0e0e0;
            min-height: 100vh;
            padding: 40px 20px;
            background-image: radial-gradient(ellipse at 30% 50%, rgba(100,0,255,0.06) 0%, transparent 60%),
                              radial-gradient(ellipse at 70% 20%, rgba(0,150,255,0.05) 0%, transparent 60%);
        }
        .container { max-width: 780px; margin: 0 auto; }
        .header { border-left: 4px solid #7b46ff; padding-left: 20px; margin-bottom: 36px; }
        .badge {
            display: inline-block;
            background: rgba(123,70,255,0.15);
            color: #7b46ff;
            border: 1px solid #7b46ff;
            padding: 3px 12px;
            border-radius: 20px;
            font-size: 0.75rem; letter-spacing: 1px;
            text-transform: uppercase; margin-bottom: 10px;
        }
        h1 { font-size: 2rem; font-weight: 700; color: #7b46ff; margin-bottom: 6px; }
        .meta { color: #666; font-size: 0.85rem; font-family: 'Share Tech Mono', monospace; }
        .card { background: #111; border: 1px solid #1e1e2e; border-radius: 12px; padding: 28px; margin-bottom: 24px; }
        .card-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; color: #7b46ff; margin-bottom: 16px; font-family: 'Share Tech Mono', monospace; }
        .description { line-height: 1.9; color: #bbb; font-size: 0.95rem; }
        .description strong { color: #9d6fff; }
        code { font-family: 'Share Tech Mono', monospace; background: #1a1a2e; color: #9d6fff; padding: 2px 8px; border-radius: 4px; font-size: 0.85rem; }
        .hint-box { background: rgba(123,70,255,0.05); border: 1px solid rgba(123,70,255,0.2); border-radius: 8px; padding: 16px 20px; margin-top: 20px; }
        .hint-box .hint-title { color: #7b46ff; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
        .hint-box ul { list-style: none; }
        .hint-box ul li { padding: 4px 0; color: #aaa; font-size: 0.88rem; }
        .hint-box ul li::before { content: '→ '; color: #7b46ff; }

        /* Audio visualizer animation */
        .visualizer { display: flex; align-items: flex-end; gap: 3px; height: 60px; margin: 20px 0; justify-content: center; }
        .bar { width: 6px; background: linear-gradient(to top, #7b46ff, #00d4ff); border-radius: 3px 3px 0 0; animation: wave 1.2s ease-in-out infinite; }
        .bar:nth-child(2) { animation-delay: 0.1s; }
        .bar:nth-child(3) { animation-delay: 0.2s; }
        .bar:nth-child(4) { animation-delay: 0.3s; }
        .bar:nth-child(5) { animation-delay: 0.4s; }
        .bar:nth-child(6) { animation-delay: 0.3s; }
        .bar:nth-child(7) { animation-delay: 0.2s; }
        .bar:nth-child(8) { animation-delay: 0.1s; }
        .bar:nth-child(9) { animation-delay: 0s; }
        @keyframes wave {
            0%, 100% { height: 8px; opacity: 0.4; }
            50% { height: 50px; opacity: 1; }
        }

        .download-btn {
            display: inline-flex; align-items: center; gap: 10px;
            background: linear-gradient(135deg, #7b46ff, #5a2de0);
            color: white; padding: 14px 28px; border-radius: 8px;
            text-decoration: none; font-weight: 600; font-size: 0.95rem;
            transition: all 0.2s; margin-bottom: 8px; margin-right: 12px;
        }
        .download-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(123,70,255,0.4); }
        .file-info { font-family: 'Share Tech Mono', monospace; font-size: 0.8rem; color: #555; margin-top: 8px; }
        .flag-form { display: flex; gap: 12px; flex-wrap: wrap; }
        .flag-input {
            flex: 1; min-width: 260px; background: #1a1a1a; border: 1px solid #333;
            border-radius: 8px; padding: 12px 18px; color: #e0e0e0;
            font-family: 'Share Tech Mono', monospace; font-size: 0.9rem;
            outline: none; transition: border-color 0.2s;
        }
        .flag-input:focus { border-color: #7b46ff; }
        .flag-input::placeholder { color: #444; }
        .submit-btn {
            background: linear-gradient(135deg, #7b46ff, #5a2de0); color: white;
            border: none; padding: 12px 28px; border-radius: 8px;
            font-family: inherit; font-weight: 600; font-size: 0.95rem;
            cursor: pointer; transition: all 0.2s;
        }
        .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(123,70,255,0.45); }
        .result-correct { margin-top: 16px; padding: 16px 20px; background: rgba(34,197,94,0.1); border: 1px solid #22c55e; border-radius: 8px; color: #4ade80; font-family: 'Share Tech Mono', monospace; }
        .result-wrong { margin-top: 16px; padding: 16px 20px; background: rgba(239,68,68,0.1); border: 1px solid #ef4444; border-radius: 8px; color: #f87171; font-family: 'Share Tech Mono', monospace; }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="badge">🎵 Forensics / Hard</div>
        <h1>🎵 File Hidden</h1>
        <p class="meta">Author: Walky &nbsp;|&nbsp; Points: 500 &nbsp;|&nbsp; Category: Forensics</p>
    </div>

    <div class="card">
        <div class="card-title">📋 Mission Briefing</div>
        <div class="visualizer">
            <div class="bar"></div><div class="bar"></div><div class="bar"></div>
            <div class="bar"></div><div class="bar"></div><div class="bar"></div>
            <div class="bar"></div><div class="bar"></div><div class="bar"></div>
        </div>
        <p class="description">
            Relax and chill with this lo-fi track... but <strong>listen carefully</strong> —
            there might be something hidden in the <strong>sound waves</strong>.<br><br>
            What sounds like a peaceful background music might be concealing a secret message.
            Analyze the audio carefully — the flag could be hiding in the <strong>spectrogram</strong>,
            encoded in the <strong>frequency domain</strong>, or embedded via other audio steganography techniques.
        </p>
        <div class="hint-box">
            <div class="hint-title">💡 Suggested Tools</div>
            <ul>
                <li>View spectrogram: <strong>Sonic Visualizer</strong> (Add Spectrogram layer)</li>
                <li>GUI: <strong>Audacity</strong> → Spectrogram view or Analyze menu</li>
                <li>CLI: <code>sox input.wav -n spectrogram -o spec.png</code></li>
                <li>Also check file metadata: <code>exiftool JACK_J97_....wav</code></li>
                <li>Try <strong>DeepSound</strong> for LSB audio steganography</li>
            </ul>
        </div>
    </div>

    <div class="card">
        <div class="card-title">⬇️ Challenge Files</div>
        <a href="{{ wav_link }}" target="_blank" class="download-btn">⬇️ Download WAV File</a>
        <p class="file-info">📦 JACK_J97_ | _THIÊN_LÝ_OI.wav &nbsp;|&nbsp; ~33.5 MB &nbsp;|&nbsp; Hosted on Google Drive</p>
    </div>

    <div class="card">
        <div class="card-title">🚩 Submit Flag</div>
        <form method="POST" class="flag-form">
            <input type="text" name="flag" class="flag-input" placeholder="GDUCTF{...}" autocomplete="off" value="{{ submitted or '' }}">
            <button type="submit" class="submit-btn">Submit Flag</button>
        </form>
        {% if result == 'correct' %}
        <div class="result-correct">✅ Correct! You heard what others couldn't!</div>
        {% elif result == 'wrong' %}
        <div class="result-wrong">❌ Wrong flag. Keep listening... the secret is in the waves.</div>
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
    return render_template_string(TEMPLATE, result=result, submitted=submitted, wav_link=WAV_LINK)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
