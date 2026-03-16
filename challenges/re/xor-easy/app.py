from flask import Flask, render_template_string, send_file
import io

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>XOR Cipher — GDU-CTF</title>
<style>
body{font-family:monospace;background:#0d1117;color:#c9d1d9;max-width:800px;margin:0 auto;padding:40px 20px;}
h1{color:#00e5ff;letter-spacing:.1em;}
.badge{display:inline-block;padding:4px 12px;border-radius:4px;font-size:.75rem;font-weight:700;background:#1d4ed8;color:#fff;margin-bottom:16px;}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;margin:16px 0;}
.card h3{color:#00e5ff;margin:0 0 12px;}
pre{background:#0d1117;padding:16px;border-radius:6px;overflow-x:auto;color:#58d68d;border:1px solid #30363d;}
a.btn{display:inline-block;background:#00e5ff;color:#000;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none;margin-top:12px;}
a.btn:hover{background:#00b8d4;}
.flag-format{color:#ffd600;font-weight:700;}
</style>
</head>
<body>
<h1>🔐 XOR Cipher</h1>
<span class="badge">RE — EASY</span>
<span class="badge" style="background:#15803d;">100 pts</span>

<div class="card">
  <h3>📋 Mô tả</h3>
  <p>Một chương trình đã mã hóa flag bằng phép toán XOR với một key bí mật. Hãy phân tích binary, tìm key và giải mã flag.</p>
  <p>Flag format: <span class="flag-format">CTF{...}</span></p>
</div>

<div class="card">
  <h3>💡 Gợi ý</h3>
  <ul>
    <li>Dùng <code>strings</code> để tìm chuỗi trong binary</li>
    <li>Dùng Ghidra hoặc IDA để decompile</li>
    <li>XOR có tính chất: A XOR K = C → C XOR K = A</li>
    <li>Nếu biết flag bắt đầu bằng <code>CTF{</code>, bạn có thể tìm ra key</li>
  </ul>
</div>

<div class="card">
  <h3>📥 Download</h3>
  <p>Download file binary và phân tích:</p>
  <a class="btn" href="/download">⬇ Download xor_crackme</a>
</div>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download')
def download():
    # Tạo binary với flag XOR encoded
    key = 0x59
    flag = b'CTF{x0r_1s_s1mpl3_crypt0}'
    cipher = bytes([b ^ key for b in flag])
    
    # Tạo ELF-like binary giả với cipher embedded
    binary = b'\x7fELF' + b'\x00' * 12
    binary += b'XOR Challenge Binary\x00'
    binary += b'Enter the key to decrypt: \x00'
    binary += b'Wrong key!\x00'
    binary += b'Correct!\x00'
    binary += b'\x00' * 32
    binary += b'cipher_data:\x00'
    binary += cipher
    binary += b'\x00' * 32
    binary += b'key_hint: single byte XOR\x00'
    binary += b'\x00' * 64
    
    return send_file(
        io.BytesIO(binary),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='xor_crackme'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)