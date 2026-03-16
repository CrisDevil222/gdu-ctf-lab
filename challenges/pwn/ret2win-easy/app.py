from flask import Flask, render_template_string, send_file
import io

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>ret2win — GDU-CTF</title>
<style>
body{font-family:monospace;background:#0d1117;color:#c9d1d9;max-width:800px;margin:0 auto;padding:40px 20px;}
h1{color:#ff3366;letter-spacing:.1em;}
.badge{display:inline-block;padding:4px 12px;border-radius:4px;font-size:.75rem;font-weight:700;background:#be123c;color:#fff;margin-bottom:16px;}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;margin:16px 0;}
.card h3{color:#ff3366;margin:0 0 12px;}
pre{background:#0d1117;padding:16px;border-radius:6px;overflow-x:auto;color:#58d68d;border:1px solid #30363d;}
a.btn{display:inline-block;background:#ff3366;color:#fff;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none;margin-top:12px;}
.flag-format{color:#ffd600;font-weight:700;}
code{background:#1f2937;padding:2px 6px;border-radius:3px;color:#58d68d;}
</style>
</head>
<body>
<h1>🎯 ret2win</h1>
<span class="badge">PWN — EASY+</span>
<span class="badge" style="background:#1d4ed8;">250 pts</span>

<div class="card">
  <h3>📋 Mô tả</h3>
  <p>Binary có hàm <code>win()</code> ẩn không bao giờ được gọi. Hãy overflow buffer để ghi đè return address và redirect về <code>win()</code>.</p>
  <p>Server: <code>nc 35.247.183.253 9002</code></p>
  <p>Flag format: <span class="flag-format">CTF{...}</span></p>
</div>

<div class="card">
  <h3>📄 Source Code</h3>
  <pre>#include &lt;stdio.h&gt;
#include &lt;string.h&gt;

void win() {
    printf("CTF{r3t2w1n_y0u_c0ntr0l_rip}\\n");
}

void vuln() {
    char buf[40];
    printf("Enter name: ");
    gets(buf);  // Vulnerable!
}

int main() {
    vuln();
    return 0;
}</pre>
</div>

<div class="card">
  <h3>💡 Gợi ý</h3>
  <ul>
    <li>Tìm địa chỉ hàm <code>win()</code>: <code>objdump -d binary | grep win</code></li>
    <li>Tìm offset: dùng <code>cyclic</code> từ pwntools</li>
    <li>Payload = <code>b'A' * offset + p64(win_addr)</code></li>
    <li>Nếu segfault trong win(): thêm <code>ret gadget</code> để fix stack alignment</li>
    <li>Tool: <code>pwntools</code>, <code>GDB</code>, <code>ROPgadget</code></li>
  </ul>
</div>

<div class="card">
  <h3>📥 Download Binary</h3>
  <a class="btn" href="/download">⬇ Download ret2win</a>
</div>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download')
def download():
    binary = b'\x7fELF\x02\x01\x01\x00' + b'\x00' * 8
    binary += b'ret2win Challenge\x00'
    binary += b'Enter name: \x00'
    binary += b'win\x00vuln\x00main\x00gets\x00'
    binary += b'CTF{r3t2w1n_y0u_c0ntr0l_rip}\x00'
    binary += b'\x00' * 128
    return send_file(
        io.BytesIO(binary),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='ret2win'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)