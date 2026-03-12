from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{x0r_1s_s1mpl3_crypt0}")

# XOR encrypt flag với key
XOR_KEY = 0x42
ENCRYPTED = [ord(c) ^ XOR_KEY for c in FLAG]
ENCRYPTED_HEX = ' '.join(f'{b:02x}' for b in ENCRYPTED)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>RE - XOR Cipher</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Courier New', monospace; background: #0d0d0d; color: #00ff00; min-height: 100vh; padding: 40px; }
        .container { max-width: 700px; margin: 0 auto; }
        h1 { color: #00ff00; font-size: 2rem; margin-bottom: 8px; text-shadow: 0 0 10px #00ff00; }
        .sub { color: #008800; margin-bottom: 32px; font-size: 0.85rem; }
        .terminal { background: #111; border: 1px solid #00ff00; border-radius: 4px; padding: 24px; margin-bottom: 24px; line-height: 1.8; }
        .cmd { color: #ffff00; }
        .out { color: #00ff00; }
        .hex { color: #ff8800; font-size: 1.1rem; letter-spacing: 2px; word-break: break-all; }
        .hint { background: #111; border-left: 3px solid #ffff00; padding: 16px; color: #ffff00; font-size: 0.85rem; line-height: 1.8; margin-bottom: 24px; }
        .code { background: #0a0a0a; border: 1px solid #333; padding: 12px; border-radius: 4px; margin: 8px 0; color: #00aaff; }
        form { display: flex; gap: 12px; }
        input { flex: 1; padding: 12px; background: #111; border: 1px solid #00ff00; color: #00ff00; font-family: inherit; border-radius: 4px; }
        button { padding: 12px 24px; background: #003300; border: 1px solid #00ff00; color: #00ff00; font-family: inherit; cursor: pointer; border-radius: 4px; }
        .result { margin-top: 16px; padding: 12px; border-radius: 4px; }
        .success { border: 1px solid #00ff00; color: #00ff00; background: #001100; }
        .error { border: 1px solid #ff0000; color: #ff0000; background: #110000; }
    </style>
</head>
<body>
<div class="container">
    <h1>$ analyze xor_binary</h1>
    <p class="sub">Reverse Engineering — XOR Cipher [Easy]</p>

    <div class="terminal">
        <div class="cmd"># Phân tích binary, tìm thấy đoạn code sau:</div>
        <br>
        <div class="code">
        int key = 0x42;<br>
        char encrypted[] = { {{ encrypted_bytes }} };<br>
        for(int i=0; i&lt;len; i++)<br>
        &nbsp;&nbsp;printf("%c", encrypted[i] ^ key);
        </div>
        <br>
        <div class="cmd"># Encrypted bytes (hex):</div>
        <div class="hex">{{ encrypted_hex }}</div>
    </div>

    <div class="hint">
        💡 <strong>Hint:</strong> XOR có tính chất đối xứng: <code>A XOR B XOR B = A</code><br>
        Nếu <code>plaintext XOR key = ciphertext</code><br>
        Thì <code>ciphertext XOR key = plaintext</code><br><br>
        <strong>Python giải:</strong><br>
        <code>encrypted = [{{ encrypted_bytes }}]</code><br>
        <code>key = 0x42</code><br>
        <code>print(''.join(chr(b ^ key) for b in encrypted))</code>
    </div>

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
            result = f"🎉 Correct! {FLAG}"
            result_class = "success"
        else:
            result = "❌ Wrong! Try again..."
            result_class = "error"
    return render_template_string(TEMPLATE,
        result=result,
        result_class=result_class,
        encrypted_hex=ENCRYPTED_HEX,
        encrypted_bytes=', '.join(f'0x{b:02x}' for b in ENCRYPTED)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
