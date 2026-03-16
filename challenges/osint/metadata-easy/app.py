from flask import Flask, render_template_string, send_file
import io
import struct

app = Flask(__name__)

HTML = '''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>EXIF Metadata — GDU-CTF</title>
<style>
body{font-family:monospace;background:#0d1117;color:#c9d1d9;max-width:800px;margin:0 auto;padding:40px 20px;}
h1{color:#38bdf8;letter-spacing:.1em;}
.badge{display:inline-block;padding:4px 12px;border-radius:4px;font-size:.75rem;font-weight:700;background:#0369a1;color:#fff;margin-bottom:16px;}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:24px;margin:16px 0;}
.card h3{color:#38bdf8;margin:0 0 12px;}
pre{background:#0d1117;padding:16px;border-radius:6px;overflow-x:auto;color:#58d68d;border:1px solid #30363d;}
a.btn{display:inline-block;background:#38bdf8;color:#000;font-weight:700;padding:10px 24px;border-radius:6px;text-decoration:none;margin-top:12px;}
.flag-format{color:#ffd600;font-weight:700;}
code{background:#1f2937;padding:2px 6px;border-radius:3px;color:#58d68d;}
img{max-width:100%;border-radius:8px;border:1px solid #30363d;}
</style>
</head>
<body>
<h1>🕵️ EXIF Metadata</h1>
<span class="badge">OSINT — EASY</span>
<span class="badge" style="background:#15803d;">200 pts</span>

<div class="card">
  <h3>📋 Mô tả</h3>
  <p>Một bức ảnh được chụp và upload lên. Flag được giấu trong metadata EXIF của ảnh. Hãy đọc metadata để tìm flag.</p>
  <p>Flag format: <span class="flag-format">CTF{...}</span></p>
</div>

<div class="card">
  <h3>🖼 Ảnh Challenge</h3>
  <p>Download ảnh và đọc EXIF metadata:</p>
  <a class="btn" href="/download">⬇ Download photo.jpg</a>
</div>

<div class="card">
  <h3>💡 Gợi ý</h3>
  <ul>
    <li>Dùng: <code>exiftool photo.jpg</code></li>
    <li>Hoặc: <code>strings photo.jpg | grep CTF</code></li>
    <li>Tìm các trường: <code>Comment</code>, <code>Description</code>, <code>Artist</code></li>
    <li>Online: <a href="https://exif.tools" target="_blank" style="color:#38bdf8;">exif.tools</a></li>
  </ul>
</div>
</body>
</html>'''

def create_jpeg_with_exif():
    """Tạo JPEG với EXIF comment chứa flag"""
    flag = b'CTF{3x1f_m3t4d4t4_l34ks}'
    
    # JPEG SOI marker
    jpeg = b'\xff\xd8'
    
    # APP1 marker (EXIF)
    exif_data = b'Exif\x00\x00'
    # TIFF header (little endian)
    exif_data += b'II\x2a\x00\x08\x00\x00\x00'
    # IFD0 - 1 entry
    exif_data += b'\x01\x00'
    # Tag 0x013B (Artist) - ASCII
    artist = b'GDU-CTF Challenge\x00'
    exif_data += struct.pack('<HHI', 0x013B, 2, len(artist))
    exif_data += struct.pack('<I', 8 + 2 + 12 + 4)
    # Next IFD offset (0 = none)
    exif_data += b'\x00\x00\x00\x00'
    exif_data += artist
    
    app1_len = len(exif_data) + 2
    jpeg += b'\xff\xe1'
    jpeg += struct.pack('>H', app1_len)
    jpeg += exif_data
    
    # APP0 JFIF
    jfif = b'JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
    jpeg += b'\xff\xe0'
    jpeg += struct.pack('>H', len(jfif) + 2)
    jpeg += jfif
    
    # Comment marker chứa flag
    comment = flag
    jpeg += b'\xff\xfe'
    jpeg += struct.pack('>H', len(comment) + 2)
    jpeg += comment
    
    # Minimal JPEG body (grey 1x1 pixel)
    jpeg += b'\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07'
    jpeg += b'\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19'
    jpeg += b'\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c'
    jpeg += b' $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\x1edL'
    jpeg += b'\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00'
    jpeg += b'\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01'
    jpeg += b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04'
    jpeg += b'\x05\x06\x07\x08\t\n\x0b'
    jpeg += b'\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xf5\x0a\xff\xd9'
    
    return jpeg

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download')
def download():
    jpeg_data = create_jpeg_with_exif()
    return send_file(
        io.BytesIO(jpeg_data),
        mimetype='image/jpeg',
        as_attachment=True,
        download_name='photo.jpg'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)