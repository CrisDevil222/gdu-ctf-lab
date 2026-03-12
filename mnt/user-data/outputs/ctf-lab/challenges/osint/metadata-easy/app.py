from flask import Flask, request, render_template_string, send_file
import os, io
from PIL import Image
import piexif, json

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{3x1f_m3t4d4t4_l34ks}")

def create_image_with_metadata():
    """Tạo ảnh với flag ẩn trong EXIF metadata"""
    img = Image.new("RGB", (400, 300))
    pixels = img.load()
    for x in range(400):
        for y in range(300):
            pixels[x, y] = (
                (x * 2) % 256,
                (y * 2) % 256,
                ((x + y) * 2) % 256
            )

    # Tạo EXIF data với flag ẩn
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: b"GDU-CTF Camera",
            piexif.ImageIFD.Model: b"Challenge v1.0",
            piexif.ImageIFD.Software: b"CTFd Photo Editor",
            piexif.ImageIFD.Artist: FLAG.encode(),  # FLAG ở đây!
            piexif.ImageIFD.Copyright: b"GDU-CTF 2026",
            piexif.ImageIFD.ImageDescription: b"A normal photo, nothing to see here...",
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: b"2026:03:11 00:00:00",
            piexif.ExifIFD.UserComment: b"UNICODE\x00\x00Look at the artist field!",
        },
        "GPS": {
            piexif.GPSIFD.GPSLatitudeRef: b"N",
            piexif.GPSIFD.GPSLatitude: ((10, 1), (49, 1), (0, 1)),
            piexif.GPSIFD.GPSLongitudeRef: b"E",
            piexif.GPSIFD.GPSLongitude: ((106, 1), (41, 1), (0, 1)),
        }
    }

    exif_bytes = piexif.dump(exif_dict)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", exif=exif_bytes, quality=85)
    buf.seek(0)
    return buf

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OSINT - Metadata</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Segoe UI',sans-serif; background:#0f1923; color:#e0e8f0; min-height:100vh; padding:40px; }
        .container { max-width:700px; margin:0 auto; }
        h1 { color:#00aaff; font-size:2rem; margin-bottom:8px; }
        .sub { color:#4488aa; margin-bottom:32px; }
        .photo-box { background:#162030; border:1px solid #1a3a5a; border-radius:8px; padding:24px; margin-bottom:24px; text-align:center; }
        .photo-box img { max-width:300px; border:2px solid #1a3a5a; border-radius:4px; }
        .hint { background:#162030; border-left:3px solid #00aaff; padding:16px; color:#88ccff; font-size:0.85rem; line-height:1.8; margin-bottom:24px; }
        .hint code { background:#0a1520; padding:2px 6px; border-radius:3px; color:#00ffcc; font-family:monospace; }
        .tools { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:24px; }
        .tool { background:#162030; border:1px solid #1a3a5a; border-radius:8px; padding:16px; font-size:0.85rem; }
        .tool h3 { color:#00aaff; margin-bottom:8px; }
        form { display:flex; gap:12px; }
        input { flex:1; padding:12px; background:#162030; border:1px solid #00aaff; color:#e0e8f0; font-family:inherit; border-radius:4px; }
        button { padding:12px 24px; background:#0a2040; border:1px solid #00aaff; color:#00aaff; font-family:inherit; cursor:pointer; border-radius:4px; }
        .result { margin-top:16px; padding:12px; border-radius:4px; }
        .success { border:1px solid #00ff00; color:#00ff00; background:#001100; }
        .error { border:1px solid #ff4444; color:#ff4444; background:#110000; }
        a { color:#00aaff; }
    </style>
</head>
<body>
<div class="container">
    <h1>🔍 Photo Investigation</h1>
    <p class="sub">OSINT — EXIF Metadata [Easy]</p>

    <div class="photo-box">
        <p style="color:#4488aa;margin-bottom:12px;font-size:0.85rem">📸 Suspicious photo received from unknown source</p>
        <img src="/image" alt="suspicious photo"><br>
        <a href="/image" download="photo.jpg" style="font-size:0.85rem;margin-top:8px;display:inline-block">⬇️ Download photo.jpg</a>
    </div>

    <div class="hint">
        🕵️ <strong>Mission:</strong> Người dùng gửi ảnh này nhưng muốn giấu danh tính. Tuy nhiên ảnh JPEG thường chứa <strong>EXIF metadata</strong> — thông tin ẩn bao gồm thiết bị chụp, GPS location, tác giả...<br><br>
        Hãy xem metadata của ảnh để tìm flag!
    </div>

    <div class="tools">
        <div class="tool">
            <h3>🐧 Linux/Mac</h3>
            <code>exiftool photo.jpg</code><br>
            <code>identify -verbose photo.jpg</code>
        </div>
        <div class="tool">
            <h3>🌐 Online</h3>
            <a href="https://www.metadata2go.com" target="_blank">metadata2go.com</a><br>
            <a href="https://exifmeta.com" target="_blank">exifmeta.com</a>
        </div>
        <div class="tool">
            <h3>🐍 Python</h3>
            <code>from PIL import Image<br>import piexif<br>img=Image.open('photo.jpg')<br>exif=piexif.load(img.info['exif'])<br>print(exif)</code>
        </div>
        <div class="tool">
            <h3>🪟 Windows</h3>
            Right-click ảnh → Properties → Details tab
        </div>
    </div>

    <form method="POST">
        <input type="text" name="flag" placeholder="CTF{...}" autocomplete="off">
        <button type="submit">Submit Flag</button>
    </form>
    {% if result %}
    <div class="result {{ result_class }}">{{ result }}</div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE, result=None, result_class=None)

@app.route("/", methods=["POST"])
def submit():
    flag = request.form.get("flag", "").strip()
    if flag == FLAG:
        result = f"🎉 Metadata exposed! {FLAG}"
        result_class = "success"
    else:
        result = "❌ Wrong! Check the metadata again..."
        result_class = "error"
    return render_template_string(TEMPLATE, result=result, result_class=result_class)

@app.route("/image")
def get_image():
    return send_file(create_image_with_metadata(), mimetype="image/jpeg", download_name="photo.jpg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
