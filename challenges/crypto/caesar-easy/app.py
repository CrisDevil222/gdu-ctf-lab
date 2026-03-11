from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{c4es4r_c1ph3r_1s_w34k}")

def caesar_encrypt(text, shift):
    result = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result += ch
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

ENCRYPTED_FLAG = caesar_encrypt(FLAG, 13)  # ROT13

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Caesar Cipher - Crypto Challenge</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Georgia', serif; background: #0a0a0a; color: #d4af37; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .scroll { background: #1a1206; border: 2px solid #d4af37; border-radius: 4px; padding: 48px; max-width: 640px; width: 90%; box-shadow: 0 0 40px rgba(212,175,55,0.15); }
        h1 { font-size: 2rem; text-align: center; margin-bottom: 8px; }
        .sub { text-align: center; color: #8a6f1e; font-size: 0.85rem; margin-bottom: 32px; }
        .cipher-block { background: #0f0c02; border: 1px solid #8a6f1e; padding: 20px; border-radius: 4px; font-family: monospace; font-size: 1rem; letter-spacing: 2px; word-break: break-all; margin-bottom: 24px; text-align: center; color: #ffd700; }
        .info { border-left: 3px solid #d4af37; padding: 12px 16px; font-size: 0.85rem; line-height: 1.7; color: #c9a227; margin-bottom: 24px; }
        label { display: block; margin-bottom: 6px; font-size: 0.85rem; color: #8a6f1e; }
        input, textarea { width: 100%; padding: 10px; background: #0f0c02; border: 1px solid #8a6f1e; border-radius: 4px; color: #d4af37; font-family: monospace; margin-bottom: 12px; }
        select { width: 100%; padding: 10px; background: #0f0c02; border: 1px solid #8a6f1e; border-radius: 4px; color: #d4af37; font-family: inherit; margin-bottom: 12px; }
        button { width: 100%; padding: 12px; background: #d4af37; color: #0a0a0a; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; font-family: inherit; font-weight: bold; }
        .result { margin-top: 16px; padding: 16px; background: #0f0c02; border: 1px solid #d4af37; border-radius: 4px; font-family: monospace; word-break: break-all; }
        .success { border-color: #22c55e; color: #22c55e; }
    </style>
</head>
<body>
<div class="scroll">
    <h1>🏛️ Caesar's Vault</h1>
    <p class="sub">Cryptography Challenge [Easy]</p>

    <div class="info">
        📜 <strong>Mission:</strong> The Roman emperor has encrypted the flag using a simple shift cipher.<br>
        The encrypted message is displayed below. Crack the cipher to find the original flag!<br>
        <strong>Hint:</strong> Caesar famously used a shift of 3... but this uses ROT13.
    </div>

    <div class="cipher-block">{{ encrypted }}</div>

    <h3 style="margin-bottom:16px;color:#8a6f1e;">🔓 Decoder Tool</h3>
    <form method="POST">
        <label>Ciphertext to decode:</label>
        <textarea name="ciphertext" rows="3" placeholder="Paste ciphertext here...">{{ ct }}</textarea>
        <label>Shift amount (1-25):</label>
        <select name="shift">
            {% for i in range(1, 26) %}
            <option value="{{ i }}" {% if i == selected_shift %}selected{% endif %}>Shift {{ i }}</option>
            {% endfor %}
        </select>
        <button type="submit">Decode 🗝️</button>
    </form>

    {% if decoded %}
    <div class="result {% if flag_found %}success{% endif %}">
        <strong>Decoded:</strong> {{ decoded }}
        {% if flag_found %}
        <br><br>🏆 You found the flag!
        {% endif %}
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    decoded = None
    ct = ENCRYPTED_FLAG
    selected_shift = 1
    flag_found = False

    if request.method == "POST":
        ct = request.form.get("ciphertext", ENCRYPTED_FLAG)
        try:
            selected_shift = int(request.form.get("shift", 1))
        except:
            selected_shift = 1
        decoded = caesar_decrypt(ct, selected_shift)
        if FLAG in decoded:
            flag_found = True

    return render_template_string(TEMPLATE,
        encrypted=ENCRYPTED_FLAG,
        decoded=decoded,
        ct=ct,
        selected_shift=selected_shift,
        flag_found=flag_found,
        range=range
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
