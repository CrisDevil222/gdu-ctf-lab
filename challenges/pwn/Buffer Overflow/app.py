from flask import Flask, render_template_string, send_file
import io

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Buffer Overflow — GDU-CTF</title>
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
<h1>💥 Buffer Overflow</h1>
<span class="badge">PWN — EASY</span>
<span class="badge" style="background:#1d4ed8;">200 pts</span>

<div class="card">
  <h3>📋 Mô tả</h3>
  <p>Một chương trình C đơn giản có lỗ hổng buffer overflow. Hãy khai thác để ghi đè biến <code>target</code> và lấy flag.</p>
  <p>Server: <code>nc 35.247.183.253 9001</code></p>
  <p>Flag format: <span class="flag-format">CTF{...}</span></p>
</div>

<div class="card">
  <h3>📄 Source Code</h3>
  <pre>#include &lt;stdio.h&gt;
#include &lt;string.h&gt;

void print_flag() {
    printf("CTF{buff3r_0v3rfl0w_smash_th3_st4ck}\\n");
}

int main() {
    char buf[64];
    int target = 0;
    
    printf("Enter your name: ");
    gets(buf);  // Vulnerable!
    
    if (target == 0xdeadbeef) {
        print_flag();
    } else {
        printf("Hello, %s!\\n", buf);
    }
    return 0;
}</pre>
</div>

<div class="card">
  <h3>💡 Gợi ý</h3>
  <ul>
    <li>Hàm <code>gets()</code> không giới hạn input — đây là lỗ hổng</li>
    <li>Buffer <code>buf</code> có 64 bytes, <code>target</code> nằm ngay sau</li>
    <li>Cần ghi đè <code>target</code> thành <code>0xdeadbeef</code></li>
    <li>Nhớ byte order: little-endian <code>\xef\xbe\xad\xde</code></li>
    <li>Tool: <code>python3</code>, <code>pwntools</code></li>
  </ul>
</div>

<div class="card">
  <h3>📥 Download Binary</h3>
  <a class="btn" href="/download">⬇ Download bof_challenge</a>
</div>
</body>
</html>'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download')
def download():
    # ELF binary stub
    binary = b'\x7fELF\x02\x01\x01\x00' + b'\x00' * 8
    binary += b'BOF Challenge\x00'
    binary += b'Enter your name: \x00'
    binary += b'CTF{buff3r_0v3rfl0w_smash_th3_st4ck}\x00'
    binary += b'gets\x00' + b'printf\x00'
    binary += b'\x00' * 128
    return send_file(
        io.BytesIO(binary),
        mimetype='application/octet-stream',
        as_attachment=True,
        download_name='bof_challenge'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)