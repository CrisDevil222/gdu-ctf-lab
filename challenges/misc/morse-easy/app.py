from flask import Flask, render_template_string, request

app = Flask(__name__)

FLAG = 'CTF{m0rs3_c0d3_1s_fun}'

MORSE = {
    'A':'.-','B':'-...','C':'-.-.','D':'-..','E':'.','F':'..-.','G':'--.','H':'....','I':'..','J':'.---',
    'K':'-.-','L':'.-..','M':'--','N':'-.','O':'---','P':'.--.','Q':'--.-','R':'.-.','S':'...','T':'-',
    'U':'..-','V':'...-','W':'.--','X':'-..-','Y':'-.--','Z':'--..',
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-','5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    '{':'-.--.-','}':'-.--.-','_':'..__','!':'-.-.--'
}

def text_to_morse(text):
    result = []
    for c in text.upper():
        if c == ' ':
            result.append('/')
        elif c in MORSE:
            result.append(MORSE[c])
        else:
            result.append('?')
    return ' '.join(result)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Morse Code — GDU-CTF</title>
<style>
body{font-family:monospace;background:#0d1117;color:#c9d1d9;max-width:800px;margin:0 auto;padding:40px 20px;}
h1{color:#ffd600;letter-spacing:.1em;}
.badge{display:inline-block;padding:4px 12px;border-radius:4px;font-size:.75rem;font-weight:700;background:#a16207;color:#fff;margin-bottom:16px;}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;margin:16px 0;}
.card h3{color:#ffd600;margin:0 0 12px;}
pre{background:#0d1117;padding:16px;border-radius:6px;overflow-x:auto;color:#58d68d;border:1px solid #30363d;word-break:break-all;white-space:pre-wrap;}
input[type=text]{background:#0d1117;border:1px solid #30363d;color:#c9d1d9;padding:10px 14px;border-radius:6px;width:100%;font-family:monospace;font-size:.9rem;margin-top:8px;}
input[type=text]:focus{border-color:#ffd600;outline:none;}
button{background:#ffd600;color:#000;font-weight:700;padding:10px 24px;border-radius:6px;border:none;cursor:pointer;margin-top:12px;font-family:monospace;}
.success{background:#14532d;border:1px solid #16a34a;padding:12px;border-radius:6px;color:#4ade80;margin-top:12px;}
.error{background:#450a0a;border:1px solid #dc2626;padding:12px;border-radius:6px;color:#f87171;margin-top:12px;}
.flag-format{color:#ffd600;font-weight:700;}
</style>
</head>
<body>
<h1>📡 Morse Code</h1>
<span class="badge">MISC — EASY</span>
<span class="badge" style="background:#15803d;">100 pts</span>

<div class="card">
  <h3>📋 Mô tả</h3>
  <p>Decode chuỗi Morse Code dưới đây để tìm flag.</p>
  <p>Flag format: <span class="flag-format">CTF{...}</span></p>
</div>

<div class="card">
  <h3>📡 Morse Signal</h3>
  <pre>{{ morse }}</pre>
</div>

<div class="card">
  <h3>💡 Gợi ý</h3>
  <ul>
    <li>Dấu cách phân cách các ký tự</li>
    <li>Dấu / phân cách các từ</li>
    <li>Dùng: <a href="https://morsecode.world/international/translator.html" target="_blank" style="color:#ffd600;">morsecode.world</a></li>
    <li>Hoặc CyberChef: From Morse Code operation</li>
  </ul>
</div>

<div class="card">
  <h3>🚩 Submit Flag</h3>
  <form method="POST">
    <input type="text" name="flag" placeholder="CTF{...}" value="{{ submitted }}">
    <br><button type="submit">Submit</button>
  </form>
  {% if result == 'correct' %}
  <div class="success">✅ Correct! Well done!</div>
  {% elif result == 'wrong' %}
  <div class="error">❌ Wrong flag. Try again!</div>
  {% endif %}
</div>
</body>
</html>'''

@app.route('/', methods=['GET', 'POST'])
def index():
    morse = text_to_morse(FLAG)
    result = None
    submitted = ''
    if request.method == 'POST':
        submitted = request.form.get('flag', '')
        result = 'correct' if submitted.strip() == FLAG else 'wrong'
    return render_template_string(HTML, morse=morse, result=result, submitted=submitted)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)