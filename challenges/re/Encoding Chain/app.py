from flask import Flask, render_template_string, send_file
import io, base64

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Encoding Chain — GDU-CTF</title>
<style>
body{font-family:monospace;background:#0d1117;color:#c9d1d9;max-width:800px;margin:0 auto;padding:40px 20px;}
h1{color:#00e5ff;letter-spacing:.1em;}
.badge{display:inline-block;padding:4px 12px;border-radius:4px;font-size:.75rem;font-weight:700;background:#1d4ed8;color:#fff;margin-bottom:16px;}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;margin:16px 0;}
.card h3{color:#00e5ff;margin:0 0 12px;}
pre{background:#0d1117;padding:16px;border-radius:6px;overflow-x:auto;color:#58d68d;border:1px solid #30363d;word-break:break-all;}
a.btn{display:inline-block;background:#00e5ff;color:#000;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none;margin-top:12px;}
.flag-format{color:#ffd600;font-weight:700;}
</style>
</head>
<body>
<h1>🔗 Encoding Chain</h1>
<span class="badge">RE — EASY</span>
<span class="badge" style="background:#15803d;">150 pts</span>

<div class="card">
  <h3>📋 Mô tả</h3>
  <p>Flag đã bị mã hóa qua nhiều lớp encoding. Hãy nhận diện từng lớp và decode theo đúng thứ tự.</p>
  <p>Flag format: <span class="flag-format">CTF{...}</span></p>
</div>

<div class="card">
  <h3>🔍 Encoded Data</h3>
  <p>Đây là dữ liệu đã được encode:</p>
  <pre id="encoded">{{ encoded }}</pre>
</div>

<div class="card">
  <h3>💡 Gợi ý</h3>
  <ul>
    <li>Base64 dùng ký tự: A-Z, a-z, 0-9, +, / và kết thúc bằng =</li>
    <li>Base32 dùng ký tự: A-Z, 2-7 và kết thúc bằng nhiều dấu =</li>
    <li>Dùng CyberChef: <a href="https://gchq.github.io/CyberChef" target="_blank" style="color:#00e5ff;">gchq.github.io/CyberChef</a></li>
    <li>Thử decode từng lớp một cho đến khi thấy CTF{</li>
  </ul>
</div>
</body>
</html>'''

@app.route('/')
def index():
    flag = b'CTF{b4s364_1n_b1n4ry_3ncod1ng}'
    # Layer 1: Base64
    l1 = base64.b64encode(flag)
    # Layer 2: Base32
    l2 = base64.b32encode(l1).decode()
    return render_template_string(HTML, encoded=l2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)