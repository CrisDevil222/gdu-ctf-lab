from flask import Flask, request, render_template_string, send_file
import os, io
from PIL import Image
import struct

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "")

def create_stego_image():
    """Create a PNG with flag hidden in LSB of red channel"""
    img = Image.new("RGB", (200, 200), color=(100, 149, 237))  # Cornflower blue

    # Draw some pixels to look like a real image
    pixels = img.load()
    for x in range(200):
        for y in range(200):
            r = (x * y) % 256
            g = (x + y) % 256
            b = (x * 2 + y) % 256
            pixels[x, y] = (r, g, b)

    # Hide flag in LSB of red channel, top-left pixels
    flag_bits = ''.join(format(ord(c), '08b') for c in FLAG + '\x00')
    pixel_list = list(img.getdata())

    for i, bit in enumerate(flag_bits):
        if i >= len(pixel_list):
            break
        r, g, b = pixel_list[i]
        r = (r & 0xFE) | int(bit)  # set LSB
        pixel_list[i] = (r, g, b)

    img.putdata(pixel_list)
    return img

def lsb_extract(img):
    """Extract LSB from red channel"""
    pixels = list(img.getdata())
    bits = [str(p[0] & 1) for p in pixels]
    chars = []
    for i in range(0, len(bits) - 7, 8):
        byte = ''.join(bits[i:i+8])
        ch = chr(int(byte, 2))
        if ch == '\x00':
            break
        chars.append(ch)
    return ''.join(chars)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Image Lab - Forensics Challenge</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Courier New', monospace; background: #1a1a2e; color: #e0e0ff; min-height: 100vh; padding: 40px; }
        .container { max-width: 700px; margin: 0 auto; }
        h1 { color: #7b68ee; font-size: 1.8rem; margin-bottom: 8px; }
        .sub { color: #5a4e8a; margin-bottom: 32px; font-size: 0.85rem; }
        .info { background: #16213e; border: 1px solid #7b68ee; padding: 20px; border-radius: 8px; font-size: 0.85rem; line-height: 1.8; margin-bottom: 24px; }
        .info code { background: #0f3460; padding: 2px 6px; border-radius: 3px; color: #7b68ee; }
        .image-box { background: #16213e; border: 1px solid #3a3060; padding: 24px; border-radius: 8px; text-align: center; margin-bottom: 24px; }
        .image-box img { max-width: 200px; border: 2px solid #7b68ee; }
        .upload-box { background: #16213e; border: 1px dashed #7b68ee; padding: 24px; border-radius: 8px; margin-bottom: 24px; }
        input[type=file] { color: #e0e0ff; font-family: inherit; margin-bottom: 12px; display: block; }
        button { padding: 10px 24px; background: #7b68ee; border: none; border-radius: 6px; color: white; cursor: pointer; font-family: inherit; }
        .result { margin-top: 16px; padding: 16px; background: #0f3460; border-radius: 6px; font-size: 0.9rem; }
        .flag-found { background: #052e16; border: 1px solid #22c55e; color: #4ade80; padding: 16px; border-radius: 8px; font-size: 1rem; margin-top: 12px; }
    </style>
</head>
<body>
<div class="container">
    <h1>🔍 Image Lab</h1>
    <p class="sub">Forensics / Steganography Challenge [Easy]</p>

    <div class="info">
        🕵️ <strong>Mission:</strong> Someone hid a secret message inside this image using <strong>LSB Steganography</strong>.<br>
        The flag is embedded in the <strong>Least Significant Bit (LSB)</strong> of the red channel of each pixel.<br><br>
        <strong>How to solve manually:</strong><br>
        1. Download the image below<br>
        2. Use tools like <code>stegsolve</code>, <code>zsteg</code>, or write a Python script:<br>
        <code>from PIL import Image; img=Image.open('stego.png'); bits=[str(p[0]&1) for p in img.getdata()]</code><br><br>
        <strong>Or:</strong> Upload the image here and we'll extract it for you!
    </div>

    <div class="image-box">
        <p style="margin-bottom:12px;color:#5a4e8a;">🖼️ Suspicious Image (download me!)</p>
        <img src="/image" alt="Stego Image"><br>
        <a href="/image" download="stego.png" style="color:#7b68ee;font-size:0.85rem;margin-top:8px;display:inline-block;">⬇️ Download stego.png</a>
    </div>

    <div class="upload-box">
        <h3 style="margin-bottom:16px;color:#7b68ee;">🔓 LSB Extractor</h3>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <button type="submit">Extract Hidden Message</button>
        </form>
        {% if extracted %}
        <div class="result">
            <strong>Extracted:</strong> {{ extracted }}
            {% if flag_found %}
            <div class="flag-found">🏆 Flag found: {{ extracted }}</div>
            {% endif %}
        </div>
        {% endif %}
    </div>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE, extracted=None, flag_found=False)

@app.route("/image")
def get_image():
    img = create_stego_image()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png", download_name="stego.png")

@app.route("/", methods=["POST"])
def extract():
    f = request.files.get("image")
    extracted = None
    flag_found = False
    if f:
        try:
            img = Image.open(f.stream)
            extracted = lsb_extract(img)
            if extracted and extracted.startswith("CTF{"):
                flag_found = True
        except Exception as e:
            extracted = f"Error: {str(e)}"
    return render_template_string(TEMPLATE, extracted=extracted, flag_found=flag_found)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
