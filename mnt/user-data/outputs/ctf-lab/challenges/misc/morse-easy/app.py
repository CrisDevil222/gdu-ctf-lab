from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{m0rs3_c0d3_1s_fun}")

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '{': '-.--.', '}': '-.--.-', '_': '..--.-'
}

def to_morse(text):
    result = []
    for ch in text.upper():
        if ch == ' ':
            result.append('/')
        elif ch in MORSE_CODE:
            result.append(MORSE_CODE[ch])
        else:
            result.append('?')
    return ' '.join(result)

MORSE_FLAG = to_morse(FLAG)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Misc - Morse Code</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Courier New',monospace; background:#1a1200; color:#ffd700; min-height:100vh; padding:40px; }
        .container { max-width:700px; margin:0 auto; }
        h1 { color:#ffd700; font-size:2rem; margin-bottom:8px; text-shadow:0 0 10px #ffd700; }
        .sub { color:#886600; margin-bottom:32px; }
        .morse-box { background:#111; border:2px solid #ffd700; border-radius:8px; padding:32px; margin-bottom:24px; text-align:center; }
        .morse-text { font-size:1.1rem; letter-spacing:3px; line-height:2; word-break:break-all; color:#ffff00; }
        .hint { background:#111; border-left:3px solid #ffd700; padding:16px; color:#ffd700; font-size:0.85rem; line-height:1.8; margin-bottom:24px; }
        .table { width:100%; border-collapse:collapse; margin-bottom:24px; font-size:0.8rem; }
        .table td { padding:4px 8px; border:1px solid #443300; text-align:center; }
        .table tr:nth-child(even) td { background:#111; }
        form { display:flex; gap:12px; }
        input { flex:1; padding:12px; background:#111; border:1px solid #ffd700; color:#ffd700; font-family:inherit; border-radius:4px; }
        button { padding:12px 24px; background:#221100; border:1px solid #ffd700; color:#ffd700; font-family:inherit; cursor:pointer; border-radius:4px; }
        .result { margin-top:16px; padding:12px; border-radius:4px; }
        .success { border:1px solid #00ff00; color:#00ff00; background:#001100; }
        .error { border:1px solid #ff0000; color:#ff0000; background:#110000; }
    </style>
</head>
<body>
<div class="container">
    <h1>·−·· ·−−·</h1>
    <p class="sub">Misc — Morse Code [Easy]</p>

    <div class="morse-box">
        <p style="color:#886600;margin-bottom:16px;font-size:0.85rem">📡 Intercepted transmission:</p>
        <div class="morse-text">{{ morse_flag }}</div>
    </div>

    <div class="hint">
        💡 <strong>Hint:</strong> Đây là Morse code.<br>
        <code>.</code> = dit (ngắn) &nbsp;|&nbsp; <code>-</code> = dah (dài) &nbsp;|&nbsp; <code>/</code> = space<br><br>
        <strong>Tools:</strong> morsecode.world hoặc dcodex.com/morse-code<br>
        Lưu ý: <code>-.--.  = {</code> &nbsp;|&nbsp; <code>-.--.- = }</code> &nbsp;|&nbsp; <code>..--.- = _</code>
    </div>

    <table class="table">
        <tr><td>A .-</td><td>B -...</td><td>C -.-.</td><td>D -..</td><td>E .</td><td>F ..-.</td></tr>
        <tr><td>G --.</td><td>H ....</td><td>I ..</td><td>J .---</td><td>K -.-</td><td>L .-..</td></tr>
        <tr><td>M --</td><td>N -.</td><td>O ---</td><td>P .--.</td><td>Q --.-</td><td>R .-.</td></tr>
        <tr><td>S ...</td><td>T -</td><td>U ..-</td><td>V ...-</td><td>W .--</td><td>X -..-</td></tr>
        <tr><td>Y -.--</td><td>Z --..</td><td>0 -----</td><td>1 .----</td><td>2 ..---</td><td>3 ...--</td></tr>
        <tr><td>4 ....-</td><td>5 .....</td><td>6 -....</td><td>7 --...</td><td>8 ---..</td><td>9 ----.</td></tr>
    </table>

    <form method="POST">
        <input type="text" name="flag" placeholder="CTF{...}" autocomplete="off">
        <button type="submit">Submit</button>
    </form>
    {% if result %}
    <div class="result {{ result_class }}">{{ result }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    result_class = None
    if request.method == "POST":
        flag = request.form.get("flag", "").strip()
        if flag == FLAG:
            result = f"🎉 Decoded! {FLAG}"
            result_class = "success"
        else:
            result = "❌ Wrong! Try again..."
            result_class = "error"
    return render_template_string(TEMPLATE, result=result, result_class=result_class, morse_flag=MORSE_FLAG)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
