import os
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/challenges')
def challenges():
    return render_template('challenges.html')

@app.route('/scoreboard')
def scoreboard():
    return render_template('scoreboard.html')

@app.route('/api/scoreboard')
def api_scoreboard():
    """Mock scoreboard API – replace with real CTFd integration when ready."""
    teams = [
        {"rank": 1,  "name": "0xC0FFEE",      "score": 4850, "solves": 19, "last": "2025-12-31 22:41"},
        {"rank": 2,  "name": "NullPointers",  "score": 4320, "solves": 17, "last": "2025-12-31 22:55"},
        {"rank": 3,  "name": "ByteBreakers",  "score": 3970, "solves": 16, "last": "2025-12-31 23:02"},
        {"rank": 4,  "name": "CryptoCrew",    "score": 3500, "solves": 14, "last": "2025-12-31 21:30"},
        {"rank": 5,  "name": "StackSmashers", "score": 3100, "solves": 13, "last": "2025-12-31 20:50"},
        {"rank": 6,  "name": "HexHunters",    "score": 2800, "solves": 11, "last": "2025-12-31 20:10"},
        {"rank": 7,  "name": "GhostPing",     "score": 2400, "solves": 10, "last": "2025-12-31 19:45"},
        {"rank": 8,  "name": "RevSlayers",    "score": 2150, "solves":  9, "last": "2025-12-31 18:30"},
        {"rank": 9,  "name": "NetNinjas",     "score": 1900, "solves":  8, "last": "2025-12-31 17:55"},
        {"rank": 10, "name": "PwnNewbies",    "score": 1600, "solves":  7, "last": "2025-12-31 17:20"},
    ]
    return jsonify({"success": True, "data": teams})

@app.route('/admin-secret-power')
def toggle_maintenance():
    key = request.args.get('key')
    if key != 'CrisDevil222':
        return "Unauthorized! Get out Hacker!", 401
    
    flag_path = '/shared_state/maintenance.flag'
    html_path = '/shared_state/maintenance.html'
    
    maintenance_html = """<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>GDU CTF - System Maintenance</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            background-color: #050505; 
            color: #00ff00; 
            font-family: 'Consolas', 'Courier New', monospace; 
            text-align: center; 
            padding-top: 15vh; 
            margin: 0;
            overflow: hidden;
        }
        h1 { font-size: 3rem; text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00; margin-bottom: 5px;}
        h2 { color: #ff3333; text-shadow: 0 0 10px #ff3333; margin-top: 0; font-size: 2rem;}
        p { font-size: 1.2rem; margin-top: 20px;}
        .loading {
            margin: 40px auto;
            width: 50%;
            height: 25px;
            border: 2px solid #00ff00;
            position: relative;
        }
        .progress {
            height: 100%;
            background-color: #00ff00;
            width: 0%;
            animation: fill 5s infinite;
        }
        .blink { animation: blink 1s steps(2, start) infinite; }
        @keyframes blink { to { visibility: hidden; } }
        @keyframes fill {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 0%; } /* Reset to simulate ongoing work */
        }
    </style>
</head>
<body>
    <h1>SYSTEM MAINTENANCE</h1>
    <h2>[!] ACCESS DENIED</h2>
    <p>Hệ thống CTF đang được bảo trì hoặc cập nhật để nâng cao trải nghiệm.</p>
    <p>Xin vui lòng quay lại sau. Admin is working...<span class="blink">_</span></p>
    
    <div class="loading">
        <div class="progress"></div>
    </div>
    
    <p style="margin-top: 50px; font-size: 0.9em; color: #555;">GDU CTF Lab Platform</p>
</body>
</html>"""

    # Hỗ trợ tự sinh thư mục nếu lỡ chạy ở chế độ Windows Local 
    os.makedirs('/shared_state', exist_ok=True)

    if os.path.exists(flag_path):
        os.remove(flag_path)
        if os.path.exists(html_path):
            os.remove(html_path)
        return "<h1 style='color:green;'>[OFF] Chế độ Bảo trì đã được TẮT! Nginx đã cho phép truy cập.</h1>"
    else:
        with open(flag_path, 'w') as f:
            f.write('MAINTENANCE ON')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(maintenance_html)
        return "<h1 style='color:red;'>[ON] Chế độ Bảo trì đã được BẬT! Nginx hiện đang TỪ CHỐI tất cả lưu lượng và hiển thị trang Đen.</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
